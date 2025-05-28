# Документация Backend — Plant Disease Detector

---

## Оглавление

1. [Общее описание](#общее-описание)
2. [Архитектура и компоненты](#архитектура-и-компоненты)
3. [Требования](#требования)
4. [Установка и запуск](#установка-и-запуск)

   * [Локальная разработка](#локальная-разработка)
   * [Docker и Docker Compose](#docker-и-docker-compose)
5. [Конфигурация](#конфигурация)
6. [Миграции базы данных](#миграции-базы-данных)
7. [Структура проекта](#структура-проекта)
8. [Подробное описание компонентов](#подробное-описание-компонентов)

   * [Конфигурация (config)](#конфигурация-config)
   * [Репозиторий и модель данных](#репозиторий-и-модель-данных)
   * [DAO (Data Access Objects)](#dao-data-access-objects)
   * [Схемы данных (Schemas)](#схемы-данных-schemas)
   * [Сервисы](#сервисы)
   * [Роуты и Endpoints](#роуты-и-endpoints)
   * [Зависимости (Depends)](#зависимости-depends)
9. [Аутентификация и авторизация](#аутентификация-и-авторизация)
10. [ML модель](#ml-модель)
11. [Загрузка и хранение файлов](#загрузка-и-хранение-файлов)
12. [Автоматическая очистка](#автоматическая-очистка)
13. [Тестирование](#тестирование)

---

## Общее описание

Данный проект реализует backend часть системы определения болезней растений по фотографии. Приложение предоставляет RESTful API, позволяя клиенту:

* Регистрировать и авторизовывать пользователей
* Загружать фото растений для анализа
* Получать предсказание болезни (название, причины, рекомендации)
* Хранить историю запросов пользователя
* Администраторам: добавлять новые болезни и инициализировать БД

---

## Архитектура и компоненты

* **FastAPI** (приложение, маршрутизация, DI)
* **SQLAlchemy** + **asyncpg** (асинхронный доступ к Postgres)
* **Alembic** (миграции БД)
* **PyTorch** (предобученная модель ResNet50)
* **JWT** (аутентификация, хранение токена в HTTP-only cookie)
* **Фоновая задача** для очистки старых файлов

---

## Требования

* Python 3.12+
* PostgreSQL 15+
* (Опционально) Docker и Docker Compose

---

## Установка и запуск

### Локальная разработка

1. Клонировать репозиторий:

   ```bash
   git clone <url репозитория>
   cd backend
   ```
2. Создать виртуальное окружение и установить зависимости:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Создать файл `.env` рядом с `main.py`:

   ```dotenv
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=plants_db
   DB_USER=postgres
   DB_PASSWORD=postgres
   SECRET_KEY=<ваш-секрет>
   ALGORITHM=HS256
   ```
4. Применить миграции:

   ```bash
   alembic upgrade head
   ```
5. Запустить сервер:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8080
   ```

### Docker и Docker Compose

1. Убедиться, что установлены Docker и Docker Compose.
2. В корне проекта выполнить:

   ```bash
   docker-compose up --build
   ```
3. Сервис backend будет доступен по адресу `http://localhost:8080`.

---

## Конфигурация

* **`app/config.py`**: загрузка переменных окружения для продакшн через Pydantic
* **`app/config_test.py`**: загрузка `env_file=.env.test` для тестов
* Функции **`get_db_url()`** и **`get_auth_data()`** возвращают URL БД и параметры JWT

---

## Миграции базы данных

* Файл `alembic.ini` указывает `script_location = app/repository/migration`
* Автогенерация миграций:

  ```bash
  alembic revision --autogenerate -m "описание"
  ```
* Применение миграций:

  ```bash
  alembic upgrade head
  ```
* Каталог миграций: `app/repository/migration/versions/`

---

## Структура проекта

```text
backend/
├─ .env.test              # Тестовые переменные
├─ Dockerfile.backend     # Сборка image
├─ docker-compose.yml     # Для контейнеров
├─ alembic.ini            # Настройки миграций
├─ requirements.txt       # Зависимости
├─ main.py                # Точка входа FastAPI
├─ app/
│   ├─ config.py          # Настройки prod
│   ├─ config_test.py     # Настройки test
│   ├─ repository/        # Engine, сессии, Base, uuid_pk, типы
│   ├─ repository/models.py # ORM модели
│   ├─ dao/               # CRUD через async_session_maker
│   ├─ schemas/           # Pydantic-модели запросов/ответов
│   ├─ services/          # JWT, security, model_service, clean_up
│   ├─ depends/           # DI (admin user проверка)
│   └─ routes/            # API-роуты по модулям
└─ tests/                 # Pytest-кейсы и фикстуры
```

---

## Подробное описание компонентов

### Конфигурация (config)

* **Settings** (`config.py`) загружает `.env` со всеми ключами.
* **ConfigTestSetup** (`config_test.py`) читает `.env.test`, игнорирует лишние.

### Репозиторий и модель данных

* **`create_async_engine`** и **`async_sessionmaker`** из SQLAlchemy обеспечивают асинхронность.
* **Типы** `uuid_pk`, `uuid_not_pk`, `created_at`, `updated_at`, `str_uniq`, `str_null_true` определены в `repository.py`.
* **Base** автоматически генерирует `__tablename__ = <класс> + "s"`.
* **Модели**:

  * **User**: id (UUID), name, email\*, password\*, флаги is\_user (=true), is\_admin, is\_super\_admin, created\_at, updated\_at
  * **Disease**: id, name\*, reason, recommendations, timestamps
  * **History**: id, user\_id → users.id, disease\_id → diseases.id, image\_path, timestamps

### DAO (Data Access Objects)

* **BaseDAO**: методы `find_all(filter_by)`, `find_one_or_none(filter_by)`
* **UserDAO**:

  * `create_user(name, email, password)`: хеширует пароль, создаёт запись
  * `update_user(update_data)`: ищет по email, обновляет поля, возвращает обновлённого
* **DiseaseDAO**:

  * `create_record(name, reason, recommendation)`
* **HistoryDAO**:

  * `create_record(user_uuid, disease_uuid, image_path)`
  * `get_history(user_id)`: выбирает с joinedload для user и disease

### Схемы данных (Schemas)

* **UserInLogin**: email, password (7–20 симв.)

* **UserInCreate**: наследует, добавляет name (3–20 симв.)

* **UserResponse**: выводит email, name

* **UserChangeRole**: email, is\_user, is\_admin, is\_super\_admin

* **DiseasesInCreate**: name, reason, recommendation

* **DiseasesInResponse**: diseases\_name, time (datetime), reason, recommendation, image\_url

* **DiseaseOut**: name, reason, recommendation

### Сервисы

* **security.py**:

  * `get_password_hash()`, `verify_password()` через bcrypt (Passlib)
  * `get_hashed_path(filename)`: MD5-фрагменты для подпапок
* **jwt.py**:

  * `create_access_token(data)`: генерирует JWT с exp = now() + 30 дней
  * `get_token(request)`: читает cookie `users_access_token`
  * `get_current_user(token)`: проверяет подпись, срок, загружает User по sub
* **model\_service.py**:

  * `ModelService.load_model()`: загружает ResNet50, заменяет fc на Linear(in, 38), `state_dict`, переводит на CPU/GPU, устанавливает transforms и class\_names из JSON
  * `predict(image_path)`: открывает, преобразует, запускает модель, возвращает словарь с ключами "eng"/"ru"
* **clean\_up.py**:

  * `delete_old_files(upload_dir, days_old=30)`: удаляет файлы старше 30 дней
  * `periodic_cleanup()`: фоновый цикл каждые 24 ч

### Зависимости (Depends)

* **get\_async\_session**: FastAPI dependency из `repository.py`
* **get\_current\_user** и **get\_current\_admin\_user**: проверка JWT и прав

### Роуты и Endpoints

#### 1. `/auth`

* **POST /login/**: логин, устанавливает cookie, возвращает access\_token
* **POST /register/**: регистрация, возвращает UserResponse

#### 2. `/users`

* **GET /all/** (admin): список всех пользователей
* **POST /logout/**: удаление cookie
* **GET /me/**: возвращает текущего пользователя
* **PUT /change\_role/** (admin): изменение флагов роли

#### 3. `/diseases`

* **POST /upload/**: аутентифицированный, загружает фото, сохраняет в `uploads/...`, вызывает модель, сохраняет историю, возвращает DiseasesInResponse
* **POST /create/** (admin): создаёт новую болезнь
* **POST /create/init/** (admin): инициализация из `class_disease.json`, возвращает статистику
* **GET /all/**: возвращает всех болезней (DiseaseOut)

#### 4. `/history`

* **GET /all/**: история текущего пользователя (list of DiseasesInResponse)

#### 5. `/analyze`

* **POST /analyze**: заглушка, возвращает `{ "disease": "Healthy" }`

---

## Аутентификация и авторизация

* Токен хранится в HTTP-only cookie `users_access_token`
* Защищённые роуты используют Depends(get\_current\_user)
* Для admin-only: Depends(get\_current\_admin\_user)

---

## ML модель

* ResNet50 без pretrained-weights, с финальным слоем на 38 классов
* Загрузка весов из `ml_model/Best-Resnet50-from-scratch-with-New-Plant-Disease.pth`
* Трансформации: Resize(224×224), ToTensor(), Normalize
* Карта индексов → классы из `class_disease.json` (ключи "eng", "ru")
* `predict` возвращает объект вида `{ "eng": ..., "ru": ... }`

---

## Загрузка и хранение файлов

* Путь сохраняется как `uploads/<хеш-фрагмент>/<имя_файла>`
* `get_hashed_path` вычисляет первые 6 символов MD5 имени файла для вложенных папок
* Статические файлы доступны по `/uploads` через StaticFiles

---

## Автоматическая очистка

* Фоновая задача запускается при старте сервера (lifespan)
* Каждые 24 ч удаляет файлы старше 30 дней из папки `uploads`

---

## Тестирование

* Pytest + pytest-asyncio
* `pytest.ini` настраивает режим asyncio
* `conftest.py`:

  * тестовая БД из `.env.test`
  * override зависимости `get_async_session`
  * фикстуры: test\_user, test\_admin\_user, test\_disease, clients
* Пакрытие:

  * DAO (UserDAO, DiseaseDAO, HistoryDAO)
  * Сервисы (ModelService, security, jwt)
  * Роуты (auth, users, diseases, history)

Запуск тестов:

```bash
pytest --cov=app
```

---

