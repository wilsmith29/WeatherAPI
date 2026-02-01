## Weather Lookup App

A full-stack Flask web application that retrieves real-time weather forcasts
using the National Weather Service API.

This app allows users to enter a U.S. ZIP Code and view a structured multi-day 
forecast in a clean, styled interface.

---

## Live Demo

https://weatherapi-nxz3.onrender.com

---

## Features
- ZIP Code -> Latitude/Longitude conversion
- Real-time forecast retrieval from the National Weather Service
- Structured multi-period forecast display
- Custom CSS styling with gradient + glassmorphism UI
- Error handling for invalid ZIP codes
- Logging for debugging and observability
- Deployed with auto-deploy enabled via GitHub

---

## How It Works
1. User enters a ZIP code.
2. Backend calls an external geolocation API to convert ZIP -> coordinates.
3. Coordinates are used to query the National Weather Service API.
4. Forecast data is parsed and formatted.
5. Results are rendered using Jinja templates.

---

## Tech Stack
- Python
- Flask
- HTML/CSS
- Jinja2
- National Weather Service API
- Render (deployment)
- GitHub (version control + auto deploy)

---

## Run Locally

```bash
git clone https://github.com/wilsmith29/WeatherAPI.git
cd WeatherAPI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
Open http://127.0.0.1:5000