from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()  # load .env file

app = Flask(__name__)

def get_coordinates(city, api_key):
    geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    try:
        response = requests.get(geo_url)
        response.raise_for_status()
        data = response.json()
        if not data:
            return None, None
        return data[0]['lat'], data[0]['lon']
    except requests.RequestException:
        return None, None

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        return jsonify({'error': 'API key not found'}), 500

    lat, lon = get_coordinates(city, api_key)
    if lat is None or lon is None:
        return jsonify({'error': f'City "{city}" not found'}), 404

    onecall_url = (
        f"https://api.openweathermap.org/data/3.0/onecall?"
        f"lat={lat}&lon={lon}&exclude=minutely,hourly,daily,alerts&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(onecall_url)
        response.raise_for_status()
        data = response.json()
        current = data.get('current', {})
        weather_info = {
            'city': city,
            'temperature': current.get('temp'),
            'humidity': current.get('humidity'),
            'description': current.get('weather', [{}])[0].get('description')
        }
        return jsonify(weather_info)
    except requests.RequestException as e:
        return jsonify({'error': 'Failed to fetch weather data', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
