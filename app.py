from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
import numpy as np
from tensorflow.keras.models import load_model
import pickle

app = Flask(__name__)

# Load the pre-trained LSTM model and the LabelEncoder
model = load_model('lstm_crime_prediction_model.h5')
with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/heatmap')
def heatmap():
    df = pd.read_csv('data/merged_dataset.csv')
    fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude', color='RACE',
                            center=dict(lat=df.Latitude.mean(), lon=df.Longitude.mean()),
                            zoom=10, mapbox_style='carto-positron', height=600)
    fig.update_traces(marker=dict(size=3))
    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
    return render_template('heatmap.html', plot=graphJSON)

# Function to preprocess the input data
def preprocess_input(lat, lon):
    additional_features = np.array([1, 15, 8, 2024])  # Replace with actual feature values
    input_data = np.array([[lat, lon, *additional_features]])  # Shape will be (1, 6)
    input_data = np.reshape(input_data, (1, 1, 6))  # Reshape to (1, 1, 6) for LSTM input
    return input_data

# Function to predict crimes based on location
def predict_crime(input_data):
    predictions = model.predict(input_data)
    top_5_indices = np.argsort(predictions, axis=1)[:, -5:]
    
    # Mapping of encoded integers to crime types (from your previous output)
    crime_type_mapping = {
        0: 'ARSON', 1: 'ASSAULT', 2: 'BATTERY', 3: 'BURGLARY',
        4: 'CONCEALED CARRY LICENSE VIOLATION', 5: 'CRIM SEXUAL ASSAULT',
        6: 'CRIMINAL DAMAGE', 7: 'CRIMINAL SEXUAL ASSAULT', 8: 'CRIMINAL TRESPASS',
        9: 'DECEPTIVE PRACTICE', 10: 'DOMESTIC VIOLENCE', 11: 'GAMBLING',
        12: 'HOMICIDE', 13: 'HUMAN TRAFFICKING', 14: 'INTERFERENCE WITH PUBLIC OFFICER',
        15: 'INTIMIDATION', 16: 'KIDNAPPING', 17: 'LIQUOR LAW VIOLATION',
        18: 'MOTOR VEHICLE THEFT', 19: 'NARCOTICS', 20: 'NON - CRIMINAL',
        21: 'NON-CRIMINAL', 22: 'NON-CRIMINAL (SUBJECT SPECIFIED)', 23: 'OBSCENITY',
        24: 'OFFENSE INVOLVING CHILDREN', 25: 'OTHER NARCOTIC VIOLATION',
        26: 'OTHER OFFENSE', 27: 'PROSTITUTION', 28: 'PUBLIC INDECENCY',
        29: 'PUBLIC PEACE VIOLATION', 30: 'RITUALISM', 31: 'ROBBERY',
        32: 'SEX OFFENSE', 33: 'STALKING', 34: 'THEFT', 35: 'WEAPONS VIOLATION'
    }
    
    top_5_crimes = [
        (crime_type_mapping[int(i)], float(predictions[0][int(i)]))
        for i in top_5_indices[0]
    ]
    return top_5_crimes

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    lat = data['latitude']
    lon = data['longitude']
    input_data = preprocess_input(lat, lon)
    top_5_crimes = predict_crime(input_data)
    return jsonify(top_5_crimes)

if __name__ == '__main__':
    app.run(debug=True)
