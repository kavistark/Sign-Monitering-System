def training_data():
    import tensorflow as tf
    from keras.preprocessing.image import ImageDataGenerator
    from PIL import Image
    import numpy as np
    import os

    # Define the number of classes
    path = "Data"
    names = os.listdir(path)
    val=len(names)
    n = val
    print(n)

    # Define the model architecture
    model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(n, activation='softmax')
    ])

    # Compile the model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Preprocess the data
    train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
    train_generator = train_datagen.flow_from_directory("Data", target_size=(224, 224), batch_size= 32, class_mode='categorical')

    # Train the model
    model.fit(train_generator, epochs=15)

    # Save the model
    model.save('my_model.h5')

    # Create a dictionary mapping class indices to class names
    class_indices = train_generator.class_indices
    class_names = list(class_indices.keys())
    index_to_class = {v: k for k, v in class_indices.items()}

    # Save the index_to_class dictionary to a TXT file
    with open('label.txt', 'w') as f:
        for index, class_name in index_to_class.items():
            f.write(f"{index}:{class_name}\n")

    # Load the index_to_class dictionary from the TXT file
    with open('label.txt', 'r') as f:
        index_to_class = {}
        for line in f:
            index, class_name = line.strip().split(":")
            index_to_class[int(index)] = class_name

    # Create a function to predict class labels
    def predict(image_path):
        image = Image.open(image_path)
        image = image.resize((224, 224))
        image = np.asarray(image) / 255.0
        image = np.expand_dims(image, axis=0)
        predictions = model.predict(image)
        predicted_index = np.argmax(predictions)
        predicted_class = index_to_class[predicted_index]
        return predicted_class