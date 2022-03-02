#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


# In[2]:


## import data
path = 'data/heart.csv'
heart_df = pd.read_csv(path)
heart_df.head()


# In[3]:


heart_df.describe()


# In[4]:


heart_df['FastingBS'].value_counts()


# In[5]:


# there are four different chest pain types
heart_df['ChestPainType'].value_counts()


# In[6]:


# three different resting ecg responses
heart_df['RestingECG'].value_counts()


# In[7]:


# three st_slope values
heart_df['ST_Slope'].value_counts()


# In[8]:


# One hot encoding of categorical data values:
heart_df_encoded= pd.get_dummies(heart_df)
heart_df_encoded.head()


# In[9]:


# Define input data and target:
X = heart_df_encoded.drop('HeartDisease', axis=1)
y = heart_df_encoded['HeartDisease']


# In[10]:


# Train, test, split:
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)


# In[12]:


# Apply standard scaling:
from sklearn.preprocessing import StandardScaler

X_scaler = StandardScaler().fit(X_train)
X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)

# View scaled data:
X_train_scaled_df = pd.DataFrame(X_train_scaled)
X_train_scaled_df.head()


# In[13]:


# Create Random Forest Model:
from sklearn.ensemble import RandomForestClassifier

rfc= RandomForestClassifier()
rfc.fit(X_train_scaled, y_train)

# Check the accuracy:
train_score = rfc.score(X_train_scaled, y_train)
test_score = rfc.score(X_test_scaled, y_test)
print(f"Train Score = {train_score:.3f}, Test Score = {test_score:.3f}")


# In[ ]:


# Display the confusion matrix:
from sklearn.metrics import confusion_matrix


# In[24]:


# Display the important features graph:
RFfeature_importance = pd.Series(rfc.feature_importances_, index=X_train.columns).sort_values(ascending=False)
RFfeature_importance[0:20].plot(kind='bar',
                                 title=f'Most Influential Features for Scaled Random Forest Model\nScore: {test_score:.3f}')


# In[14]:


# Save model and scaler to files:
import pickle

filename1 = 'rfc_model.pkl'
filename2 = 'rfc_scaler.pkl'
pickle.dump(rfc, open(filename1, 'wb'))
pickle.dump(X_scaler, open(filename2, 'wb'))
print(f"Model saved to file: {filename1}")
print(f"Scaler saved to file: {filename2}")


# In[15]:


# Load saved model and scaler from files:
import pickle

model_file = 'rfc_model.pkl'
scaler_file = 'rfc_scaler.pkl'
loaded_model = pickle.load(open(model_file, 'rb'))
loaded_scaler = pickle.load(open(scaler_file, 'rb'))
print(f"Model loaded from file: {model_file}")
print(f"Scaler loaded from file: {scaler_file}")


# In[19]:


# Make some testing data for a fictitious patient:
Age = 65
Sex = "M"
ChestPainType = "ATA"
RestingBP = 185
Cholesterol = 235
FastingBS = 0
RestingECG = "Normal"
MaxHR = 150
ExerciseAngina = "Y"
Oldpeak = 1.5
ST_Slope = "Flat"

# Create column headers to match the ones in heart_df_encoded:
column_headers = ["Age","RestingBP","Cholesterol","FastingBS","MaxHR","Oldpeak",
                  "Sex_F","Sex_M",
                  "ChestPainType_ASY","ChestPainType_ATA","ChestPainType_NAP","ChestPainType_TA",
                  "RestingECG_LVH","RestingECG_Normal","RestingECG_ST",
                  "ExerciseAngina_N","ExerciseAngina_Y",
                  "ST_Slope_Down","ST_Slope_Flat","ST_Slope_Up"]

# Put the testing data into a row:
data_row = []
data_row.append(Age)
data_row.append(RestingBP)
data_row.append(Cholesterol)
data_row.append(FastingBS)
data_row.append(MaxHR)
data_row.append(Oldpeak)
if Sex == "F":
    data_row.append(1)
    data_row.append(0)
else:
    data_row.append(0)
    data_row.append(1)
if ChestPainType == "ASY":
    data_row.append(1)
    data_row.append(0)
    data_row.append(0)
    data_row.append(0)
elif ChestPainType == "ATA":
    data_row.append(0)
    data_row.append(1)
    data_row.append(0)
    data_row.append(0)
elif ChestPainType == "NAP":
    data_row.append(0)
    data_row.append(0)
    data_row.append(1)
    data_row.append(0)    
else:
    data_row.append(0)
    data_row.append(0)
    data_row.append(0)
    data_row.append(1)
if RestingECG == "LVH":
    data_row.append(1)
    data_row.append(0)
    data_row.append(0)
elif RestingECG == "Normal":
    data_row.append(0)
    data_row.append(1)
    data_row.append(0)
else:
    data_row.append(0)
    data_row.append(0)
    data_row.append(1)
if ExerciseAngina == "N":
    data_row.append(1)
    data_row.append(0)
else:
    data_row.append(0)
    data_row.append(1)
if ST_Slope == "Down":
    data_row.append(1)
    data_row.append(0)
    data_row.append(0)
elif ST_Slope == "Flat":
    data_row.append(0)
    data_row.append(1)
    data_row.append(0)
else:
    data_row.append(0)
    data_row.append(0)
    data_row.append(1)
    
# Create a single row dataframe to pass as input to the model:
input_data = pd.DataFrame([data_row], columns=column_headers)
input_data


# In[20]:


# Scale the input data: 
input_data_scaled = loaded_scaler.transform(input_data)

# Get prediction from model:
y = loaded_model.predict(input_data_scaled)
if y == 1:
    print("You are at risk for having a heart attack.")
else:
    print("You are not at risk for having a heart attack.")

