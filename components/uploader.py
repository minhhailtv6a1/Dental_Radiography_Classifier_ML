from io import BytesIO
import streamlit as st


def upload_image(label: str = "Choose an image...", type: list | None = None):
    """Show a Streamlit file uploader and return the uploaded file-like object or None.

    The returned object is the Streamlit `UploadedFile` and is compatible with
    `src.inference.classify_image` which expects a file-like object with
    either a `save()` method or readable bytes.
    """
    if type is None:
        type = ["png", "jpg", "jpeg", "bmp", "gif", "tiff", "webp"]

    uploaded_file = st.file_uploader(label, type=type)

    if uploaded_file is not None:
        # Do not read or consume the file here — return it so caller can use it
        return uploaded_file

    return None