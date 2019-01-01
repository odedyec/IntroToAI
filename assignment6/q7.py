import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from itertools import product
""" Create the database of 6 binary inputs and the label output """
data = []
labels = []
for perm in product([True, False], repeat=6):
    perm_i = list(map(int, perm))
    label = [0] if sum(perm_i) == 0 or sum(perm_i) % 3 else [1]
    data.append(perm_i)
    labels.append(label)
X = np.array(data, "float32")
y = np.array(labels, "float32")

""" Build a Fully connected NN model - Input (6 neurons), Hidden(6 neurons), output(1 neurons)"""
model = Sequential()
d1 = Dense(6, input_dim=6)
model.add(d1)
model.add(Activation('tanh'))
d2 = Dense(1)
model.add(d2)
model.add(Activation('sigmoid'))
# compile network
sgd = SGD(lr=0.1)
model.compile(loss='binary_crossentropy', optimizer=sgd)
# train
model.fit(X, y, batch_size=1, nb_epoch=250)
""" Predict the database and compare to output """
pred = model.predict(X).round()
cnt = 0
for i in range(64):
    if pred[i] == labels[i]:
        cnt += 1
print('Accuracy is {} ({}/64)'.format(cnt / 64, cnt))
print('----------------')
print(d1.get_weights())
print('----------------')
print(d2.get_weights())