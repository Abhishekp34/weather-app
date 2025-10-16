from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone
import traceback

load_dotenv()

app = Flask(__name__)

# Configure logging to a file with rotation
log_handler = RotatingFileHandler('app.log', maxBytes=10*1024*1024, backupCount=5)
log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

@app.before_request
def log_request_info():
    app.logger.info(f"Request: {request.method} {request.url}")

def get_coordinates(city, api_key):
    geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    try:
        response = requests.get(geo_url)
        response.raise_for_status()
        data = response.json()
        if not data:
            app.logger.warning(f"Geocoding: No results for city '{city}'")
            return None, None
        return data[0]['lat'], data[0]['lon']
    except requests.RequestException as e:
        app.logger.error(f"Geocoding API request failed: {e}")
        return None, None

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city or not city.strip():
        app.logger.warning("Bad request: City parameter missing or empty")
        return jsonify({'error': 'City parameter is required and must be a non-empty string'}), 400

    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        app.logger.error('API key not found in environment')
        return jsonify({'error': 'API key not found'}), 500

    lat, lon = get_coordinates(city, api_key)
    if lat is None or lon is None:
        app.logger.info(f"City not found or geocoding failed: {city}")
        return jsonify({'error': f'City "{city}" not found or geocoding failed'}), 404

    onecall_url = (
        f"https://api.openweathermap.org/data/3.0/onecall?"
        f"lat={lat}&lon={lon}&exclude=minutely,hourly,daily,alerts&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(onecall_url)
        response.raise_for_status()
        data = response.json()

        current = data.get('current')
        if not current:
            app.logger.error("Current weather data missing from One Call API response")
            return jsonify({'error': 'Current weather data unavailable'}), 502

        weather_info = {
            'city': city,
            'temperature': current.get('temp'),
            'humidity': current.get('humidity'),
            'description': current.get('weather', [{}])[0].get('description')
        }
        app.logger.info(f"Weather data fetched successfully for city: {city}")
        return jsonify(weather_info)

    except requests.HTTPError as http_err:
        error_msg = f"HTTP error occurred: {http_err} Response: {response.text}"
        app.logger.error(error_msg)
        status_code = response.status_code if response else 500
        return jsonify({'error': 'Weather API request failed', 'details': response.text}), status_code

    except requests.RequestException as e:
        app.logger.error(f"Request exception: {e}")
        return jsonify({'error': 'Failed to fetch weather data', 'details': str(e)}), 500

    except Exception as e:
        tb = traceback.format_exc()
        app.logger.error(f"Unexpected server error: {e}\n{tb}")
        return jsonify({'error': 'Unexpected server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
