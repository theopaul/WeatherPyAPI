from typing import Dict, Any, List
from datetime import datetime
import json

class WeatherFormatter:
    """Format weather data for display"""
    
    @staticmethod
    def format_current_weather(data: Dict[str, Any], city: str, detailed: bool = False) -> str:
        """Format current weather data for user-friendly display"""
        main_data = data.get("main", {})
        weather_data = data.get("weather", [{}])[0]
        wind_data = data.get("wind", {})
        sys_data = data.get("sys", {})
        
        temperature = main_data.get("temp", "N/A")
        feels_like = main_data.get("feels_like", "N/A")
        pressure = main_data.get("pressure", "N/A")
        humidity = main_data.get("humidity", "N/A")
        weather_description = weather_data.get("description", "N/A")
        
        # Basic output for all cases
        output = [
            f"\n📍 Weather in {city.title()}, {sys_data.get('country', '')}:",
            f"🌡️ Temperature: {temperature}°C",
            f"🤔 Feels like: {feels_like}°C",
            f"💧 Humidity: {humidity}%",
            f"🌬️ Pressure: {pressure} hPa",
            f"☁️ Conditions: {weather_description.capitalize()}"
        ]
        
        # Add more details if requested
        if detailed:
            wind_speed = wind_data.get("speed", "N/A")
            wind_direction = wind_data.get("deg", "N/A")
            visibility = data.get("visibility", "N/A")
            if visibility != "N/A":
                visibility = visibility / 1000  # Convert to km
                
            sunrise = sys_data.get("sunrise", None)
            sunset = sys_data.get("sunset", None)
            
            if sunrise:
                sunrise_time = datetime.fromtimestamp(sunrise).strftime('%H:%M')
                output.append(f"🌅 Sunrise: {sunrise_time}")
            
            if sunset:
                sunset_time = datetime.fromtimestamp(sunset).strftime('%H:%M')
                output.append(f"🌇 Sunset: {sunset_time}")
                
            output.extend([
                f"💨 Wind: {wind_speed} m/s at {wind_direction}°",
                f"👁️ Visibility: {visibility} km" if visibility != "N/A" else ""
            ])
        
        return "\n".join([line for line in output if line])
    
    @staticmethod
    def format_forecast(data: Dict[str, Any], city: str) -> str:
        """Format 5-day forecast data for user-friendly display"""
        forecast_list = data.get("list", [])
        city_data = data.get("city", {})
        
        if not forecast_list:
            return "No forecast data available."
        
        # Group forecasts by day
        days = {}
        for item in forecast_list:
            dt = datetime.fromtimestamp(item.get("dt", 0))
            day_key = dt.strftime('%Y-%m-%d')
            
            if day_key not in days:
                days[day_key] = []
            
            days[day_key].append(item)
        
        # Create output
        output = [f"\n🔮 5-Day Forecast for {city.title()}, {city_data.get('country', '')}:\n"]
        
        for day_key, items in days.items():
            day_name = datetime.strptime(day_key, '%Y-%m-%d').strftime('%A, %b %d')
            output.append(f"📆 {day_name}:")
            
            # Get min and max temps for the day
            temps = [item.get("main", {}).get("temp") for item in items if "main" in item]
            if temps:
                avg_temp = sum(temps) / len(temps)
                output.append(f"   🌡️ Average Temp: {avg_temp:.1f}°C")
            
            # Get the most common weather condition for the day
            conditions = [item.get("weather", [{}])[0].get("description", "") for item in items]
            if conditions:
                most_common = max(set(conditions), key=conditions.count)
                output.append(f"   ☁️ Conditions: {most_common.capitalize()}")
                
            output.append("")
        
        return "\n".join(output)
    
    @staticmethod
    def format_as_json(data: Dict[str, Any], pretty: bool = True) -> str:
        """Format weather data as JSON"""
        if pretty:
            return json.dumps(data, indent=2)
        return json.dumps(data)
