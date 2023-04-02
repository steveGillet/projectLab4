import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define the CNN architecture
model = keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(3, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Create data generators for training and validation
train_datagen = ImageDataGenerator(rescale=1.0/255,
                                   shear_range=0,
                                   zoom_range=0.2,
                                   horizontal_flip=False)

test_datagen = ImageDataGenerator(rescale=1.0/255)

train_generator = train_datagen.flow_from_directory(
        'train/',
        target_size=(64, 64),
        batch_size=32,
        color_mode='grayscale', # set color_mode to grayscale
        class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
        'validation/',
        target_size=(64, 64),
        batch_size=32,
        color_mode='grayscale', # set color_mode to grayscale
        class_mode='categorical')

# Train the model
model.fit(
        train_generator,
        epochs=60,
        validation_data=validation_generator)

# Save the trained model
model.save('cnn_model.h5')
