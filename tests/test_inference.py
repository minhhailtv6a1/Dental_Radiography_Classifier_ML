import pytest
from src.inference import load_model, predict

def test_load_model():
    model = load_model('models/lightgbm_model.pkl')
    assert model is not None, "Model should be loaded successfully"

def test_predict():
    model = load_model('models/lightgbm_model.pkl')
    sample_input = [[0.5, 0.2, 0.1]]  # Replace with appropriate sample input
    prediction = predict(model, sample_input)
    assert prediction in ['Cavity', 'Fillings', 'Impacted Tooth', 'Implant', 'Normal'], "Prediction should be one of the valid categories"