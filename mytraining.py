import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import pickle

def data_split(data,ratio):
  np.random.seed(42)
  shuffled=np.random.permutation(len(data))
  test_set_size=int(len(data)*ratio)
  test_indices=shuffled[:test_set_size]
  train_indices=shuffled[test_set_size:]
  return data.iloc[train_indices],data.iloc[test_indices]

if __name__ == '__main__':
    df=pd.read_csv('covid.csv')
    train,test=data_split(df,0.2)
    X_train=train[['fever','bodypain','age','runnynose','diffbreath']].to_numpy()
    X_test=test[['fever','bodypain','age','runnynose','diffbreath']].to_numpy()
    Y_train=train[['infectionp']].to_numpy().reshape(2032,)
    Y_test=test[['infectionp']].to_numpy().reshape(507,)
    clf = LogisticRegression()
    clf.fit(X_train,Y_train)

    # open a file, where you ant to store the data
    file = open('models/model.pkl', 'wb')

    # dump information to that file
    pickle.dump(clf, file)

    input_features=[100,1,21,1,0]
    infprob=clf.predict_proba([input_features])[0][1]
    print("infprob")