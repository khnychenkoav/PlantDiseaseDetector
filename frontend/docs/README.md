# Plant Disease Detector Frontend Documentation

## Table of Contents

1. [Project Structure](#project-structure)
2. [Installation and Setup](#installation-and-setup)
3. [Components](#components)
   - [FormFileInput](#formfileinput)
   - [FormInput](#forminput)
   - [FormSelect](#formselect)
   - [FormTextArea](#formtextarea)
   - [LoadingSpinner](#loadingspinner)
   - [DisplayHeader](#displayheader)
4. [Layouts](#layouts)
   - [Footer](#footer)
   - [Navbar](#navbar)
5. [Pages](#pages)
   - [Home](#home)
   - [AboutUs](#aboutus)
   - [Auth](#auth)
   - [DetectDisease](#detectdisease)
   - [DiseasesList](#diseaseslist)
   - [History](#history)
6. [Services](#services)
   - [axiosInstance](#axiosinstance)

## Project Structure

```
PlantDiseaseDetector/
├── docs/
│   └── README.md
├── package.json
├── README.md
├── public/
│   ├── favicon.ico
│   ├── index.html
│   ├── logo192.png
│   ├── logo512.png
│   ├── manifest.json
│   └── robots.txt
├── src/
│   ├── App.jsx
│   ├── App.scss
│   ├── index.js
│   ├── reportWebVitals.js
│   ├── setupTests.js
│   ├── assets/
│   │   └── images/
│   │       ├── 3818806.jpg
│   │       └── default-person-image.jpg
│   ├── components/
│   │   ├── DisplayHeader/
│   │   │   └── DisplayHeader.jsx
│   │   ├── FormFileInput/
│   │   │   └── FormFileInput.jsx
│   │   ├── FormInput/
│   │   │   └── FormInput.jsx
│   │   ├── FormSelect/
│   │   │   ├── FormSelect.jsx
│   │   │   └── FormSelect.scss
│   │   ├── FormTextArea/
│   │   │   └── FormTextArea.jsx
│   │   └── LoadingSpinner/
│   │       └── LoadingSpinner.jsx
│   ├── layouts/
│   │   ├── Footer/
│   │   │   ├── Footer.jsx
│   │   │   └── Footer.css
│   │   └── Navbar/
│   │       ├── Navbar.jsx
│   │       ├── Navbar.scss
│   │       └── NavItem.jsx
│   ├── pages/
│   │   ├── AboutUs/
│   │   │   ├── AboutUs.jsx
│   │   │   └── AboutUs.scss
│   │   ├── Auth/
│   │   │   ├── SignIn.jsx
│   │   │   └── SignUp.jsx
│   │   ├── DetectDisease/
│   │   │   └── DetectDisease.jsx
│   │   ├── DiseasesList/
│   │   │   ├── DiseasesList.jsx
│   │   │   └── DiseasesList.scss
│   │   ├── History/
│   │   │   ├── History.jsx
│   │   │   └── History.scss
│   │   └── Home/
│   │       ├── CreateAccountBanner.jsx
│   │       ├── Home.jsx
│   │       ├── Home.css
│   │       ├── Overlay.jsx
│   │       └── Steps.jsx
│   └── services/
│       └── axiosInstance.js
```

## Installation and Setup

### Prerequisites

Ensure you have the following installed:

- Node.js (version 14.x or higher)
- npm (version 6.x or higher)

### Installation

1. Clone the repository to your local machine:

    ```sh
    git clone <repository-url>
    ```

2. Navigate to the project directory:

    ```sh
    cd PlantDiseaseDetector/frontend
    ```

3. Install the dependencies:

    ```sh
    npm install
    ```

### Running the Project

1. Start the project:

    ```sh
    npm start
    ```

2. Open your browser and go to:

    ```
    http://localhost:3000
    ```

## Components

### FormFileInput

File: `src/components/FormFileInput/FormFileInput.jsx`

A custom file input component for Formik forms.

#### Props

- `name`: The name of the input field.
- `accept`: The accepted file types.
- `label`: The label for the input field.
- `className`: Additional class names for the input field.
- `render`: Additional elements to render inside the input group.

### FormInput

File: `src/components/FormInput/FormInput.jsx`

A custom text input component for Formik forms.

#### Props

- `type`: The type of the input field.
- `name`: The name of the input field.
- `label`: The label for the input field.
- `placeholder`: The placeholder text for the input field.
- `className`: Additional class names for the input field.
- `render`: Additional elements to render inside the input group.

### FormSelect

File: `src/components/FormSelect/FormSelect.jsx`

A custom select input component for Formik forms.

#### Props

- `name`: The name of the input field.
- `options`: The options for the select input.
- `placeholder`: The placeholder text for the select input.
- `label`: The label for the select input.
- `className`: Additional class names for the select input.
- `search`: Whether to enable the search functionality.

### FormTextArea

File: `src/components/FormTextArea/FormTextArea.jsx`

A custom textarea component for Formik forms.

#### Props

- `name`: The name of the input field.
- `label`: The label for the textarea.
- `rows`: The number of rows for the textarea.
- `className`: Additional class names for the textarea.
- `disabled`: Whether the textarea is disabled.

### LoadingSpinner

File: `src/components/LoadingSpinner/LoadingSpinner.jsx`

A loading spinner component.

#### Props

- `className`: Additional class names for the spinner.

### DisplayHeader

File: `src/components/DisplayHeader/DisplayHeader.jsx`

A header component for displaying titles.

#### Props

- `firstText`: The first part of the text.
- `secondText`: The second part of the text.
- `size`: The size of the header.

## Layouts

### Footer

File: `src/layouts/Footer/Footer.jsx`

The footer layout component.

### Navbar

File: `src/layouts/Navbar/Navbar.jsx`

The navbar layout component.

## Pages

### Home

File: `src/pages/Home/Home.jsx`

The home page component.

### AboutUs

File: `src/pages/AboutUs/AboutUs.jsx`

The about us page component.

### Auth

#### SignIn

File: `src/pages/Auth/SignIn.jsx`

The sign-in page component.

#### SignUp

File: `src/pages/Auth/SignUp.jsx`

The sign-up page component.

### DetectDisease

File: `src/pages/DetectDisease/DetectDisease.jsx`

The detect disease page component.

### DiseasesList

File: `src/pages/DiseasesList/DiseasesList.jsx`

The diseases list page component.

### History

File: `src/pages/History/History.jsx`

The history page component.

## Services

### axiosInstance

File: `src/services/axiosInstance.js`

The Axios instance for making API requests.
