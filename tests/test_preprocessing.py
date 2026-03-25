import pytest
from src.preprocessing import preprocess_image

def test_preprocess_image():
    # Test with a valid image path
    image_path = "tests/test_images/sample_image.jpg"  # Replace with a valid test image path
    processed_image = preprocess_image(image_path)
    assert processed_image is not None
    assert processed_image.shape == (224, 224, 3)  # Assuming the output shape is (224, 224, 3)

def test_preprocess_image_invalid_path():
    # Test with an invalid image path
    image_path = "invalid/path/to/image.jpg"
    with pytest.raises(FileNotFoundError):
        preprocess_image(image_path)

def test_preprocess_image_empty():
    # Test with an empty image path
    image_path = ""
    with pytest.raises(ValueError):
        preprocess_image(image_path)