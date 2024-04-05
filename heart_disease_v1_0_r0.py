# -*- coding: utf-8 -*-
"""Heart_Disease_V1.0_R0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lTKqES6SJNtaYc09JUk-NusaF-P7iB6D

# **Heart Disease prediction Code V1.0 (Assignment)**
"""

#Importing of necessary liabraries
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

#Loading CSV file and Converting it in to dataframe 
df=pd.read_csv("/content/heart.csv")
df.head()

df.info()

df.isna().sum() #there are no null values in Dataframe

#Number of males and females whose heart data is stored in the dataset
df.sex.value_counts()

#Count of the number of males and females who have heart disease
df.sex[df.target==1].value_counts()

sns.set()
df.hist(figsize=(25,10))
plt.show()

pd.crosstab(df.target,df.sex)

df.sex[df.target==1].value_counts().plot(kind='bar',figsize=(10,6),color=['green','blue'])
plt.title("Count of the number of males and females with heart disease")
plt.xticks(rotation=0);

pd.crosstab(df.target,df.sex).plot(kind='bar',figsize=(10,6),color=["lightblue","pink"])
plt.title("Frequency of Heart Disease vs Sex")
plt.xlabel("0= Heart Disease, 1= No disease")
plt.ylabel("Number of people with heart disease")
plt.legend(["Female","Male"])
plt.xticks(rotation=0);

"""Building a Correlation Matrix"""

df.corr()

#correlation matrix with heatmap
cor_mat=df.corr()
fig,ax=plt.subplots(figsize=(15,10))
sns.heatmap(cor_mat,annot=True,linewidths=0.5,fmt=".3f")

#standard scaling with minmaxscaler
from sklearn.preprocessing import MinMaxScaler
scal=MinMaxScaler()
df1=df
feat=['age', 	'sex', 	'cp', 'trestbps', 'chol', 	'fbs', 	'restecg', 	'thalach' ,	'exang', 	'oldpeak' ,	'slope', 	'ca', 'thal']
df[feat] = scal.fit_transform(df[feat])
df.head()

#Creating Features and Target variable
X=df1.drop("target",axis=1).values
Y=df1.target.values

#Splitting the data into train and test sets
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,random_state=52,test_size=0.3)

#Create a function for evaluating metrics
from sklearn.metrics import accuracy_score,recall_score,f1_score,precision_score,roc_auc_score,confusion_matrix

def evaluation(Y_test,Y_pred):
  acc=accuracy_score(Y_test,Y_pred)
  rcl=recall_score(Y_test,Y_pred)
  f1=f1_score(Y_test,Y_pred)
 

  metric_dict={'accuracy': round(acc,3),
               'recall': round(rcl,3),
               'F1 score': round(f1,3),
               
              }

  return print(metric_dict)

#evaluation(Y_test,SVC_Y_pred)

"""# **Fitting and Comparing different Models**"""

np.random.seed(42)
from sklearn.linear_model import LogisticRegression
LR_clf=LogisticRegression()
LR_clf.fit(X_train,Y_train)
LR_Y_pred=LR_clf.predict(X_test)
LR_score=LR_clf.score(X_test,Y_test)
#print(LR_score)
evaluation(Y_test,LR_Y_pred)

np.random.seed(42)
from sklearn.neighbors import KNeighborsClassifier
Knn_clf=  KNeighborsClassifier()
Knn_clf.fit(X_train,Y_train)
Knn_Y_pred=Knn_clf.predict(X_test)
Knn_score=Knn_clf.score(X_test,Y_test)
#print(Knn_score)
evaluation(Y_test,Knn_Y_pred)

np.random.seed(42)
from sklearn.svm import SVC
SVC_clf=SVC()
SVC_clf.fit(X_train,Y_train)
SVC_score=SVC_clf.score(X_test,Y_test)
SVC_Y_pred=SVC_clf.predict(X_test)
#print(SVC_score)
evaluation(Y_test,SVC_Y_pred)

from xgboost import XGBClassifier
XGB_clf=XGBClassifier()
XGB_clf.fit(X_train,Y_train)
XGB_score=XGB_clf.score(X_test,Y_test)
XGB_Y_pred=XGB_clf.predict(X_test)
#print(SVC_score)
evaluation(Y_test,XGB_Y_pred)

np.random.seed(42)
from sklearn.ensemble import RandomForestClassifier
RF_clf=RandomForestClassifier(n_estimators=450)
RF_clf.fit(X_train,Y_train)
RF_score=RF_clf.score(X_test,Y_test)
RF_Y_pred=RF_clf.predict(X_test)
#print(RF_score)
evaluation(Y_test,RF_Y_pred)

model_comp = pd.DataFrame({'Model': ['Logistic Regression','Random Forest',
                    'K-Nearest Neighbour','Support Vector Machine',"XGBoost"], 'Accuracy': [LR_score*100,
                    RF_score*100,Knn_score*100,SVC_score*100,XGB_score*100]})
model_comp

"""# **Tuning KNN**




"""

neighbors = range(1, 21) # 1 to 20
# Setup algorithm
knn = KNeighborsClassifier()

# Loop through different neighbors values
for i in neighbors:
    knn.set_params(n_neighbors = i) # set neighbors value
    
    # Fit the algorithm
    print(f"Accuracy with {i} no. of neighbors: {knn.fit(X_train, Y_train).score(X_test,Y_test)}%")

from matplotlib import pyplot
error_rate= []
for i in range(1,40):
    knn = KNeighborsClassifier(n_neighbors = i)
    knn.fit(X_train,Y_train)
    pred_i = knn.predict(X_test)
    error_rate.append(np.mean(pred_i != Y_test))


