import numpy as np
import csv
import os
import collections
from collections import Counter
from numpy import linalg as la
from sklearn.cluster import SpectralClustering, spectral_clustering
import networkx as nx
import scipy.cluster.vq as vq
import matplotlib.pyplot as plt

#Decision Tree Classifier
import sklearn
from sklearn import tree

from sklearn import datasets
from sklearn import svm
import numpy as np

import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsClassifier

# Create Adjancency Matrix
class ReadData:
	def read_train_output(self):
		training_output = []
		basepath = os.path.dirname(__file__)
		filepath = os.path.abspath(os.path.join(basepath, "cluster_preds4.csv"))
		with open(filepath) as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			count = 0
			for row in readCSV:
				if count == 0:
					count += 1
					continue
				training_output.append(int(row[1]))
		return training_output

	def read_training_input(self):
		basepath = os.path.dirname(__file__)
		filepath = os.path.abspath(os.path.join(basepath, "Extracted_features.csv"))
		training_input = []
		with open(filepath) as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			for row in readCSV:
				row = list(map(float, row))
				training_input.append(row)
		return training_input

	def generate_output_file(self, output_cluster, output_filename):
		fileToWrite = open(output_filename,"w")
		fileToWrite.write('Id'+','+'Label\n')
		for i in range(0, 4000):
			fileToWrite.write(str(6000 + i+1)+","+str(output_cluster[i]))
			fileToWrite.write("\n")
		fileToWrite.close()

	def read_seed_input(self):
		basepath = os.path.dirname(__file__)
		filepath = os.path.abspath(os.path.join(basepath, "Seed.csv"))
		seed_input = dict()
		with open(filepath) as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			for row in readCSV:
				seed_input[int(row[0])] = int(row[1])
		return seed_input

if __name__ == "__main__":
	a_obj = ReadData()
	t_output = a_obj.read_train_output()
	t_input = a_obj.read_training_input()

	training_features = t_input[:6000]
	labels = t_output

	seed_data = a_obj.read_seed_input()
	for key in seed_data:
		labels[key-1] = seed_data[key]


	# Decision Trees - 17%
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(training_features,labels)

	test_input = t_input[6000:]
	test_output = []
	for i in range(len(test_input)):
		test_output.append(clf.predict([test_input[i]])[0])
	print (len(test_output))

	# BackPropagation Classifier Object
	#training_features2 = t_input[:6000]
	#labels2 = t_output	
	#test_output2 = []
	#for i in range(len(test_input)):
	#	clf1 = tree.DecisionTreeClassifier()
	#	clf1 = clf1.fit(training_features2,labels2)
	#	training_features2.append(test_input[i])
	#	labels2.append(clf.predict([test_input[i]])[0])
	#	test_output2.append(clf.predict([test_input[i]])[0])
	#print (len(test_output2))

	a_obj.generate_output_file(test_output, "classifier_predictions.csv")

	C = 1.0
	# Linear SVM - 48%
	#svc = svm.SVC(kernel='linear', C=C).fit(training_features, labels)
	
	# RBF SVM - 48%
	svc = svm.SVC(kernel='rbf', C=C).fit(training_features, labels)
	
	lin_svc = svm.LinearSVC(C=C).fit(training_features, labels)
	Y2 = lin_svc.predict(test_input)
	a_obj.generate_output_file(Y2, "classifier_predictions3.csv")

	neigh = KNeighborsClassifier(n_neighbors=10)
	neigh.fit(training_features, labels)
	Y3 = neigh.predict(test_input)
	a_obj.generate_output_file(Y3, "KNNclassifier_predictions.csv")
