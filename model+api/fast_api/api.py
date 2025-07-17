from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet_v2 import preprocess_input

import numpy as np
from PIL import Image
import io
# from starlette.responses import Response

from functions.model import load_keras_model
from functions.preprocessing import preprocess_for_resnet


app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins - substituir por origem específica ex.: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/predict")
async def predict_from_image(file: UploadFile = File(...)):
    # Lê a imagem enviada de forma assíncrona (sem travar a API)
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))

    # Pré-processamento (retorna array NumPy)
    processed_img = preprocess_for_resnet(img)

    # Predição
    # O Keras converte automaticamente para tensor internamente
    model = load_keras_model()
    assert model is not None
    prediction = model.predict(processed_img)

    return {"predicted_price": float(np.exp(prediction))}
