from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import io

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load the model
model = tf.keras.models.load_model("model/initial_model.h5")

# All 38 plant diseases
class_labels = [
    'Apple Scab',                        # 0
    'Apple Black Rot',                   # 1
    'Apple Cedar Apple Rust',            # 2
    'Healthy Apple',                     # 3
    'Healthy Blueberry',                 # 4
    'Cherry Powdery Mildew',             # 5
    'Healthy Cherry',                    # 6
    'Corn Cercospora Leaf Spot',         # 7
    'Corn Common Rust',                  # 8
    'Corn Northern Leaf Blight',         # 9
    'Healthy Corn',                      # 10
    'Grape Black Rot',                   # 11
    'Grape Esca (Black Measles)',        # 12
    'Grape Leaf Blight',                 # 13
    'Healthy Grape',                     # 14
    'Orange Haunglongbing (Citrus Greening)', # 15
    'Peach Bacterial Spot',              # 16
    'Healthy Peach',                     # 17
    'Pepper Bell Bacterial Spot',        # 18
    'Healthy Pepper Bell',               # 19
    'Potato Early Blight',               # 20
    'Potato Late Blight',                # 21
    'Healthy Potato',                    # 22
    'Healthy Raspberry',                 # 23
    'Healthy Soybean',                   # 24
    'Squash Powdery Mildew',             # 25
    'Strawberry Leaf Scorch',            # 26
    'Healthy Strawberry',                # 27
    'Tomato Bacterial Spot',             # 28
    'Tomato Early Blight',               # 29
    'Tomato Late Blight',                # 30
    'Tomato Leaf Mold',                  # 31
    'Tomato Septoria Leaf Spot',         # 32
    'Tomato Spider Mites (Two-spotted)', # 33
    'Tomato Target Spot',                # 34
    'Tomato Yellow Leaf Curl Virus',     # 35
    'Tomato Mosaic Virus',               # 36
    'Healthy Tomato'                     # 37
]


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    print("Received an image")
    # Read the image file uploaded by the user
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes))

    # Preprocess the image
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Make predictions
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    predicted_label = class_labels[predicted_class]
    confidence = predictions[0][predicted_class]

    return {"predicted_class": predicted_label, "confidence": float(confidence)}

