import pytest
from unittest.mock import patch, MagicMock, mock_open
import torch # Нужен для torch.device и других типов torch
import torchvision.transforms as transforms # Для сравнения объекта transforms

from app.services.model_service import ModelService

@pytest.fixture
def model_service_instance():
    """Возвращает экземпляр ModelService для каждого теста."""
    return ModelService()

class TestModelService:

    def test_initialization(self, model_service_instance: ModelService):
        """Тестирует начальное состояние атрибутов."""
        assert model_service_instance.model is None
        assert model_service_instance.device is None
        assert model_service_instance.class_names is None
        assert model_service_instance.transforms is None

    @patch('app.services.model_service.json.load')
    @patch('app.services.model_service.open', new_callable=mock_open, read_data='{"0": "class_a", "1": "class_b"}')
    @patch('app.services.model_service.torch.load')
    @patch('app.services.model_service.torch.cuda.is_available')
    @patch('app.services.model_service.models.resnet50')
    @patch('app.services.model_service.nn.Linear') # Мокаем nn.Linear
    def test_load_model_cpu(
        self,
        mock_nn_linear: MagicMock,
        mock_resnet50: MagicMock,
        mock_cuda_is_available: MagicMock,
        mock_torch_load: MagicMock,
        mock_file_open: MagicMock,
        mock_json_load: MagicMock,
        model_service_instance: ModelService
    ):
        """Тестирует load_model с использованием CPU."""
        mock_cuda_is_available.return_value = False # Имитируем отсутствие CUDA

        # Настройка моков для resnet50 и его атрибутов
        mock_model_instance = MagicMock()
        mock_model_instance.fc.in_features = 2048 # Примерное значение
        mock_resnet50.return_value = mock_model_instance
        
        # Настройка мока для nn.Linear
        mock_linear_layer = MagicMock()
        mock_nn_linear.return_value = mock_linear_layer

        # Настройка мока для json.load - КЛЮЧИ ДОЛЖНЫ БЫТЬ СТРОКАМИ, как в JSON
        expected_class_names_from_json = {"0": "class_a", "1": "class_b"}
        mock_json_load.return_value = expected_class_names_from_json
        
        # ИСПРАВЛЕНИЕ: mock_model_instance.to() должен возвращать сам себя (или настроенный мок)
        # чтобы последующие операции, такие как .eval() или доступ к .fc, работали на ожидаемом объекте
        mock_model_after_to = MagicMock()
        mock_model_instance.to.return_value = mock_model_after_to
        # Также, load_state_dict вызывается на mock_model_instance, а не на результате .to()
        # .eval() вызывается на результате .to()

        # Вызов тестируемого метода
        model_service_instance.load_model()

        # Проверки
        mock_resnet50.assert_called_once_with(pretrained=False)
        # model_service_instance.model теперь это mock_model_after_to
        # а mock_model_instance.fc был заменен на mock_linear_layer
        assert mock_model_instance.fc == mock_linear_layer # Проверяем, что fc у *исходного* мока модели был заменен
        mock_nn_linear.assert_called_once_with(2048, 38)


        mock_torch_load.assert_called_once_with(
            "ml_model/Best-Resnet50-from-scratch-with-New-Plant-Disease.pth",
            map_location=torch.device("cpu"),
        )
        mock_model_instance.load_state_dict.assert_called_once_with(mock_torch_load.return_value)
        
        assert model_service_instance.device == torch.device("cpu")
        mock_model_instance.to.assert_called_once_with(torch.device("cpu"))
        # model_service_instance.model это результат .to(), на нем вызывается .eval()
        assert model_service_instance.model == mock_model_after_to
        mock_model_after_to.eval.assert_called_once()


        # Проверка transforms
        assert isinstance(model_service_instance.transforms, transforms.Compose)

        mock_file_open.assert_called_once_with("ml_model/class_disease.json", "r", encoding="utf-8")
        mock_json_load.assert_called_once_with(mock_file_open.return_value)
        assert model_service_instance.class_names == expected_class_names_from_json

    @patch('app.services.model_service.json.load')
    @patch('app.services.model_service.open', new_callable=mock_open, read_data='{"0": "class_a", "1": "class_b"}')
    @patch('app.services.model_service.torch.load')
    @patch('app.services.model_service.torch.cuda.is_available')
    @patch('app.services.model_service.models.resnet50')
    @patch('app.services.model_service.nn.Linear')
    def test_load_model_cuda(
        self,
        mock_nn_linear: MagicMock,
        mock_resnet50: MagicMock,
        mock_cuda_is_available: MagicMock,
        mock_torch_load: MagicMock,
        mock_file_open: MagicMock,
        mock_json_load: MagicMock,
        model_service_instance: ModelService
    ):
        """Тестирует load_model с использованием CUDA, если доступно."""
        mock_cuda_is_available.return_value = True # Имитируем наличие CUDA

        mock_model_instance = MagicMock()
        mock_model_instance.fc.in_features = 2048
        mock_resnet50.return_value = mock_model_instance
        
        mock_linear_layer = MagicMock()
        mock_nn_linear.return_value = mock_linear_layer

        expected_class_names_from_json = {"0": "class_a", "1": "class_b"}
        mock_json_load.return_value = expected_class_names_from_json
        
        mock_model_after_to = MagicMock()
        mock_model_instance.to.return_value = mock_model_after_to

        model_service_instance.load_model()

        mock_resnet50.assert_called_once_with(pretrained=False)
        assert mock_model_instance.fc == mock_linear_layer
        mock_nn_linear.assert_called_once_with(2048, 38)


        mock_torch_load.assert_called_once_with(
            "ml_model/Best-Resnet50-from-scratch-with-New-Plant-Disease.pth",
            map_location=torch.device("cpu"), 
        )
        mock_model_instance.load_state_dict.assert_called_once_with(mock_torch_load.return_value)
        
        assert model_service_instance.device == torch.device("cuda")
        mock_model_instance.to.assert_called_once_with(torch.device("cuda")) 
        assert model_service_instance.model == mock_model_after_to
        mock_model_after_to.eval.assert_called_once()

        assert isinstance(model_service_instance.transforms, transforms.Compose)
        mock_file_open.assert_called_once_with("ml_model/class_disease.json", "r", encoding="utf-8")
        mock_json_load.assert_called_once_with(mock_file_open.return_value)
        assert model_service_instance.class_names == expected_class_names_from_json

    # Далее будут тесты для predict()
    @patch('app.services.model_service.Image.open')
    @patch('app.services.model_service.torch.max') # Мокаем torch.max
    def test_predict_success(
        self,
        mock_torch_max: MagicMock,
        mock_image_open: MagicMock,
        model_service_instance: ModelService
    ):
        """Тестирует успешное предсказание."""
        # Подготовка моков и данных для predict
        model_service_instance.model = MagicMock()
        model_service_instance.device = torch.device("cpu")
        model_service_instance.transforms = MagicMock(spec=transforms.Compose)
        
        model_service_instance.class_names = ["Болезнь А", "Болезнь Б", "Болезнь В"]

        mock_pil_image = MagicMock()
        mock_image_open.return_value.convert.return_value = mock_pil_image

        mock_input_tensor = MagicMock(spec=torch.Tensor) 
        mock_transformed_image = MagicMock()
        mock_unsqueezed_image = MagicMock()
        model_service_instance.transforms.return_value = mock_transformed_image
        mock_transformed_image.unsqueeze.return_value = mock_unsqueezed_image
        mock_unsqueezed_image.to.return_value = mock_input_tensor
        
        mock_output_tensor = MagicMock(spec=torch.Tensor) 
        model_service_instance.model.return_value = mock_output_tensor

        mock_predicted_indices = MagicMock(spec=torch.Tensor)
        predicted_index_int = 1 # Имитируем, что предсказан индекс 1
        mock_predicted_indices.item.return_value = predicted_index_int
        mock_torch_max.return_value = (MagicMock(), mock_predicted_indices)

        image_path = "dummy/path/to/image.jpg"
        
        # Вызов метода predict
        result = model_service_instance.predict(image_path)

        # Проверки
        mock_image_open.assert_called_once_with(image_path)
        mock_image_open.return_value.convert.assert_called_once_with("RGB")
        
        model_service_instance.transforms.assert_called_once_with(mock_pil_image)
        mock_transformed_image.unsqueeze.assert_called_once_with(0)
        mock_unsqueezed_image.to.assert_called_once_with(model_service_instance.device)
        
        model_service_instance.model.assert_called_once_with(mock_input_tensor)
        mock_torch_max.assert_called_once_with(mock_output_tensor, 1)
        mock_predicted_indices.item.assert_called_once()
        
        # Ожидаем класс по индексу 1 из списка
        assert result == model_service_instance.class_names[predicted_index_int] # "Болезнь Б"