from flask import Flask, jsonify, request
#from bs4 import BeautifulSoup
import requests
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"home": "weather API running"})

@app.route('/forecast')
def fetch_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"Error": "lat and lon are required"}), 400
    
    points_url = f"https://api.weather.gov/points/{lat}, {lon}"
    points_resp = requests.get(points_url)

    if points_resp.status_code != 200:
        return jsonify({"error": "Invalid location"}), 400
    
    points_data = points_resp.json()

    grid_id = points_data["properties"]["gridId"]
    grid_x = points_data["properties"]["gridX"]
    grid_y = points_data["properties"]["gridY"]

    forecast_url = f'https://api.weather.gov/gridpoints/{grid_id}/{grid_x},{grid_y}/forecast'
    forecast_resp = requests.get(forecast_url)

    if forecast_resp.status_code != 200:
        return jsonify({"error": "Failed to fetch weather data"})
    data = forecast_resp.json()
    
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
