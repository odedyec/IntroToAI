# from keras.models import Sequential
# from keras.layers import Dense, Activation
# import numpy as np
# from itertools import product
#
#
# model = Sequential()
# model.add(Dense(2, input_dim=2, kernel_initializer='normal', activation='sigmoid'))
# model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
# model.compile(loss='binary_crossentropy',
#               optimizer='adam',
#               metrics=['accuracy'])
#
# # Generate dummy data
#
# # data = []
# # labels = []
# # for perm in product([True, False], repeat=6):
# #     perm_i = list(map(int, perm))
# #     label = [0] if sum(perm_i) == 0 or sum(perm_i) % 3 else [1]
# #     print(perm_i, label)
# #     data.append(perm_i)
# #     labels.append(label)
# # data = np.array(data)
# # labels = np.array(labels)
# data = []
# labels = []
# for perm in product([True, False], repeat=2):
#     perm_i = list(map(int, perm))
#     label = [1] if perm[0] is not perm[1] else [0]
#     print(perm_i, label)
#     data.append(perm_i)
#     labels.append(label)
# data = np.array(data)
# labels = np.array(labels)
#
# # Train the model, iterating on the data in batches of 32 samples
# model.fit(data, labels, epochs=5, batch_size=4, validation_split=0.)
#
# cnt = []
# for perm in product([True, False], repeat=2):
#     perm_i = list(map(int, perm))
#     label = [1] if perm[0] is not perm[1] else [0]
#
#     p = model.predict(np.array([perm_i]))
#     res = int( 2 * p[0][0])
#     cnt.append(1 if res == label[0] else 0)
#     print(perm_i, label, p, res)
#
# print (sum(cnt) / len(cnt), sum(cnt), len(cnt))
#
# #
# # cnt = []
# # for perm in product([True, False], repeat=6):
# #     perm_i = list(map(int, perm))
# #     label = [0] if sum(perm_i) == 0 or sum(perm_i) % 3 else [1]
# #     p = model.predict(np.array([perm_i]))
# #     res = int( 2 * p[0][0])
# #     cnt.append(1 if res == label[0] else 0)
# #     print(perm_i, label, p, res)
# #
# # print (sum(cnt) / len(cnt), sum(cnt), len(cnt))


import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from itertools import product
# the four different states of the XOR gate


data = []
labels = []
for perm in product([True, False], repeat=6):
    perm_i = list(map(int, perm))
    label = [0] if sum(perm_i) == 0 or sum(perm_i) % 3 else [1]
    data.append(perm_i)
    labels.append(label)
X = np.array(data, "float32")

# the four expected results in the same order
y = np.array(labels, "float32")

model = Sequential()
d1 = Dense(6, input_dim=6)
model.add(d1)
model.add(Activation('tanh'))
d2 = Dense(1)
model.add(d2)
model.add(Activation('sigmoid'))

sgd = SGD(lr=0.1)
model.compile(loss='binary_crossentropy', optimizer=sgd)

model.fit(X, y, batch_size=1, nb_epoch=500)

pred = model.predict(X).round()

cnt = 0
for i in range(64):
    if pred[i] == labels[i]:
        cnt += 1

print(cnt, cnt / 64)
print('----------------')
print(d1.get_weights())
print('----------------')
print(d2.get_weights())