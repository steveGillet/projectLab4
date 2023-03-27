import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.imagenet_utils import preprocess_input

def load_image_and_preprocess(img_path, target_size=(64, 64)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

def predict_image(model_path, img_path):
    # Load and preprocess the image
    img_array = load_image_and_preprocess(img_path)

    # Load the model
    model = load_model(model_path)

    # Make predictions
    predictions = model.predict(img_array)

    # Print the prediction
    print("Prediction: ", np.argmax(predictions[0]))
    print(predictions)

if __name__ == "__main__":
    model_path = "cnn_model.h5"
    img_path = "right.jpg"

    predict_image(model_path, img_path)