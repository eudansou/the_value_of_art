from tensorflow.keras.models import load_model
from google.cloud import storage
import os


def load_keras_model():
    """Carrega modelo Keras"""
    client = storage.Client()
    blobs = list(client.get_bucket('the_value_of_art').list_blobs(prefix="CNN"))
    latest_blob = max(blobs, key=lambda x: x.updated)
    latest_model_path_to_save = os.path.join(latest_blob.name)
    latest_blob.download_to_filename(latest_model_path_to_save)

    latest_model = load_model(latest_model_path_to_save)

    print("✅ Latest model downloaded from cloud storage")

    return latest_model
