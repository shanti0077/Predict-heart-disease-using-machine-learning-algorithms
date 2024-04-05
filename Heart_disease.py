import base64
import sklearn
import numpy as np
import pickle as pickle
import streamlit as st
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
#Load the saved model
#model=pkl.load(open("final_model.p","rb"))
#model = pickle.load(open('final_model.pkl', 'rb'))
import joblib


 
# load the model from disk
model = joblib.load("final_model_KNN.pkl")


st.set_page_config(page_title="Heart Health Prediction App ",page_icon="DVC",layout="centered",initial_sidebar_state="expanded")



def preprocess(age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal ):   
    
    # Pre-processing user input   
    if sex=="male":
        sex=1 
    else: sex=0
    
    
    if cp=="Typical angina":
        cp=0
    elif cp=="Atypical angina":
        cp=1
    elif cp=="Non-anginal pain":
        cp=2
    elif cp=="Asymptomatic":
        cp=3
        
    if fbs=="Yes":
        fbs=1
    elif fbs=="No":
        fbs=0

    if restecg=="Nothing to note":
        restecg=0
    elif restecg=="ST-T Wave abnormality":
        restecg=1
    elif restecg=="Possible or definite left ventricular hypertrophy":
        restecg=2
        
    if exang=="Yes":
        exang=1
    elif exang=="No":
        exang=0
        
    if slope=="Upsloping: better heart rate with excercise(uncommon)":
        slope=0
    elif slope=="Flatsloping: minimal change(typical healthy heart)":
        slope=1
    elif slope=="Downsloping: signs of unhealthy heart":
        slope=2  


    user_input=[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
    #user_input=[62,1,0,148,203,0,1,106,0,1.9,1,3,2]
    user_input=np.array([user_input])
    user_input=user_input.reshape(1,-1)
    #user_input=scaler.fit_transform(user_input)
    prediction = model.predict(user_input)

    return prediction

       
    # front end elements of the web page 
html_temp = """ 
    <div style ="background-color:silver;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Heart Disease Prediction App 📱 V1.0</h1> 
    </div> 
    """
      
# display the front end aspect
st.markdown(html_temp, unsafe_allow_html = True) 
st.subheader('Designed by :- Dhiraj Chavan (Assignment)')
      
# following lines create boxes in which user can enter data required to make prediction
age=st.selectbox ("Age",range(1,121,1))
sex = st.radio("Select Gender: ", ('male', 'female'))
cp = st.radio('Chest Pain Type',("Typical angina","Atypical angina","Non-anginal pain","Asymptomatic"))
trestbps=st.selectbox('Resting Blood Sugar',range(1,500,1)) 
chol=st.selectbox('Serum Cholestoral in mg/dl',range(1,1000,1))
fbs=st.radio("Fasting Blood Sugar higher than 120 mg/dl", ['Yes','No'])
restecg=st.radio('Resting Electrocardiographic Results',("Nothing to note","ST-T Wave abnormality","Possible or definite left ventricular hypertrophy"))
thalach=st.selectbox('Maximum Heart Rate Achieved',range(1,300,1))
exang=st.radio('Exercise Induced Angina',["Yes","No"])
oldpeak=st.number_input('Oldpeak')
slope = st.radio('Heart Rate Slope',("Upsloping: better heart rate with excercise(uncommon)","Flatsloping: minimal change(typical healthy heart)","Downsloping: signs of unhealthy heart"))
ca=st.selectbox('Number of Major Vessels Colored by Flourosopy',range(0,5,1))
thal=st.selectbox('Thalium Stress Result',range(0,4,1))


#user_input=preprocess(sex,cp,exang, fbs, slope, thal )
pred=preprocess(age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal)

  

if st.button("Predict"):
    if pred == 0:
        st.error('Predicted that there are more chances of Heart disease')
    elif pred == 1:
        st.success('Predicted that there are less lchances of Heart disease')
    


st.sidebar.subheader("About App")

st.sidebar.info("R1.0 V1.0 ")
st.sidebar.info("📱 : +919881539987")