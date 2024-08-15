from sklearn.preprocessing import LabelEncoder
import pandas as pd
import pickle

# Load your dataset (use the dataset you used during training)
df = pd.read_csv('data/preprocessed_data.csv')

# Fit the LabelEncoder on the 'Primary Type' column (the target variable)
label_encoder = LabelEncoder()
label_encoder.fit(df['Primary Type'])

# Save the LabelEncoder
import pickle
with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)
print("Classes in LabelEncoder:", label_encoder.classes_)
