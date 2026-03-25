# Dental Radiography Classifier

This project is a web application designed to classify dental radiographs using a trained machine learning model. The application is built with Streamlit and provides an intuitive interface for users to upload images and receive classification results.

## Project Structure

```
dental-radiography-streamlit
├── streamlit_app.py          # Main entry point for the Streamlit application
├── requirements.txt          # List of dependencies for the project
├── README.md                 # Documentation for the project
├── .gitignore                # Files and directories to ignore by Git
├── .streamlit
│   └── config.toml          # Configuration settings for the Streamlit application
├── models
│   ├── lightgbm_model.pkl    # Trained LightGBM model for classification
│   └── scaler.pkl            # Scaler for preprocessing input data
├── src
│   ├── __init__.py           # Marks the src directory as a Python package
│   ├── inference.py          # Functions for loading the model and making predictions
│   ├── preprocessing.py       # Functions for preprocessing input images
│   ├── features.py           # Functions for extracting features from images
│   └── ui.py                 # User interface components for the Streamlit application
├── components
│   └── uploader.py           # Custom file uploader component for the application
├── utils
│   └── file_utils.py         # Utility functions for file operations
├── notebooks
│   └── explore.ipynb         # Jupyter notebook for exploratory data analysis
├── tests
│   ├── test_inference.py      # Unit tests for inference functions
│   └── test_preprocessing.py   # Unit tests for preprocessing functions
├── docker
│   └── Dockerfile            # Instructions for building a Docker image
└── docs
    └── design.md             # Design documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd dental-radiography-streamlit
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```
   streamlit run streamlit_app.py
   ```

## Usage Guidelines

- Upload dental radiographs in supported formats (PNG, JPG, JPEG, BMP, GIF, TIFF, WEBP).
- The model will classify the images into categories: Cavity, Fillings, Impacted Tooth, Implant, or Normal.
- Ensure that the images are clear and centered for best accuracy.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.