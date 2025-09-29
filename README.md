# CloudCast - Advanced Weather Logger

A comprehensive weather logging website that fetches live weather data, provides forecasts, stores data in CSV format, and offers advanced data visualization with intelligent weather alerts.

## Features

- 🌤️ **Live Weather Data**: Fetch current weather conditions using OpenWeather API
- 🔮 **7-Day Forecast**: Get detailed weather forecasts for the next week
- 🚨 **Smart Weather Alerts**: Intelligent alerts for extreme temperatures, humidity, and wind conditions
- 📊 **Advanced Data Visualization**: Interactive graphs for temperature, humidity, and wind speed trends
- 📈 **Historical Data Management**: View, filter, and download weather history in CSV format
- 🌙 **Dark/Light Mode**: Toggle between light and dark themes with persistent preferences
- 📱 **Responsive Design**: Mobile-friendly interface that works on all devices
- 💾 **Data Persistence**: Automatic CSV logging of all weather queries
- 🔍 **Advanced Filtering**: Filter weather history by city, date range, and parameters
- 🗺️ **Location Services**: Get precise coordinates for any city worldwide
- 📊 **Data Analytics**: Clear history and generate comprehensive weather reports

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get OpenWeather API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key from the dashboard
4. **Note**: The application comes with a pre-configured API key, but you can replace it in `script.py` if needed

### 3. Run the Application

**Option 1: Using Python directly**
```bash
python script.py
```

**Option 2: Using the provided batch file (Windows)**
```bash
start.bat
```

The application will be available at `http://localhost:5000`

### 4. Quick Start Guide

1. **First Launch**: The application will automatically create the `weather_data.csv` file
2. **Get Weather**: Enter any city name (e.g., "London", "New York", "Tokyo")
3. **View Alerts**: Check for any weather alerts that appear automatically
4. **Explore Forecast**: Use the forecast feature to see upcoming weather
5. **Analyze Data**: Use the history and graphs sections to analyze your weather data

## Usage

### Basic Weather Operations
1. **Fetch Current Weather**: Enter a city name and click "Get Weather" to fetch current conditions
2. **Get Weather Forecast**: Use the forecast feature to get 7-day weather predictions
3. **View Weather Alerts**: The system automatically displays intelligent alerts for extreme conditions
4. **Get City Coordinates**: Access precise location data for any city worldwide

### Data Management
5. **View History**: Navigate to the History tab to see all recorded weather data
6. **Filter Data**: Use advanced filtering by city, date range, or weather parameters
7. **Clear History**: Remove all stored weather data with the clear history function
8. **Download Data**: Export your weather data as a CSV file for external analysis

### Visualization & Analytics
9. **Generate Graphs**: Create interactive visualizations for temperature, humidity, and wind speed trends
10. **Data Analytics**: Access dedicated pages for comprehensive weather data analysis
11. **Toggle Theme**: Use the moon/sun icon to switch between light and dark modes

## File Structure

```
Cloud_Cast/
├── script.py              # Flask backend application with weather API integration
├── requirements.txt       # Python dependencies (Flask, requests, matplotlib)
├── start.bat             # Windows batch file for easy startup
├── weather_data.csv       # Auto-generated CSV file (created on first use)
├── index.html            # Root HTML file (alternative entry point)
├── style.css             # Additional CSS styling
├── templates/
│   └── index.html         # Main HTML template with weather interface
└── static/
    └── style.css          # CSS styling with dark/light mode support
```

## API Endpoints

### Core Weather Functions
- `GET /` - Main page with weather form and history
- `POST /fetch_weather` - Fetch current weather data for a city
- `POST /fetch_forecast` - Fetch 7-day weather forecast for a city
- `GET /get_city_coordinates` - Get precise coordinates for any city

### Data Management
- `GET /get_history` - Retrieve all weather history data
- `GET /filter_history` - Filter weather history by city, date range, or parameters
- `POST /clear_history` - Clear all weather history data
- `GET /download_csv` - Download weather data as CSV file

### Visualization & Analytics
- `GET /generate_graph` - Generate interactive graphs for temperature, humidity, or wind speed
- `GET /history` - Dedicated history page with advanced filtering
- `GET /graphs` - Dedicated graphs page for data visualization

## Key Features Explained

### 🚨 Smart Weather Alerts
The system automatically detects and alerts users about:
- **Temperature Alerts**: Extreme heat (>35°C), freezing conditions (<0°C), and hot weather warnings (>30°C)
- **Humidity Alerts**: High humidity (>80%) and dry conditions (<30%)
- **Wind Alerts**: Strong winds (>15 m/s) with safety warnings

### 🔮 7-Day Forecast
- Detailed hourly forecasts for the next week
- Temperature, humidity, wind speed, and weather descriptions
- Visual weather icons for easy interpretation

### 🔍 Advanced Data Filtering
- Filter by specific cities
- Date range filtering for historical analysis
- Parameter-specific filtering for targeted data analysis

### 📊 Intelligent Data Visualization
- Interactive graphs showing weather trends over time
- Multiple parameter visualization (temperature, humidity, wind speed)
- High-resolution graph generation with professional styling

## Technologies Used

- **Backend**: Flask (Python) with advanced routing
- **Frontend**: HTML5, CSS3, JavaScript with responsive design
- **Data Visualization**: Matplotlib with high-DPI graph generation
- **API Integration**: OpenWeatherMap with geocoding and forecast APIs
- **Data Storage**: CSV files with automatic header management
- **UI/UX**: Dark/Light mode with persistent user preferences

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## License

This project is open source and available under the MIT License.