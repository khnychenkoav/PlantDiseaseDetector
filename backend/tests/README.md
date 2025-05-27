### 1. Запуск тестов

1. Убедитесь, что в проекте установлены зависимости для тестирования:

   ```sh
   pip install -r requirements.txt
   ```
2. Запустите все тесты командой:

   ```sh
   pytest
   ```
3. Для одновременного тестирования с выводом асинхронных логов:

   ```sh
   pytest -s
   ```

---

### 2. Структура каталогов

```
backend/
└── tests/
    ├── conftest.py            # Общие фикстуры и настройка тестовой БД
    ├── test_dao/              # Unit-тесты для DAO-слоя
    │   ├── test_history_dao.py
    │   └── test_user_dao.py
    ├── test_routes/           # Интеграционные тесты HTTP-маршрутов
    │   ├── test_auth.py
    │   ├── test_disease.py
    │   ├── test_history.py
    │   └── test_user.py
    └── test_services/         # Unit-тесты сервисного (ML) слоя
        └── test_model_service.py
```

---

### 3. Общая настройка (conftest.py)

* **Тестовая БД**

  * Создаётся `AsyncEngine` с `NullPool` и фабрикой `TestingSessionLocal`.
  * Перед каждым тестом (`function`-scope) сбрасываются и создаются заново все таблицы (`Base.metadata.drop_all` / `create_all`).

* **Monkey-patch DAO**

  * Подменяются фабрики сессий (`async_session_maker`) в модулях `app.dao.*` на `TestingSessionLocal`, чтобы DAO писали в тестовую БД.

* **FastAPI dependency override**

  * Зависимость `get_async_session` заменяется на генератор из `TestingSessionLocal`, чтобы HTTP-запросы использовали тестовую БД.

* **Асинхронный HTTP-клиент**

  * Фикстура `client` создаёт `httpx.AsyncClient` с `ASGITransport(app=app)` и базовым URL `http://test`.
  * Дополнительные фикстуры `authenticated_client` и `authenticated_admin_client` логинятся через `/auth/login/` и добавляют токен в заголовки.

* **Тестовые данные**

  * `test_user`, `test_admin_user` и `test_disease` — создают в БД пользователя/админа/болезнь через соответствующие DAO.
  * `db_session` — даёт прямой доступ к `TestingSessionLocal` для произвольных запросов и проверок.

---

### 4. Unit-тесты DAO-уровня (`test_dao`)

#### 4.1. `test_user_dao.py`

* **`create_user`**: проверяется корректность создания и хеширования пароля.
* **`update_user`**: сценарии

  * Успешное обновление имени и хеша;
  * Попытка обновить несуществующего пользователя → `NoResultFound`;
  * Пустой или некорректный набор полей → без изменений.

#### 4.2. `test_history_dao.py`

* **`create_record`**:

  * Проверка возвращаемого объекта, полей (`user_id`, `disease_id`, `image_path`, `created_at`).
  * Прямая верификация записи через `db_session`.
* **`get_history`**:

  * Пользователь с записями → возвращает только его;
  * Без записей → пустой список;
  * Не существующий `user_id` → пустой список;
  * Проверяется `joinedload` связей: `record.user` и `record.disease` загружены.

---

### 5. Интеграционные тесты маршрутов (`test_routes`)

#### 5.1. `test_auth.py`

* **Регистрация** (`/auth/register/`):

  * Успех: возвращает `{name, email}`, без пароля.
  * Параметризация ошибок: дубликат, валидация полей → 409 или 422.
* **Логин** (`/auth/login/`):

  * Успех: присутствует `access_token`.
  * Ошибки: неверный пароль, несуществующий пользователь, валидация → 401 или 422.
* **Logout** (`/users/logout/`):

  * Успешный выход, затем защищённые маршруты (`/users/me/`) должны вернуть 401.

#### 5.2. `test_disease.py`

* **Создание болезни** (`/diseases/create/`):

  * 401 если не авторизован, 403 если не админ, 200 если админ + проверка в БД.
* **Загрузка файла** (`/diseases/upload/`):

  * 401 для неавторизованных;
  * Моки `predict`, `open`, `os.makedirs`, DAO:

    * Проверка сохранения файла, предсказания, поиска болезни, создания истории;
    * Fallback на «НеизвестнаяБолезнь», если предсказание не в БД.
* **Инициализация из JSON** (`/diseases/create/init/`):

  * Ошибка чтения файла → 500 с деталями;
  * Успех: подсчёт созданных записей, дубликатов, всех обработанных элементов;
  * Продолжение при ошибке части вставок (side-effect DAO).
* **Получить все болезни** (`/diseases/all/`):

  * Пустая БД → `[]`;
  * Непустая → список объектов с полями `name`, `reason`, `recommendation`.

#### 5.3. `test_history.py`

* **Получить историю** (`/history/all/`):

  * 401 для неавторизованных;
  * Мок DAO: 0 или >0 записей;
  * Проверка сериализации полей, в том числе `time` в ISO-формате.

#### 5.4. `test_user.py`

* **`/users/me/`**: 401 без токена, 200 с данными пользователя.
* **`/users/all/`**: 401/403 для не-админов, 200 со списком пользователей для админа.
* **`/users/change_role/`**: 401/403/409/422 сценарии неавторизации, смены ролей, ошибок валидации.

---

### 6. Unit-тесты сервисного ML-слоя (`test_services/test_model_service.py`)

* **Инициализация `ModelService`**: все поля (`model`, `device`, `class_names`, `transforms`) изначально `None`.
* **`load_model()`**:

  * CPU vs CUDA (`torch.cuda.is_available()`) — оба пути:

    * Моки `models.resnet50`, `nn.Linear`, `torch.load`, `json.load`, `open`;
    * Проверка замены последнего fully-connected слоя, `.to(device)`, `eval()`.
    * Сборка `transforms.Compose` и чтение `class_names` из JSON.
* **`predict(path)`**:

  * Мок PIL (`Image.open`), трансформации, `.unsqueeze`, `.to(device)`;
  * Feed-forward через `model(...)` и `torch.max`;
  * Преобразование индекса → имя класса из `class_names`.

---
