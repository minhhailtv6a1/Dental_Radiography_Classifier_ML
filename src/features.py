import os
import tempfile
import numpy as np
import matplotlib.image as mpimg
from skimage.transform import resize
from skimage.feature import hog
import io
from PIL import Image


def extract_features_from_image(image_file, target_size=(64, 64)):
    """Extract features from an uploaded file-like object.

    Returns a numpy array shaped (1, n_features) or None on failure.
    """
    tmp_path = None
    try:
        # Preserve original file extension if provided
        original_filename = getattr(image_file, 'filename', None) or getattr(image_file, 'name', None) or 'upload.png'
        file_ext = os.path.splitext(original_filename)[1] or '.png'

        # Try to read bytes via file-like interface (Streamlit UploadedFile / Flask FileStorage)
        img = None
        try:
            # Reset pointer when possible and read bytes
            if hasattr(image_file, 'seek'):
                try:
                    image_file.seek(0)
                except Exception:
                    pass
            if hasattr(image_file, 'read'):
                data = image_file.read()
                # If reading returned bytes-like, use PIL to open
                if isinstance(data, (bytes, bytearray)) and len(data) > 0:
                    img_pil = Image.open(io.BytesIO(data)).convert('RGB')
                    img = np.array(img_pil)
        except Exception:
            img = None

        # Fallback: save to a temporary file and read with matplotlib
        if img is None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                if hasattr(image_file, 'save'):
                    image_file.save(tmp_file.name)
                else:
                    # If we already read data above, write it; otherwise read again
                    try:
                        if 'data' in locals() and isinstance(data, (bytes, bytearray)):
                            tmp_file.write(data)
                        else:
                            # Attempt to read from the stream again
                            try:
                                image_file.seek(0)
                            except Exception:
                                pass
                            tmp_file.write(image_file.read())
                    except Exception:
                        pass
                tmp_path = tmp_file.name
            img = mpimg.imread(tmp_path)

        # At this point `img` should be a numpy array
        if img is None:
            return None

        # Normalize to [0, 1] if needed
        if img.dtype != np.float32 and img.dtype != np.float64:
            # Convert integer images to float in [0,1]
            if img.max() > 1.0:
                img = img.astype(float) / 255.0

        # Convert to grayscale if RGB
        if img.ndim == 3:
            img_gray = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
        else:
            img_gray = img

        # Resize image
        img_resized = resize(img_gray, target_size, anti_aliasing=True)

        # Extract HOG features
        features_hog = hog(img_resized, pixels_per_cell=(8, 8),
                           cells_per_block=(2, 2), feature_vector=True)

        # Statistical features
        mean_intensity = np.mean(img_resized)
        std_intensity = np.std(img_resized)

        # Combine features
        feature_vector = np.concatenate([features_hog, [mean_intensity, std_intensity]])

        # Cleanup
        try:
            if tmp_path is not None:
                os.unlink(tmp_path)
        except Exception:
            pass

        if np.isnan(feature_vector).any():
            # Return None to indicate failure to upstream callers
            return None

        return feature_vector.reshape(1, -1)

    except Exception:
        try:
            if tmp_path is not None:
                os.unlink(tmp_path)
        except Exception:
            pass
        return None


def preprocess_image(image):
    """Compatibility wrapper: returns the image unchanged (kept for API parity)."""
    return image


def get_image_features(image_file):
    """High-level wrapper to get features from an uploaded file-like object."""
    return extract_features_from_image(image_file)