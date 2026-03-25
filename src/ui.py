from streamlit import st
from components.uploader import file_uploader
from src.inference import classify_image

def main():
    st.title("Dental Radiography Classifier")
    st.write("Upload a dental X-ray image to classify it into categories such as Cavity, Fillings, Impacted Tooth, Implant, or Normal.")

    # File uploader
    uploaded_file = file_uploader("Choose a dental X-ray image...", type=["png", "jpg", "jpeg", "bmp", "gif", "tiff", "webp"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        # Classify the image
        if st.button("Classify Image"):
            result = classify_image(uploaded_file)
            st.write("Prediction:", result)

if __name__ == "__main__":
    main()