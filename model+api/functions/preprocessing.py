import tensorflow as tf
from tensorflow.keras.applications.resnet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image as keras_image_preprocessing

import numpy as np
from PIL import Image

def preprocess_for_resnet(image: Image.Image) -> np.ndarray:
    """Pré-processamento específico para ResNet50V2"""
    image = image.resize((224, 224))
    img_array = keras_image_preprocessing.img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    # img_array = np.array(image)
    return preprocess_input(img_array)
