# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 20:14:02 2017

@author: juan9
"""
#Based on Kaleko's excellent notebook. This is a script/python 3 version, without the plots.
#Basically a function library.

import numpy as np

##Script that contains the functions for Andrew NG Machine Learning course exercise 1

datafile = 'data/ex1data1.txt'
cols = np.loadtxt(datafile,delimiter=',',usecols=(0,1),unpack=True) #Load file as csv

#Create matrix with training samples                 
X = np.transpose(np.array(cols[:-1]))
#Create vector of labels, with rows equal to X's rows
y = np.transpose(np.array(cols[-1:]))

#Number of training samples, or m in the equations.
m = y.size 
#Insert the column of 1's into index 0 of the X matrix. This will be x0 which will join
#theta0 as the first parameter of the equation.
X = np.insert(X,0,1,axis=1)

#Gradient Descent
#Parameters
#Can change for different results
alpha = 0.01
num_iterations = 1000

#Hypothesis function h(x) This is the multiplication of the theta vector with each sample.
def hypothesis(theta,X):
    return np.dot(X,theta)

def CostFunction(theta,X,y): #Cost function
    """
    Reminder that the cost function is 1/2m(sum from i to m of (hypothesis(X[i]) - y[i])^2)
    This returns the sum of how far off the predictions were from the labels.
    It's the performance indicator for linear regression.
    """
    return float((1./(2*m)) * np.dot((hypothesis(theta,X)-y).T,(hypothesis(theta,X)-y)))



def GradientDescent(X, initial_theta = np.zeros(2)):
    """
    Do the gradient descent procedure and find the best theta.
    """
    theta_vector = initial_theta
    for i in range(num_iterations):
        temp = theta_vector
        #Update all values of the theta vector
        for j in range(len(temp)):
            temp[j] = theta_vector[j] - (alpha/m)*np.sum((hypothesis(initial_theta,X) - y)*np.array(X[:,j]).reshape(m,1))
        theta = temp
    return theta

theta = GradientDescent(X,np.zeros((X.shape[1],1)))

def OneVarFit(value):
    #Function that computes the prediction from linear regression with 1 variable.
    return theta[0] + theta[1]*value

print("Theta vector for univariate linear regression")
print(theta)
#Profit for population of 90,000
print("Fit for population of 90,000")
print(OneVarFit(9))

#Multivariate Linear Regression 
datafile = 'data/ex1data2.txt'
cols = np.loadtxt(datafile,delimiter=',',usecols=(0,1,2),unpack=True) #Load file as csv

#Create matrix with training samples                 
X = np.transpose(np.array(cols[:-1]))
#Create vector of labels, with rows equal to X's rows
y = np.transpose(np.array(cols[-1:]))

#Number of training samples, or m in the equations.
m = y.size 
#Insert the column of 1's into index 0 of the X matrix. This will be x0 which will join
#theta0 as the first parameter of the equation.
X = np.insert(X,0,1,axis=1)

def Normalize(X):
    mean_vector,std_vector = [],[]
    for i in range(X.shape[1]):
        mean_vector.append(np.mean(X[:,i]))
        std_vector.append(np.std(X[:,i]))
        
        if not i:
            continue
        #Mean normalization calculation.
        X[:,i] =(X[:,i] - mean_vector[-1])/std_vector[-1]
        
    return X,mean_vector,std_vector

newX = X.copy()
#Create normalized copy of matrix.
newX,means,stds = Normalize(newX)

##Calculate theta vector for this matrix, using Gradient Descent.
initial_theta = np.zeros((newX.shape[1],1))
theta = GradientDescent(newX,initial_theta)
print("Theta vector for multivariate linear regression")
print(theta)
print("Cost for house with 1650 sq.feet area and 3 bedrooms")
test = np.array([1650,3])

#Normalize test data
testscaled = [(test[x]-means[x+1])/stds[x+1] for x in range(len(test))]
testscaled.insert(0,1)
print ("$%0.2f" % float(hypothesis(theta,testscaled)))

#Normal equation

from numpy.linalg import inv

def normal_Equation(X,y):
    #Normal equation calculation
    return np.dot(np.dot(inv(np.dot(X.T,X)),X.T),y)

print ("Normal equation prediction of price for a house with an area of 1650 square feet and 3 bedrooms")
print ("$%0.2f" % float(hypothesis(normal_Equation(X,y),[1,1650.,3])))