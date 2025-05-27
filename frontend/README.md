### 1. Введение

Проект Plant Disease Detector — SPA на React, позволяющее пользователям загружать фото растений, автоматически определять заболевания и получать советы по лечению.

**Ключевые технологии:**

* **React** (v17)
* **Create React App** (CRA)
* **Formik** + **Yup** — формы и валидация
* **Axios** — HTTP-запросы
* **Bootstrap 5** + **Sass** — адаптивный UI
* **React Router DOM** (v5) — маршрутизация
* **React-Toastify** — уведомления

---

### 2. Установка и запуск

1. **Клонирование**

   ```bash
   git clone <repo-url>
   cd PlantDiseaseDetector/frontend
   ```
2. **Зависимости**

   ```bash
   npm install
   ```
3. **Запуск в dev-режиме**

   ```bash
   npm start
   ```
4. Приложение доступно по адресу `http://localhost:3000`

При необходимости изменить прокси-путь к API, добавьте в `package.json`:

```json
"proxy": "http://localhost:8081"
```

---

### 3. Структура проекта

```
frontend/
├─ public/                # статические файлы (HTML, фавиконка, manifest)
├─ src/
│  ├─ assets/images/      # изображения и SVG
│  ├─ components/         # UI-компоненты
│  ├─ layouts/            # общие лэйауты (Navbar, Footer)
│  ├─ pages/              # страницы
│  ├─ services/           # axiosInstance с interceptor
│  ├─ App.jsx             # основной компонент с роутами и ToastContainer
│  ├─ App.scss            # глобальные стили и переменные
│  ├─ index.js            # ReactDOM.render + StrictMode
│  ├─ reportWebVitals.js  # метрики производительности
│  └─ setupTests.js       # настройка jest-dom
└─ package.json           # зависимости и скрипты
```

---

### 4. Глобальные стили (App.scss)

* **Шрифты:** подключение Google Fonts (Poppins)
* **SCSS-переменные:** цвета (\$color, \$secondary, \$success и др.), размеры (\$small-size, \$large-size-2 и т.д.)
* **Bootstrap:** импорт `~bootstrap/scss/bootstrap.scss` и иконок `bootstrap-icons`
* **Утилиты:** настройки border-radius (`.rounded-*`), тени, обнуление margin/padding, flex-контейнер для `body` и `main`.

```scss
// пример переменных
$primary: rgb(61, 59, 177);
$secondary: rgb(0, 37, 57);
$success: #70c0b6;
// ...
@import "~bootstrap/scss/bootstrap.scss";
@import "~bootstrap-icons/font/bootstrap-icons.css";
```

---

### 5. Маршрутизация (App.jsx)

* Обёртка `<Router>` вокруг приложения
* **Navbar** и **Footer** рендерятся на всех страницах
* `<Switch>` + `<Route>` для:

  * `/` → `<Home />`
  * `/detect-disease` → `<DetectDisease />`
  * `/diseases-list` → `<DiseasesList />`
  * `/about` → `<AboutUs />`
  * `/history` → `<History />`
  * `/signin`, `/signup` → страницы авторизации
* **ToastContainer** для всплывающих уведомлений с параметрами:

  ```jsx
  <ToastContainer position="bottom-right" autoClose={5000} ... />
  ```

---

### 6. Сервис API (`services/axiosInstance.js`)

```js
import axios from "axios";
const axiosInstance = axios.create({ baseURL: "http://localhost:8081" });

axiosInstance.interceptors.request.use(config => {
  const token = localStorage.getItem("accessToken");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
export default axiosInstance;
```

**Interceptor** автоматически добавляет JWT-токен ко всем запросам после логина.

---

### 7. Формы: компоненты и валидация

Все формы построены на **Formik** + **Yup** и используют набор переиспользуемых компонентов:

