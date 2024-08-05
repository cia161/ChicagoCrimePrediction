from flask import Flask, render_template, json, jsonify
import pandas as pd
import plotly
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json

app = Flask(__name__)

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
    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)  # Correct usage
    return render_template('heatmap.html', plot=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)
