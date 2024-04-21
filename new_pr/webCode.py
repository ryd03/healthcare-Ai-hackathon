import numpy as np
import pickle

np.random.seed(4)
x_train=np.load('x_train.npy')
raw_y_train=np.load('y_train.npy')


#determine the training and test set sizes:
n_tr=len(raw_y_train)

x_train=x_train.reshape(n_tr, 19*500)

y_train=[]

for i in range(n_tr):
    if raw_y_train[i]==0:
        y_train.append(0)
    else:
        y_train.append(1)


x_tr_means=np.mean(x_train, axis=0)
x_tr_std=np.std(x_train, axis=0, ddof=1)

x_train=(x_train-x_tr_means)/x_tr_std

from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier()
rf.fit(x_train,y_train)
pickle.dump(rf , open("model.pkl" , "wb"))