plt.figure(figsize = (10,6))
plt.plot(range(1,40),error_rate,color = 'black',linestyle = '--',marker = 'o',markerfacecolor='red',markersize = 8)
plt.title('Error Rate vs K_value')
plt.xlabel('K_value')
plt.ylabel('Error Rate')

np.random.seed(42)
from sklearn.neighbors import KNeighborsClassifier
Knn_clf=  KNeighborsClassifier(n_neighbors=1)
Knn_clf.fit(X_train,Y_train)
Knn_Y_pred=Knn_clf.predict(X_test)
Knn_score=Knn_clf.score(X_test,Y_test)
evaluation(Y_test,Knn_Y_pred)

"""Knn_clf=  KNeighborsClassifier(n_neighbors=1)    #final value of KNN model

# **Tuning Random Forest**
"""

from sklearn.ensemble import RandomForestClassifier
np.random.seed(42)
for i in range(1,10,1):
  print(f"With {i*10} estimators:")
  clf2=RandomForestClassifier(n_estimators=i*10,max_depth=i,random_state=i).fit(X_train,Y_train)
  print(f"Accuracy: {clf2.score(X_test,Y_test)*100:2f}%")

error_rate= []
for i in range(1,40):
  RF_clf2=RandomForestClassifier(n_estimators=i*10,max_depth=i,random_state=i)
  RF_clf2.fit(X_train,Y_train)
  pred_i = RF_clf2.predict(X_test)
  error_rate.append(np.mean(pred_i != Y_test))


plt.figure(figsize = (10,6))
plt.plot(range(1,40),error_rate,color = 'black',linestyle = '--',marker = 'o',markerfacecolor='red',markersize = 8)
plt.title('Error Rate vs Estimator_value')
plt.xlabel('Estimator_value')
plt.ylabel('Error Rate')

from sklearn.ensemble import RandomForestClassifier
RF_clf2=RandomForestClassifier(n_estimators=80,max_depth=8,random_state=8)
RF_clf2.fit(X_train,Y_train)
RF2_acc_score=RF_clf2.score(X_test,Y_test)
RF2_Y_pred=RF_clf2.predict(X_test)
evaluation(Y_test,RF2_Y_pred)

"""RF_clf2=RandomForestClassifier(n_estimators=80,max_depth=8,random_state=8) #final value of RF model

# **Hyper parameter tuning SVC using GridSearchCV**
"""

from sklearn.model_selection import GridSearchCV 
  
# defining parameter range 
param_grid = {'C': [0.1, 1,2, 10, 100, 1000],  
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001], 
              'kernel': ['rbf','linear']}  
  
gs_clf = GridSearchCV(SVC(), param_grid,cv=5, refit = True, verbose = 3) 
  
# fitting the model for grid search 
gs_clf.fit(X_train, Y_train)

print(gs_clf.best_params_)

print(f"Accuracy score:{gs_clf.score(X_test,Y_test)}%")

"""# **Hyper parameter tuning KNN using GridSearchCV**"""

knn_grid={'n_neighbors': np.arange(1,30,1),
          'leaf_size': np.arange(1,50,1)}

gs_knn=GridSearchCV(KNeighborsClassifier(),param_grid=knn_grid,cv=5,verbose=True)

gs_knn.fit(X_train, Y_train)

gs_knn.best_params_

print(f"Accuracy score:{gs_knn.score(X_test,Y_test)*100}%")

model_comp = pd.DataFrame({'Model': ['Logistic Regression','Random Forest',
                    'K-Nearest Neighbour','Support Vector Machine','Extreme Gradient Boost'], 'Accuracy': [LR_score*100,
                    RF2_acc_score*100,Knn_score*100,SVC_score*100, XGB_score*100]})
model_comp

"""# **The Best evaluation parameters achieved with KNN**"""

print(" Best evaluation parameters achieved with KNN:") 
evaluation(Y_test,Knn_Y_pred)

final_metrics={'Accuracy': Knn_clf.score(X_test,Y_test),
                   'Precision': precision_score(Y_test,Knn_Y_pred),
                   'Recall': recall_score(Y_test,Knn_Y_pred),
                   'F1': f1_score(Y_test,Knn_Y_pred),
                   'AUC': roc_auc_score(Y_test,Knn_Y_pred)}

metrics=pd.DataFrame(final_metrics,index=[0])

metrics.T.plot.bar(title='Final metric evaluation',legend=False);

from sklearn.metrics import confusion_matrix

fig,ax=plt.subplots()
ax=sns.heatmap(confusion_matrix(Y_test,Knn_Y_pred),annot=True,cbar=True);

"""# **Hance, KNN model is selected for final Predictions**"""

user_input=input("Enter the values one by one")
user_input=user_input.split(",")


for i in range(len(user_input)):
    # convert each item to int type
    user_input[i] = float(user_input[i])

user_input=np.array(user_input)
user_input=user_input.reshape(1,-1)
knn_Y_pred=Knn_clf.predict(user_input)
if(knn_Y_pred[0]==0):
  print("Predicted that there are more chances of Heart disease")
else:
  print("Predicted that there are less lchances of Heart disease")

"""# **Saving The Final KNN trained model with Pickle File for streamlit APP development**"""

import pickle as pickle
#pkl.dump(Knn_clf,open("final_model.p","wb"))

pickle.dump(Knn_clf, open('final_model_KNN.pkl', 'wb'))

loaded_model = pickle.load(open('final_model_KNN.pkl', 'rb')) 
prediction = loaded_model.predict(user_input)
prediction