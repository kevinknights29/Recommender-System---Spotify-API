import pandas as pd
from flask import Flask, app, render_template

from iTunesXMLToDF import getDfFromXml
from spotifyRecommendations import getRecomendations

itunes_xml = r'../ref/itunes_library.xml'
tracks_data = getDfFromXml(itunes_xml)
recommendations = getRecomendations(tracks_data)

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    index = 0
    return render_template('index.html', tracks=recommendations, index=index)

