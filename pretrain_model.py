import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import LabelEncoder
import pickle

# Load the preprocessed data
df = pd.read_csv('data/preprocessed_data.csv')

# Define features and target variable
X = df.drop(columns=['Primary Type'])
y = df['Primary Type']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Reshape data for LSTM [samples, time steps, features]
X_train = np.reshape(np.array(X_train), (X_train.shape[0], 1, X_train.shape[1]))
X_test = np.reshape(np.array(X_test), (X_test.shape[0], 1, X_test.shape[1]))

# Initialize and build the LSTM model
model = Sequential()
model.add(LSTM(units=100, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(units=100, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=100, activation='relu'))
model.add(Dense(units=len(df['Primary Type'].unique()), activation='softmax'))

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=128, validation_data=(X_test, y_test))

# Save the trained model
model.save('lstm_crime_prediction_model.h5')

# Save the LabelEncoder for later use
label_encoder = LabelEncoder()
label_encoder.fit(df['Primary Type'])
with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)
