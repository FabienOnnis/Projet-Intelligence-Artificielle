import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dropout, Flatten
from keras.layers import Dense

import os
import cv2
from tqdm import tqdm

# labels = ['Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___healthy', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_mosaic_virus', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus']

labels = ['Tomato___Bacterial_spot']

IMG_SIZE = 256

# load all the images
def DataLoading(DIR):
    X = []
    Y = []
    for label in labels:
        path = os.path.join(DIR, label)
        class_num = labels.index(label)
        print(label)
        list_img = os.listdir(path)
        SelectedData = np.arange(len(list_img))
        SelectedData = np.random.choice(SelectedData, 500)
        new_list_img = [list_img[elem] for elem in SelectedData]
        for img in new_list_img:
            try:
                arr = cv2.imread(os.path.join(path, img), cv2.IMREAD_COLOR)
                resized_arr = cv2.resize(arr, (IMG_SIZE, IMG_SIZE))
                X.append(resized_arr)
                Y.append(class_num)
            except Exception as e:
                print(str(e) + '\n')
    return (np.array(X), np.array(Y))

def HistoryPlot(history):
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend(['Train', 'Val'], loc = 'upper left')
    plt.show()

    # plot training and validation loss values
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(['Train', 'Val'], loc = 'upper left')
    plt.show()

# Chargement des données
DIR = './train'
(X_train, Y_train) = DataLoading(DIR)


DIR = './test'
(X_test, Y_test) = DataLoading(DIR)


X_train = X_train / 255
X_test = X_test / 255


# reshape the data

#X_train = X_train.reshape(-1, 256, 256, 3)
#X_test = X_test.reshape(-1, 256, 256, 3)
#Y_train = Y_train.reshape(-1, 1)
Y_train = keras.utils.to_categorical(Y_train, len(labels))
#Y_test = Y_test.reshape(-1, 1)
Y_test = keras.utils.to_categorical(Y_test, len(labels))
#X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3)


# Explore the dataset
print("X_train shape:" + str(X_train.shape))
print("Y_train shape:" + str(Y_train.shape))
print("X_test shape:" + str(X_test.shape))
print("Y_test shape:" + str(Y_test.shape))

IMG_SIZE = 256

"""
model = Sequential(
    [
        Conv2D(filters = 8, kernel_size = (3, 3), padding = 'same', activation = 'relu', input_shape = (IMG_SIZE, IMG_SIZE, 3)),
        MaxPool2D(pool_size = (2, 2), strides = (2, 2)),

        Conv2D(filters = 24, kernel_size = (3, 3), padding = 'same', activation = 'relu'),
        MaxPool2D(pool_size = (2, 2), strides = (2, 2)),

        Conv2D(filters = 72, kernel_size = (3, 3), padding = 'same', activation = 'relu'),
        MaxPool2D(pool_size = (2, 2), strides = (2, 2)),

        Conv2D(filters = 144, kernel_size = (3, 3), padding = 'same', activation = 'relu'),
        MaxPool2D(pool_size = (2, 2), strides = (2, 2)),
        
        Flatten(),
        Dense(128, activation = 'relu'),
        Dropout(0.5),
        Dense(len(labels), activation = 'softmax')
    ]
)
"""


model = Sequential(
    [
        Conv2D(filters = 16, kernel_size = (3, 3), padding = 'same', activation = 'relu', input_shape = (IMG_SIZE, IMG_SIZE, 3)),
        MaxPool2D(pool_size = (2, 2), strides = (2, 2)),

        Conv2D(filters = 32, kernel_size = (3, 3), padding = 'same', activation = 'relu'),
        MaxPool2D(pool_size = (2, 2), strides = (2, 2)),
    
        
        
        Flatten(),
        Dense(64, activation = 'relu'),
        Dropout(0.5),
        Dense(len(labels), activation = 'softmax')
    ]
)



model.summary()

predictions = model(X_train[:1]).numpy()
print(predictions)


model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

history = model.fit(X_train, Y_train, epochs = 15, validation_split = 0.2)

HistoryPlot(history)

