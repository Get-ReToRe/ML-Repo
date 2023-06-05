import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical


data_path = "path_ke_folder_gambar"


data = []
labels = []


categories = ['Budaya', 'Taman Hiburan', 'Bahari', 'Cagar Alam', 'Pusat Perbelanjaan']


for category in categories:
    folder_path = os.path.join(data_path, category)
    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)
        image = cv2.imread(img_path)
        image = cv2.resize(image, (150, 150)) 
        data.append(image)
        labels.append(category)


data = np.array(data)
labels = np.array(labels)


label_encoder = LabelEncoder()
labels = to_categorical(label_encoder.fit_transform(labels))


train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.2, random_state=42)


train_data = train_data.astype('float32') / 255
test_data = test_data.astype('float32') / 255


model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dense(len(categories), activation='softmax'))


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_data, train_labels, epochs=10, batch_size=32, validation_data=(test_data, test_labels))


model.save("model_tempat_wisata.h5")