| Компонент        | Файл                                           | Описание                                                                    |
| ---------------- | ---------------------------------------------- | --------------------------------------------------------------------------- |
| `FormInput`      | `components/FormInput/FormInput.jsx`           | Текстовое поле с лейблом, ошибками; props: `type, name, label, placeholder` |
| `FormFileInput`  | `components/FormFileInput/FormFileInput.jsx`   | Загрузка файла; сохраняет объект File в Formik; props: `accept`             |
| `FormTextArea`   | `components/FormTextArea/FormTextArea.jsx`     | Многострочный ввод; props: `rows, disabled`                                 |
| `FormSelect`     | `components/FormSelect/FormSelect.jsx`         | Dropdown с поиском по опциям; props: `options, search (enable/disable)`     |
| `LoadingSpinner` | `components/LoadingSpinner/LoadingSpinner.jsx` | Центрированный спиннер для загрузки                                         |
| `DisplayHeader`  | `components/DisplayHeader/DisplayHeader.jsx`   | Красивый заголовок с двумя цветами; props: `firstText, secondText, size`    |

**Пример использования в SignIn:**

```jsx
<Formik initialValues={...} validationSchema={...} onSubmit={handleSubmit}>
  {({ isSubmitting }) => (
    <Form>
      <FormInput name="email" type="email" label="Email" />
      <FormInput name="password" type="password" label="Password" />
      <button disabled={isSubmitting}>Sign In</button>
    </Form>
  )}
</Formik>
```

---

### 8. Layouts

#### 8.1 Navbar

* Фиксированная верхняя панель с градиентным фоном (SCSS в `Navbar.scss`).
* Кнопки-роуты через `<NavLink>` с `activeClassName='active'`, иконки Bootstrap Icons.
* Кнопки для входа/регистрации в правой части.

#### 8.2 Footer

* Градиентный фон, две колонки:

  * Лого и описание проекта
  * Ссылки на основные страницы
* Стили в `Footer.css`.

---

### 9. Страницы приложения

#### 9.1 Home (Home.jsx)

* **Overlay.jsx:** крупный баннер с call-to-action, кнопка Detect → history.push('/detect-disease')
* **Steps.jsx:** пошаговая инструкция с иконками и описанием преимуществ
* **CreateAccountBanner.jsx:** промо-блок регистрации

#### 9.2 AboutUs

* Текстовая информация о проекте, команда, миссия
* Импорт изображения `assets/images/3818806.jpg`

#### 9.3 Auth

* **SignIn.jsx:** POST `/auth/login`, сохранение `accessToken` в localStorage, toast-уведомления
* **SignUp.jsx:** POST `/auth/register`, валидация паролей (Yup.oneOf), уведомления об ошибках

#### 9.4 DetectDisease

* Форма с `FormFileInput`, отправка изображения через Axios на `/api/analyze`
* Сервер возвращает объект:

  ```json
  { "disease": "Late Blight", "treatment": "Fungicide...", "prevention": "Crop rotation..." }
  ```
* Результат выводится после формы в отдельном блоке (болезнь, лечение, профилактика).

#### 9.5 DiseasesList

* Хук `useEffect` вызывает `axios.get("/api/diseases")`
* Массив объектов `{id, name, description}` отображается в `<ul className='list-group'>`.

#### 9.6 History

* `axiosInstance.get('/history/all')`
* Данные массива `{id, time, plant, disease, treatment}` отображаются в таблице Bootstrap.

---

### 10. Уведомления и загрузка

* **React-Toastify** для успеха/ошибок: toast.success / toast.error
* **LoadingSpinner** можно внедрить в компонентах при асинхронных действиях (напр. загрузка DiseasesList или History).

---

### 11. Тестирование

* Конфигурация в `setupTests.js` для расширений jest-dom.
* Покрытие простых unit- и integration-тестов для компонентов и форм.

---

### 12. Сборка и деплой

1. Сборка:

   ```bash
   npm run build
   ```
2. Деплой содержимого папки `build/` на статический хостинг (Netlify, Vercel, GitHub Pages).

---

### 13. Настройка окружения

* Для продакшена можно передавать `REACT_APP_API_URL` через `.env`:

  ```env
  REACT_APP_API_URL=https://api.myapp.com
  ```
* В `axiosInstance.js` заменить `baseURL` на `process.env.REACT_APP_API_URL`.

---

