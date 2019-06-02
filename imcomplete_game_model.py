#Set up model 

#gotta love dem imports 
import csv
import pandas
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.neural_network import MLPClassifier
import pickle

#import file
c4_data = pandas.read_csv("c4_data.csv")

#replace strings with numbers 
c4_data =c4_data.replace(to_replace = "b", value = 0)#blank space 
c4_data = c4_data.replace(to_replace = "x", value = 1)#player 1 move
c4_data = c4_data.replace(to_replace = "o", value = 2)#player 2 move 
c4_data = c4_data.replace(to_replace = "win", value = 1)#player 1 won
c4_data = c4_data.replace(to_replace = "loss", value = 2)#player 2 won
c4_data = c4_data.replace(to_replace = "draw", value = 0)#draw

#seperate data and targets
data = c4_data.drop("winner", axis = 1)
target = c4_data['winner']

target=target.astype('int')


#seperate training and test sets
data_train, data_test, target_train, target_test = train_test_split(
    data, target, test_size=0.33, random_state=42)

#desicion tree model
tree_model = DecisionTreeClassifier()
tree_model.fit(data_train,target_train)

pred = tree_model.predict(data_test)

print(" Tree Accuracy score:", accuracy_score(target_test,pred))


"""#random forest
print("starting random forest") 
data, target = make_classification(n_samples=1000, n_features=4,n_informative=2,
                           n_redundant=0,random_state=0, shuffle=False)
forest_model = RandomForestClassifier()
forest_model.fit(data_train,target_train)
print("done fitting")

pred = forest_model.predict(data_test)

print("forest Accuracy score:", accuracy_score(target_test,pred))


#svc
print("starting svc") 
svc_model = LinearSVC(random_state = 0)
svc_model.fit(data_train,target_train)
print("done fitting")

pred = svc_model.predict(data_test)

print("SVC Accuracy score:", accuracy_score(target_test,pred))

#k nearest
print("starting k nearest")
neigh_model = KNeighborsClassifier(n_neighbors=4)
neigh_model.fit(data_train,target_train)
print("done fitting") 

pred = neigh_model.predict(data_test)

print("neigh Accuracy score:", accuracy_score(target_test,pred))"""

#neural net
print("starting neural network")
neural_model = MLPClassifier(hidden_layer_sizes=(64,64,64),max_iter=500)
neural_model.fit(data_train,target_train)
print("done fitting") 

pred = neural_model.predict(data_test)
print("hidden layers: 64,64,13")
print("max_iter:500")

print("neural Accuracy score:", accuracy_score(target_test,pred))

#saving file
print("saving file") 
filename = '/home/fiabot/Desktop/connect_4/neural_model_test.sav'
pickle.dump(neural_model, open(filename, 'wb'))



