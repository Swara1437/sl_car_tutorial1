# -*- coding: utf-8 -*-
"""App

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PixlguU02S9nfD2aq_vYbobIvks9fSco
"""

import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# App Title
st.title("🚗 Car Evaluation Classifier using Random Forest 🚗")
st.write("Predict the car condition using Machine Learning based on various features.")

# Made by Swati (Added credit)
st.markdown("👩‍💻 *Made by: Swati*")

# Load the 'car.csv' dataset

df = pd.read_csv('/content/car.csv')  # Updated: Using relative path 'car.csv'


# Encoding categorical columns
df_encoded = df.apply(lambda col: pd.factorize(col)[0])

# Splitting data
X = df_encoded.iloc[:, :-1]
y = df_encoded.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)
st.success(f"🎯 Model Accuracy: {accuracy * 100:.2f}%")

st.subheader("🧪 Predict Car Condition")

# Get unique values for each feature
feature_options = {column: df[column].unique() for column in df.columns[:-1]}

# Create input sliders/selectors
input_data = []
for column in df.columns[:-1]:
    if pd.api.types.is_numeric_dtype(df[column]):
        # Check if column is 'Unnamed: 0' and use selectbox instead of slider
        if column == 'Unnamed: 0':
            value = st.selectbox(f"{column}", feature_options[column])
        else:
            # Slider for numerical features (excluding 'Unnamed: 0')
            min_val = float(df[column].min())
            max_val = float(df[column].max())
            mean_val = float(df[column].mean())
            value = st.slider(f"{column}", min_val, max_val, mean_val)
    else:
        value = st.selectbox(f"{column}", feature_options[column])
    input_data.append(value)

# Convert input to encoded form
input_encoded = [pd.Series(df[column].unique()).tolist().index(val) for column, val in zip(df.columns[:-1], input_data)]

# Predict
prediction = model.predict([input_encoded])[0]

# Decode prediction
decoded_label = pd.Series(df[df.columns[-1]].unique())[prediction]
st.write(f"### Predicted Car Condition: *{decoded_label}*")

st.write("#### About the App:")
st.write("This app uses a Random Forest Classifier trained on the car dataset to predict the condition of a car based on its features.")

