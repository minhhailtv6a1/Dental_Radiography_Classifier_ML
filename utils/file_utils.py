def save_uploaded_file(uploaded_file, destination):
    with open(destination, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return destination

def load_image(image_path):
    from PIL import Image
    return Image.open(image_path)

def save_image(image, destination):
    image.save(destination)