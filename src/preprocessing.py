from PIL import Image
import numpy as np

def load_image(image_path):
    """Load an image from the specified path."""
    image = Image.open(image_path)
    return image

def preprocess_image(image, target_size=(224, 224)):
    """Preprocess the image for model input."""
    image = image.resize(target_size)
    image_array = np.array(image) / 255.0  # Normalize to [0, 1]
    return image_array

def normalize_image(image_array):
    """Normalize the image array."""
    return (image_array - np.mean(image_array)) / np.std(image_array)

def preprocess_and_normalize(image_path):
    """Load, preprocess, and normalize the image."""
    image = load_image(image_path)
    preprocessed_image = preprocess_image(image)
    normalized_image = normalize_image(preprocessed_image)
    return normalized_image