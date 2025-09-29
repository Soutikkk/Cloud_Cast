from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import requests
import csv
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
import json

app = Flask(__name__)

# OpenWeather API configuration
API_KEY = "6cc8aa51aea99c9cf8b90546d059dac6"  # OpenWeather API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# CSV file path
CSV_FILE = "weather_data.csv"

def get_weather_data(city_name):
    """Fetch weather data from OpenWeather API"""
    try:
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric'  # Get temperature in Celsius
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract relevant data
        weather_data = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        }
        
        return weather_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing weather data: {e}")
        return None

def get_forecast_data(city_name):
    """Fetch 7-day weather forecast from OpenWeather API"""
    try:
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(FORECAST_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        forecast_list = []
        
        # Process forecast data (5-day forecast with 3-hour intervals)
        for item in data['list'][:8]:  # Get next 7 days (8 * 3-hour intervals = 24 hours)
            forecast_data = {
                'date': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d'),
                'time': datetime.fromtimestamp(item['dt']).strftime('%H:%M'),
                'temperature': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'wind_speed': item['wind']['speed'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon']
            }
            forecast_list.append(forecast_data)
        
        return forecast_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forecast data: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing forecast data: {e}")
        return None

def check_weather_alerts(weather_data):
    """Check for weather alerts based on thresholds"""
    alerts = []
    
    # Temperature alerts
    if weather_data['temperature'] > 35:
        alerts.append({
            'type': 'danger',
            'message': f'🌡️ High Temperature Alert: {weather_data["temperature"]}°C is very hot!',
            'icon': 'fas fa-thermometer-full'
        })
    elif weather_data['temperature'] < 0:
        alerts.append({
            'type': 'warning',
            'message': f'🧊 Freezing Alert: {weather_data["temperature"]}°C is below freezing!',
            'icon': 'fas fa-snowflake'
        })
    elif weather_data['temperature'] > 30:
        alerts.append({
            'type': 'info',
            'message': f'☀️ Hot Weather: {weather_data["temperature"]}°C - Stay hydrated!',
            'icon': 'fas fa-sun'
        })
    
    # Humidity alerts
    if weather_data['humidity'] > 80:
        alerts.append({
            'type': 'info',
            'message': f'💧 High Humidity: {weather_data["humidity"]}% - Very humid conditions',
            'icon': 'fas fa-tint'
        })
    elif weather_data['humidity'] < 30:
        alerts.append({
            'type': 'warning',
            'message': f'🏜️ Low Humidity: {weather_data["humidity"]}% - Dry conditions',
            'icon': 'fas fa-mountain'
        })
    
    # Wind alerts
    if weather_data['wind_speed'] > 15:
        alerts.append({
            'type': 'warning',
            'message': f'💨 Strong Winds: {weather_data["wind_speed"]} m/s - Be cautious!',
            'icon': 'fas fa-wind'
        })
    
    return alerts

def save_to_csv(weather_data):
    """Save weather data to CSV file"""
    file_exists = os.path.exists(CSV_FILE)
    
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['city', 'temperature', 'humidity', 'wind_speed', 'date', 'time', 'description', 'icon']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write header if file is new
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(weather_data)

def read_csv_data():
    """Read all data from CSV file"""
    if not os.path.exists(CSV_FILE):
        return []
    
    data = []
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    
    return data

def create_graph(parameter, data):
    """Create a graph for the specified parameter"""
    if not data:
        return None
    
    # Extract data for plotting
    dates = []
    values = []
    
    for entry in data:
        date_time = f"{entry['date']} {entry['time']}"
        dates.append(datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S'))
        values.append(float(entry[parameter]))
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(dates, values, marker='o', linewidth=2, markersize=6)
    plt.title(f'{parameter.title()} Over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Date & Time', fontsize=12)
    plt.ylabel(parameter.title(), fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Convert plot to base64 string
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return img_base64

@app.route('/')
def index():
    """Main page with weather form and history"""
    weather_data = read_csv_data()
    return render_template('index.html', weather_history=weather_data)

@app.route('/fetch_weather', methods=['POST'])
def fetch_weather():
    """Fetch weather data and save to CSV"""
    city_name = request.form.get('city')
    
    if not city_name:
        return jsonify({'error': 'City name is required'}), 400
    
    # Get weather data from API
    weather_data = get_weather_data(city_name)
    
    if weather_data is None:
        return jsonify({'error': 'Failed to fetch weather data. Please check the city name and try again.'}), 400
    
    # Check for alerts
    alerts = check_weather_alerts(weather_data)
    
    # Save to CSV
    save_to_csv(weather_data)
    
    return jsonify({
        'success': True,
        'data': weather_data,
        'alerts': alerts
    })

@app.route('/fetch_forecast', methods=['POST'])
def fetch_forecast():
    """Fetch 7-day weather forecast"""
    city_name = request.form.get('city')
    
    if not city_name:
        return jsonify({'error': 'City name is required'}), 400
    
    forecast_data = get_forecast_data(city_name)
    
    if forecast_data is None:
        return jsonify({'error': 'Failed to fetch forecast data. Please check the city name and try again.'}), 400
    
    return jsonify({
        'success': True,
        'forecast': forecast_data
    })

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear weather history"""
    try:
        if os.path.exists(CSV_FILE):
            # Keep only the header
            with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['city', 'temperature', 'humidity', 'wind_speed', 'date', 'time', 'description', 'icon']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
        
        return jsonify({'success': True, 'message': 'Weather history cleared successfully!'})
    except Exception as e:
        return jsonify({'error': f'Failed to clear history: {str(e)}'}), 500

@app.route('/filter_history')
def filter_history():
    """Filter weather history by city or date range"""
    city_filter = request.args.get('city', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()
    
    data = read_csv_data()
    filtered_data = data
    
    # Filter by city
    if city_filter:
        filtered_data = [entry for entry in filtered_data if city_filter.lower() in entry['city'].lower()]
    
    # Filter by date range
    if start_date:
        filtered_data = [entry for entry in filtered_data if entry['date'] >= start_date]
    
    if end_date:
        filtered_data = [entry for entry in filtered_data if entry['date'] <= end_date]
    
    return jsonify(filtered_data)

@app.route('/get_city_coordinates')
def get_city_coordinates():
    """Get coordinates for a city using OpenWeather geocoding API"""
    city_name = request.args.get('city', '').strip()
    
    if not city_name:
        return jsonify({'error': 'City name is required'}), 400
    
    try:
        # Use OpenWeather geocoding API
        geocode_url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {
            'q': city_name,
            'limit': 1,
            'appid': API_KEY
        }
        
        response = requests.get(geocode_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data and len(data) > 0:
            coordinates = {
                'lat': data[0]['lat'],
                'lon': data[0]['lon'],
                'name': data[0]['name'],
                'country': data[0].get('country', ''),
                'state': data[0].get('state', '')
            }
            return jsonify({'success': True, 'coordinates': coordinates})
        else:
            return jsonify({'error': 'City not found'}), 404
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to get coordinates: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error getting coordinates: {str(e)}'}), 500

@app.route('/get_history')
def get_history():
    """Get weather history data"""
    data = read_csv_data()
    return jsonify(data)

@app.route('/generate_graph')
def generate_graph():
    """Generate graph for specified parameter"""
    parameter = request.args.get('parameter', 'temperature')
    data = read_csv_data()
    
    if not data:
        return jsonify({'error': 'No data available for graphing'}), 400
    
    graph_base64 = create_graph(parameter, data)
    
    if graph_base64:
        return jsonify({
            'success': True,
            'graph': graph_base64
        })
    else:
        return jsonify({'error': 'Failed to generate graph'}), 400

@app.route('/download_csv')
def download_csv():
    """Download the CSV file"""
    if not os.path.exists(CSV_FILE):
        return jsonify({'error': 'No data file found'}), 404
    
    return send_file(CSV_FILE, as_attachment=True, download_name='weather_data.csv')

@app.route('/history')
def history():
    """Weather history page"""
    weather_data = read_csv_data()
    return render_template('history.html', weather_history=weather_data)

@app.route('/graphs')
def graphs():
    """Graphs page"""
    weather_data = read_csv_data()
    return render_template('graphs.html', weather_history=weather_data)

if __name__ == '__main__':
    # Create CSV file with headers if it doesn't exist
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['city', 'temperature', 'humidity', 'wind_speed', 'date', 'time']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
