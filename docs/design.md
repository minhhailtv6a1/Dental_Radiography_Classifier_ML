# Design Documentation for Dental Radiography Classifier

## Overview
The Dental Radiography Classifier is a web application designed to classify dental X-ray images into various categories such as Cavity, Fillings, Impacted Tooth, Implant, and Normal. The application leverages machine learning techniques, specifically using a LightGBM model for classification.

## Architecture
The application is structured into several key components:

1. **Streamlit Application**: The main entry point of the application is `streamlit_app.py`, which sets up the user interface and handles interactions.

2. **Model and Preprocessing**:
   - **Models**: The trained LightGBM model (`lightgbm_model.pkl`) and the scaler (`scaler.pkl`) are stored in the `models` directory.
   - **Preprocessing**: The `src/preprocessing.py` file contains functions to preprocess the input images, ensuring they are in the correct format for the model.

3. **Feature Extraction**: The `src/features.py` file is responsible for extracting relevant features from the images that will be used for classification.

4. **Inference**: The `src/inference.py` file includes functions to load the model and make predictions based on the preprocessed input data.

5. **User Interface**: The `src/ui.py` file manages the layout and display elements of the Streamlit application, providing a user-friendly experience.

6. **File Uploading**: The `components/uploader.py` file contains a custom file uploader component that allows users to upload their dental radiographs easily.

7. **Utilities**: The `utils/file_utils.py` file provides utility functions for handling file operations, such as saving and loading images.

## Design Decisions
- **Framework Choice**: Streamlit was chosen for its simplicity and effectiveness in building interactive web applications quickly, especially for data science projects.
- **Model Selection**: LightGBM was selected due to its efficiency and performance in handling large datasets, making it suitable for image classification tasks.
- **Modular Structure**: The project is organized into distinct modules (src, components, utils) to promote code reusability and maintainability.

## Future Enhancements
- **User Authentication**: Implementing user authentication to allow users to save their results and access them later.
- **Model Improvement**: Continuously improving the model by retraining it with new data and exploring other machine learning algorithms.
- **Deployment**: Creating a Docker container for easy deployment and scalability of the application.

## Conclusion
This design document outlines the architecture and design decisions made for the Dental Radiography Classifier application. The modular approach and choice of technologies aim to create a robust and user-friendly application for dental radiography classification.