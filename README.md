# Plant Disease Detector

Проект "Plant Disease Detector" предназначен для выявления заболеваний растений с использованием распознавания изображений и предоставления пользователям рекомендаций по лечению и профилактике. Пользователи могут загружать изображения растений, и система проанализирует их, определит возможные заболевания и предоставит подробную информацию о проблеме и её решении.

## Особенности
- **Обнаружение заболеваний**: Загрузка изображений растений для определения заболеваний с использованием обученной модели машинного обучения.
- **Рекомендации по лечению**: Получение инструкций по уходу, предложений по удобрениям и мерам профилактики.
- **Карта сада**: Визуализация схемы сада и анализ взаимосвязей между соседними растениями.
- **Автоматизация**: Поддержка подключения камер для автоматической загрузки изображений.

## Технологический стек
- **Frontend**: Интерфейс пользователя на основе React для загрузки изображений и отображения результатов.
- **Backend**: Python (FastAPI/Django) для обработки API-запросов, обработки изображений и взаимодействия с моделью машинного обучения.
- **Машинное обучение**: Модель на основе TensorFlow/PyTorch для распознавания заболеваний.
- **База данных**: PostgreSQL для хранения данных о болезнях, пользователях и схемах сада.
- **Хранилище**: S3/MinIO для сохранения загруженных изображений.

## Структура проекта
```
project_root/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadForm.js
│   │   │   ├── ResultView.js
│   │   │   ├── GardenMap.js
│   │   └── App.js
│   ├── package.json
│   ├── webpack.config.js
│   └── README.md
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── disease_model.py
│   │   │   ├── user.py
│   │   │   └── garden.py
│   │   ├── routes/
│   │   │   ├── image_analysis.py
│   │   │   ├── recommendations.py
│   │   │   └── garden.py
│   │   ├── schemas/
│   │   │   ├── disease.py
│   │   │   ├── user.py
│   │   │   └── garden.py
│   │   ├── database.py
│   │   └── config.py
│   ├── requirements.txt
│   └── README.md
├── ml_model/
│   ├── train/
│   │   ├── preprocess.py
│   │   ├── train.py
│   │   ├── dataset.py
│   │   └── utils.py
│   ├── inference/
│   │   ├── predict.py
│   │   └── model_export.py
│   ├── models/
│   │   └── trained_model.onnx
│   └── README.md
├── docker/
│   ├── docker-compose.yml
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── README.md
├── docs/
│   ├── architecture.md
│   ├── api_specification.md
│   └── README.md
└── README.md
```

## Установка

### Требования
- Docker
- Node.js
- Python 3.8+

### Шаги
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-repo/plant-disease-detector.git
   cd plant-disease-detector
   ```

2. Постройте и запустите сервисы с использованием Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Откройте приложение:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)

## Использование
1. Загрузите изображение растения через интерфейс.
2. Просмотрите результаты анализа и рекомендации по лечению.
3. Используйте карту сада для управления вашими растениями и их здоровьем.

## Лицензия
Этот проект лицензируется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

## Контакты
Для вопросов или поддержки пишите на khnartem@gmail.com.
