#Problem 1: Dataset Splitting

#You have recordings of 44 phones from 100 people; each person records ~200 phones/day for 5 days.

#1. Design a valid training/validation/test split strategy that ensures the model generalizes to new speakers.

# Answer: ~200 recording per day for 5 days is ~1000 recording per person, for the 100 people, ~100,000 recordings in main dataset
#I would train 70 speakers so there are ~70,000 recordings, validate with ~15,000 recordings and teset ~15,000 recording. 


#2. You now receive an additional dataset of 10,000 phone recordings from Kilian, a single speaker.
#You must train a model that performs well specifically for Kilian, while also maintaining generalization.
#Describe your proposed split strategy and reasoning. (Theory)

#Answer: I would keep the ~15,000 recordings and from Kilian's 10,000 recordings from a single speaker I would split 6,000 for training and the remianing 4,000 into valluation and testing.

#Problem 2: K-Nearest Neighbors
#1. 1-NN Classification: Given dataset:
#Plot the 1-NN decision boundary and classify new points visually.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import seaborn as sns

positive=np.array([[1,2],[1,4],[5,4]])
negative=np.array([[3,1],[3,2]])
X_train = np.vstack([positive, negative])
y_train = np.array([1,1,1,-1,-1])

def predict(X_train,y_train,x_test,k=1):
    distances=np.sqrt(np.sum((X_train - x_test)**2,axis=1))
    nearest=np.argsort(distances)[:k]
    return y_train[nearest[0]]

x_min,x_max = 0,6
y_min,y_max = 0,5
xx,yy = np.meshgrid(np.arange(x_min, x_max, 0.1),np.arange(y_min, y_max, 0.1))
Z=np.array([predict(X_train, y_train, np.array([x,y])) 
for x, y in zip(xx.ravel(), yy.ravel())])
Z=Z.reshape(xx.shape)


plt.contourf(xx,yy,Z,alpha=0.4)
plt.scatter(positive[:,0],positive[:,1],c="blue",s=100,marker='+',label="Positive")
plt.scatter(negative[:,0], negative[:,1],c="red",s=100,marker='_',label="Negative")
plt.title("1-NN Decision Boundary")
plt.legend()
plt.show()

test_points-np.array([[2,1],[2,3],[4,3],[4,1]])
for p in test_points:
    pred=predict(X_train,y_train,p)            

#2. Feature Scaling: Consider dataset:
#What would the 1-NN classify point (500,1) as before and after scaling to [0,1] per feature?

positive=np.array([[100,2],[100,4],[500,4]])
negative=([[300,1],[300,2]])
X=np.vstack([positive, negative])
y=np.array([1,1,1,-1,-1])
test_point=np.array([[500,1]])
def scale(X):
    return (X-x.min(axis=0))/(X.max(axis=0)-X.min(axis=0))

before=predict(X,y,test_point[0])
X_scaled=scale(X)
test=scale(test_point)
after=predict(X_scaled,y,test[0])

#3. Handling Missing Values: How can you modify K-NN to handle missing features in a test point?
def missing(X_train, y_train, x_test, k=1, missing_val=123):
    distances=[]
    for x_train in X_train:
        total_distance=0
        valid_distnace=0
        for j in range(len(x_test)):
            if x_test[j]!=missing_val:
                total_distance+=(x_test[j]-x_train[j])**2
                valid_count=1
        if valid_count>0:
            distance=np.sqrt(total_distance)
        distances.append(distance)
    closest=np.argsort(distances)[:k]
    return y_train[closest[0]]

#4. High-dimensional Data: Why can K-NN still work well for images even with thousands of pixels?
#Answer: The images are just the visual representation of the points but the numerical data remains the same. 







