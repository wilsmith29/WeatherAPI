from flask import Flask, jsonify, request, render_template
#from bs4 import BeautifulSoup
import requests
import logging
app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

@app.route('/')
def home():
    return render_template("index.html")

def get_coordinates(zip_code):
    url = f"https://api.zippopotam.us/us/{zip_code}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        place = response.json()["places"][0]
        lat = float(place["latitude"])
        lon = float(place["longitude"])

        return lat, lon
    
    except requests.exceptions.RequestException as e:
        logging.error(f"ZIP lookup failed for {zip_code}: {e}")
        return None, None

@app.route('/forecast') #Note: use /forecast?lat=num&lon=num or forecast?zip=num
def fetch_weather():
    zip_code = request.args.get("zip")
    lat = request.args.get("lat")
    lon = request.args.get("lon")
  
    if zip_code:
        if not zip_code.isdigit() or len(zip_code) != 5:
            return jsonify({"error": "Invalid ZIP code"}), 400
        
        lat, lon = get_coordinates(zip_code)

        if not lat or not lon:
            return jsonify({"error": "Could not resolve ZIP code"}), 404
        
    elif lat and lon:
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return jsonify({"error": "Invalid coordinates"}), 400
    else:
        return jsonify({"error": "Provide zip OR lat/lon"}), 400
    
    logging.info(f"Resolved ZIP {zip_code} to lat={lat}, lon={lon}")
    logging.info(f"Requesting forecast from weather.gov for {lat},{lon}")
    
    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    headers = {"User-Agent": "william-weather-api"}
    points_resp = requests.get(points_url, headers=headers, timeout=5)

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
    forecast_data = forecast_resp.json()
    
    periods = forecast_data["properties"]["periods"]

    results = []

    for period in periods:
        results.append({
            "name": period["name"],
            "forecast": period["shortForecast"],
            "temperature": period["temperature"]
        })

    return render_template("forecast.html", forecast=results)

if __name__ == '__main__':
    app.run()
