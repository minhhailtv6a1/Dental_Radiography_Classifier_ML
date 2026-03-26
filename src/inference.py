import os
import joblib
import numpy as np
import traceback
from typing import Optional, Tuple, Any

from .features import extract_features_from_image

# Encoding/decoding masks (kept consistent with the Flask app)
ENCODE_MASK = {
    "Cavity": 0,
    "Fillings": 1,
    "Impacted Tooth": 2,
    "Implant": 3,
    "Normal": 4,
}
DECODE_MASK = {v: k for k, v in ENCODE_MASK.items()}


def load_model(model_path: str):
    """Load a trained model from disk."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return joblib.load(model_path)


def load_scaler(scaler_path: str):
    """Load a fitted scaler from disk."""
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler file not found: {scaler_path}")
    return joblib.load(scaler_path)


def predict_from_features(features: np.ndarray, model: Any, scaler: Any) -> Tuple[int, str]:
    """Scale features and predict label (returns (encoded, decoded))."""
    if features is None:
        raise ValueError("Features array is None")
    scaled = scaler.transform(features)
    pred = model.predict(scaled)[0]
    label = DECODE_MASK.get(int(pred), "Unknown")
    return int(pred), label


def classify_image(uploaded_file, model: Optional[Any] = None, scaler: Optional[Any] = None,
                   model_path: str = 'models/XGBoost_encodeClass.pkl',
                   scaler_path: str = 'models/scaler.pkl') -> dict:
    """High-level helper to classify an uploaded file-like object.

    Returns a dict: {'prediction': decoded_label, 'encoded_value': int}
    """
    try:
        # Extract raw features using the features module
        raw_features = extract_features_from_image(uploaded_file)
        if raw_features is None:
            return {'error': 'Failed to extract features from image'}

        # Load model/scaler if not provided
        if scaler is None:
            scaler = load_scaler(scaler_path)
        if model is None:
            model = load_model(model_path)

        encoded, decoded = predict_from_features(raw_features, model, scaler)
        return {'prediction': decoded, 'encoded_value': encoded}

    except Exception as exc:
        traceback.print_exc()
        return {'error': str(exc)}


# Backwards-compatible predict function signature used by some tests
def predict(image_array: np.ndarray, model: Any, scaler: Any) -> Any:
    """Predict from a preprocessed image array (flattened or feature array).

    If image_array looks like raw image pixels, it is flattened and scaled.
    """
    arr = np.array(image_array)
    # Ensure 2D shape (1, n)
    if arr.ndim == 1:
        features = arr.reshape(1, -1)
    elif arr.ndim == 2:
        features = arr
    else:
        features = arr.reshape(1, -1)

    encoded, decoded = predict_from_features(features, model, scaler)
    return decoded