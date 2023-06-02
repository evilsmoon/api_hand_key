import mediapipe as mp
import os
import cv2
import base64
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity
import math


def reescale_image(b64_image):
    image_bytes = base64.b64decode(b64_image)
    
    # Convertir los bytes en un array NumPy
    image_array = np.frombuffer(image_bytes, np.uint8)
    
    # Decodificar el array NumPy en una imagen OpenCV
    imagen = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    clase_manos  =  mp.solutions.hands
    manos = clase_manos.Hands()
    # dibujo = mp.solutions.drawing_utils

    # img = cv2.imread("imagen_gabo1.jpeg")
    img_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    copia = imagen.copy()

    resultado = manos.process(img_rgb)
    posiciones = []

    for mano in resultado.multi_hand_landmarks:
        for id, lm in enumerate(mano.landmark): 
            alto, ancho, c = imagen.shape  
            corx, cory = int(lm.x*ancho), int(lm.y*alto)
            posiciones.append([id,corx,cory])

        if len(posiciones) != 0:
            pto_4 = posiciones[4] #5 Dedos: 4 | 0 Dedos: 3 | 1 Dedo: 2 | 2 Dedos: 3 | 3 Dedos: 4 | 4 Dedos: 8
            pto_20 = posiciones[20]#5 Dedos: 20| 0 Dedos: 17| 1 Dedo: 17| 2 Dedos: 20| 3 Dedos: 20| 4 Dedos: 20
            pto_12 = posiciones[12]#5 Dedos: 12| 0 Dedos: 10 | 1 Dedo: 20|2 Dedos: 16| 3 Dedos: 12| 4 Dedos: 12
            pto_0 = posiciones[0] #5 Dedos: 0 | 0 Dedos: 0 | 1 Dedo: 0 | 2 Dedos: 0 | 3 Dedos: 0 | 4 Dedos: 0
            
            if(pto_20[1] < pto_4[1] ): #palma
                print('palma')
                x1, y1 = (pto_20[1] - 50), (pto_12[2] - 50)
                x2, y2 = (pto_4[1] + 50), (pto_0[2] + 50)
            else: #reverso
                print('reverso')
                x1, y1 = (pto_4[1] - 50), (pto_12[2] - 50)
                x2, y2 = (pto_20[1] + 50), (pto_0[2] + 50)
            
            dedos_reg = copia[y1:y2, x1:x2]
            dedos = cv2.resize(dedos_reg,(200,200), interpolation = cv2.INTER_CUBIC)
            # cv2.imwrite("prueba_gabo1.jpg",dedos)
            return dedos


        
def extrart_feateres(b64_image,model_path):

    model = InceptionV3(weights='imagenet', include_top=False)

    image = reescale_image(b64_image)
    query_image_array = np.expand_dims(image, axis=0)
    query_image_array = preprocess_input(query_image_array)

    # Extraer características de la imagen de consulta utilizando el modelo InceptionV3
    query_features = model.predict(query_image_array)
    query_features = np.ndarray.flatten(query_features)

    # Cargar el conjunto de imágenes
    # image_set_path = "Gabriel_imagenes.npy"
    image_set = np.load(model_path)

    # Extraer características del conjunto de imágenes utilizando el modelo InceptionV3
    image_set_features = []
    for img in image_set:
        img_array = np.expand_dims(img, axis=0)
        img_array = preprocess_input(img_array)
        features = model.predict(img_array)
        features = np.ndarray.flatten(features)
        image_set_features.append(features)
    image_set_features = np.array(image_set_features)

    # Calcular la similitud utilizando la correlación de coseno
    similarity_scores = cosine_similarity(query_features.reshape(1, -1), image_set_features)

    # Obtener los porcentajes de similitud
    similarity_percentages = similarity_scores[0] * 100

    # Obtener los índices de las imágenes más similares
    most_similar_indices = np.argsort(similarity_percentages)[::-1]

    # Obtener los porcentajes de similitud más altos y las imágenes correspondientes
    most_similar_percentages = similarity_percentages[most_similar_indices]
    most_similar_images = image_set[most_similar_indices]

    # Imprimir los resultados
    print(f"Porcentaje de similitud: {most_similar_percentages[np.argmax(most_similar_percentages)]}")
    similar_percentage = round(most_similar_percentages[np.argmax(most_similar_percentages)],4)
    if (similar_percentage >= 50):
        return True
    else:
        return False

