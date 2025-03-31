# 🔹 Importamos FastAPI para crear la API
from fastapi import FastAPI, File, UploadFile

# 🔹 Importamos TensorFlow y las funciones necesarias para usar MobileNetV2
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

# 🔹 Importamos otras librerías necesarias
import numpy as np               # Para manejar arrays numéricos
from PIL import Image            # Para manejar imágenes con PIL
import io                        # Para manejar flujos de datos en memoria
import base64                    # Para codificar la imagen en base64 y enviarla al frontend

# 🔹 Importamos middleware CORS para permitir solicitudes desde el frontend
from fastapi.middleware.cors import CORSMiddleware

# 🔹 Definir la aplicación FastAPI
app = FastAPI()

# 🔹 Agregar middleware CORS para permitir peticiones desde el frontend (evita problemas de CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],  # Define qué dominios pueden acceder a la API
    allow_credentials=True,                   # Permite credenciales en las solicitudes (cookies, autenticación, etc.)
    allow_methods=["*"],                       # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],                       # Permite todos los encabezados HTTP
)

# 🔹 Inicializar el modelo MobileNetV2 preentrenado con pesos de ImageNet
model = MobileNetV2(weights="imagenet")

# 🔹 Función para clasificar la imagen
def classify_image(img_bytes):
    # 🔹 Cargar la imagen desde los bytes
    img = Image.open(io.BytesIO(img_bytes))

    # 🔹 Redimensionar la imagen a 224x224 (tamaño requerido por MobileNetV2)
    img = img.resize((224, 224))

    # 🔹 Convertir la imagen a un array de numpy
    x = image.img_to_array(img)

    # 🔹 Agregar una dimensión extra para que tenga la forma (1, 224, 224, 3)
    x = np.expand_dims(x, axis=0)

    # 🔹 Preprocesar la imagen según lo requerido por MobileNetV2
    x = preprocess_input(x)

    # 🔹 Hacer la predicción con el modelo
    preds = model.predict(x)

    # 🔹 Decodificar las predicciones en etiquetas legibles
    decoded = decode_predictions(preds, top=3)[0]  # Obtener las 3 mejores predicciones

    # 🔹 Formatear los resultados en un diccionario
    return [{"label": label, "probability": float(prob) * 100} for (_, label, prob) in decoded]

# 🔹 Endpoint para clasificar una imagen
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # 🔹 Leer la imagen subida por el usuario en formato bytes
    img_bytes = await file.read()

    # 🔹 Convertir la imagen a Base64 para enviarla al frontend
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    # 🔹 Obtener las predicciones de la imagen
    predictions = classify_image(img_bytes)

    # 🔹 Retornar la imagen en base64 y las predicciones
    return {
        "image": img_base64,  # Imagen en formato base64 para mostrar en el frontend
        "predictions": predictions  # Lista de predicciones con probabilidades
    }

# 🔹 Endpoint raíz para verificar que la API
