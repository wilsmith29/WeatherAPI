from flask import Flask, jsonify
#from bs4 import BeautifulSoup
import requests
app = Flask(__name__)

@app.route('/')
def fetch_weather():
    url = 'https://api.weather.gov/gridpoints/PQR/113,104/forecast'
    data = requests.get(url).json()
    
    periods = data["properties"]["periods"]

    results = []

    for period in periods:
        results.append({
            "name": period["name"],
            "forecast": period["shortForecast"],
            "temperature": period["temperature"]
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
