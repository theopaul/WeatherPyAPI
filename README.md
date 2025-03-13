# WeatherPyAPI

<p align="center">
  <img src="https://openweathermap.org/themes/openweathermap/assets/img/logo_white_cropped.png" alt="WeatherPyAPI Logo" width="200"/>
</p>

## Description

WeatherPyAPI is a powerful and user-friendly Python application for fetching and displaying real-time weather data and forecasts from OpenWeatherMap. It supports both command-line and interactive usage, making it ideal for quick weather checks, data analysis, or integration into larger Python projects.

## Features

- **Current Weather Data**: Temperature, humidity, pressure, wind speed, etc.
- **Weather Forecasts**: 5-day weather forecasts
- **Multiple Location Inputs**: Search by city name or geographic coordinates
- **Interactive Mode**: User-friendly interface for interactive weather queries
- **Command-line Interface**: Perfect for scripts and automation
- **Unit Selection**: Support for metric, imperial, and standard units
- **Data Export**: Save weather data to JSON files for further analysis
- **Detailed or Concise Output**: Choose between basic and detailed weather information
- **Proper Error Handling**: Robust error handling for API issues and user input
- **Environment Variable Support**: Secure API key management

## Installation

### Prerequisites

- Python 3.6 or higher
- OpenWeatherMap API key ([Get one here](https://openweathermap.org/api))

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/theopaul/WeatherPyAPI.git
   cd WeatherPyAPI
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API key:
   - Copy `.env.example` to `.env`
   - Add your OpenWeatherMap API key to the `.env` file
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

## Usage

### Interactive Mode

Run the script without any arguments to use the interactive mode:

```bash
python weather.py
```

Follow the prompts to get weather information for any city or location.

### Command-line Mode

Use command-line arguments for scripting or quick queries:

```bash
# Get current weather for a city
python weather.py --city "London"

# Get weather using geographic coordinates
python weather.py --location "51.5074,-0.1278"

# Get detailed weather information in imperial units
python weather.py --city "New York" --units imperial --detailed

# Get 5-day forecast
python weather.py --city "Tokyo" --forecast

# Save weather data to a file
python weather.py --city "Paris" --save weather_data.json

# Output raw JSON data
python weather.py --city "Berlin" --json
```

### API Usage in Your Projects

You can import the modules into your own Python projects:

```python
from weather_app.api import WeatherAPI
from weather_app.formatter import WeatherFormatter

# Initialize API with your key
api = WeatherAPI("your_api_key_here")

# Get current weather
success, data = api.get_current_weather("London", units="metric")
if success:
    # Process the data
    formatted_weather = WeatherFormatter.format_current_weather(data, "London")
    print(formatted_weather)
```

## Command-line Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `--city` | `-c` | City name (e.g., 'London' or 'New York,US') |
| `--location` | `-l` | Latitude and longitude (e.g., '51.5074,-0.1278') |
| `--api-key` | `-k` | OpenWeatherMap API key (optional if set in env) |
| `--units` | `-u` | Units of measurement (metric, imperial, standard) |
| `--detailed` | `-d` | Show detailed weather information |
| `--forecast` | `-f` | Show 5-day weather forecast |
| `--save` | `-s` | Save results to specified file (JSON format) |
| `--json` | `-j` | Output raw JSON data |

## Examples

### Basic Current Weather

```
$ python weather.py --city "London"

📍 Weather in London, GB:
🌡️ Temperature: 12.2°C
🤔 Feels like: 11.5°C
💧 Humidity: 76%
🌬️ Pressure: 1011 hPa
☁️ Conditions: Light rain
```

### Detailed Weather with Forecast

```
$ python weather.py --city "New York" --detailed --forecast

📍 Weather in New York, US:
🌡️ Temperature: 19.8°C
🤔 Feels like: 19.5°C
💧 Humidity: 68%
🌬️ Pressure: 1015 hPa
☁️ Conditions: Clear sky
🌅 Sunrise: 06:15
🌇 Sunset: 19:32
💨 Wind: 2.57 m/s at 180°
👁️ Visibility: 10.0 km

🔮 5-Day Forecast for New York, US:

📆 Wednesday, Sep 13:
   🌡️ Average Temp: 20.5°C
   ☁️ Conditions: Clear sky

📆 Thursday, Sep 14:
   🌡️ Average Temp: 22.1°C
   ☁️ Conditions: Few clouds

...
```

## Contributing

Contributions are welcome! If you'd like to contribute, please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [OpenWeatherMap API](https://openweathermap.org/api) for providing the weather data
- All open-source contributors who have helped improve this project
