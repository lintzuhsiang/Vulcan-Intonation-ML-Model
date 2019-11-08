
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Conv1D,Conv2D, Flatten, Dropout, MaxPooling1D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import sys
from data_process import Data_process # import train_data,test_data
data_process = Data_process()
import numpy as np
#label: sad0, angry1,happy2,neutral3
from sklearn.utils import shuffle


if os.path.isfile("train_x_1.npy") and os.path.isfile("train_y_1.npy"):
    train_x = np.load('train_x_1.npy')
    train_y = np.load('train_y_1.npy')
else: train_x,train_y = data_process.train_data('train data')

data_x= data_process.test_data(sys.argv[1])
train_y = to_categorical(train_y[1:])
train_x = train_x[1:]
train_X,train_Y = shuffle(train_x,train_y)
train_len = int(len(train_y) * 0.7)
train_x = train_X[:train_len]
train_y = train_Y[:train_len]
test_x = train_X[train_len:]
test_y = train_Y[train_len:]
print(train_x.shape,train_y.shape)
print(test_x.shape,test_y.shape)

# print("train y",train_y.shape)
# print("train x",train_x.shape)
if os.path.isdir("./model"):
    model = tf.keras.models.load_model('./model')
    print("load saved model")
else:
# if 1:
    model = Sequential([
        Conv1D(16, 3, padding='same', activation='relu', input_shape=((train_x.shape[1], train_x.shape[2]))),#data_format="channels_last"
        MaxPooling1D(),
        Conv1D(32, 3, padding='same', activation='relu'),
        MaxPooling1D(),
        Conv1D(64, 3, padding='same', activation='relu'),
        MaxPooling1D(),
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(264, activation='relu'),
        Dropout(0.5),
        Dense(4, activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    model.summary()

    history = model.fit(train_x,train_y,epochs=50,batch_size=32,validation_data=(test_x,test_y),verbose=2)

    model.save('./model')
ans = []
import csv

# for i in test_x:
predictions = model.predict(data_x)

#write result in csv file
sad = 0
angry = 0
happy =0
neutral = 0

second = 0
with open('%s.csv'%sys.argv[1],'w') as csv_file:

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['second','sad','angry','happy','neutral','class'])
    for prediction in predictions:
        max_class = np.argmax(prediction)
        sad_,angry_,happy_,neutral_ = prediction
        csv_writer.writerow([second,sad_,angry_,happy_,neutral_,max_class])
        second += 1
        if max_class ==0:
            sad += 1
        elif max_class ==1:
            angry +=1
        elif max_class ==2:
            happy+=1
        elif max_class==3:
            neutral+=1
    csv_writer.writerow(['Class count',sad,angry,happy,neutral])


