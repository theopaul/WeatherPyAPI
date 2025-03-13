#!/usr/bin/env python3

import argparse
import os
from dotenv import load_dotenv
from weather_app.api import WeatherAPI
from weather_app.formatter import WeatherFormatter
from weather_app.utils import save_to_file
from typing import Any, Dict, Optional

# Load environment variables from .env file
load_dotenv()

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Weather information from OpenWeatherMap")
    
    # Required arguments
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--city", help="City name (e.g., 'London' or 'New York,US')")
    group.add_argument("-l", "--location", help="Latitude and longitude (e.g., '51.5074,-0.1278')")
    
    # Optional arguments
    parser.add_argument("-k", "--api-key", help="OpenWeatherMap API key (can also be set as OPENWEATHER_API_KEY env variable)")
    parser.add_argument("-u", "--units", choices=["metric", "imperial", "standard"], 
                       default="metric", help="Units of measurement (default: metric)")
    parser.add_argument("-d", "--detailed", action="store_true", help="Show detailed weather information")
    parser.add_argument("-f", "--forecast", action="store_true", help="Show 5-day weather forecast")
    parser.add_argument("-s", "--save", help="Save results to specified file (JSON format)")
    parser.add_argument("-j", "--json", action="store_true", help="Output raw JSON data")
    
    return parser.parse_args()

def get_weather_data(args) -> Dict[str, Any]:
    """Get weather data based on command line arguments"""
    # Initialize API with key from args or env var
    api = WeatherAPI(args.api_key)
    
    try:
        if args.city:
            # Get weather by city name
            success, data = api.get_current_weather(args.city, args.units)
            if not success:
                print(f"Error: {data.get('error')}")
                return {}
            
            # Get forecast if requested
            if args.forecast:
                forecast_success, forecast_data = api.get_forecast(args.city, units=args.units)
                if forecast_success:
                    data["forecast"] = forecast_data
        else:
            # Get weather by coordinates
            try:
                lat, lon = map(float, args.location.split(','))
                success, data = api.get_by_coordinates(lat, lon, args.units)
                if not success:
                    print(f"Error: {data.get('error')}")
                    return {}
                
                # Get forecast if requested
                if args.forecast:
                    forecast_success, forecast_data = api.get_forecast(f"{lat},{lon}", units=args.units)
                    if forecast_success:
                        data["forecast"] = forecast_data
            except ValueError:
                print("Error: Location should be in format 'latitude,longitude' (e.g., '51.5074,-0.1278')")
                return {}
        
        return data
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {}

def main():
    """Main entry point for the application"""
    args = parse_arguments()
    data = get_weather_data(args)
    
    if not data:
        return
    
    # Get city name for display
    city_name = args.city if args.city else f"coordinates ({args.location})"
    
    # Save data to file if requested
    if args.save:
        if save_to_file(data, args.save):
            print(f"Weather data saved to {args.save}")
    
    # Output JSON if requested
    if args.json:
        print(WeatherFormatter.format_as_json(data))
        return
    
    # Display formatted weather information
    print(WeatherFormatter.format_current_weather(data, city_name, args.detailed))
    
    # Display forecast if available
    if args.forecast and "forecast" in data:
        print(WeatherFormatter.format_forecast(data["forecast"], city_name))

def interactive_mode():
    """Run the application in interactive mode"""
    print("\n🌤️  WeatherPyAPI - Interactive Mode 🌤️\n")
    print("Type 'exit' or 'quit' to exit the application.\n")
    
    # Try to get API key from environment
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    if not api_key:
        api_key = input("Enter your OpenWeatherMap API key: ")
        os.environ['OPENWEATHER_API_KEY'] = api_key
    
    api = WeatherAPI(api_key)
    formatter = WeatherFormatter()
    
    while True:
        choice = input("\nWhat would you like to do?\n1. Current weather by city\n2. Current weather by coordinates\n3. Weather forecast\n4. Exit\nChoice (1-4): ")
        
        if choice in ['4', 'exit', 'quit']:
            print("\nThank you for using WeatherPyAPI! Goodbye!")
            break
        
        units = input("\nChoose units (metric/imperial/standard) [metric]: ").lower() or "metric"
        if units not in ["metric", "imperial", "standard"]:
            print("Invalid unit system. Using metric.")
            units = "metric"
        
        if choice == '1':
            city = input("\nEnter city name (e.g., 'London' or 'New York,US'): ")
            success, data = api.get_current_weather(city, units)
            if success:
                print(formatter.format_current_weather(data, city, detailed=True))
            else:
                print(f"\nError: {data.get('error')}")
                
        elif choice == '2':
            try:
                coords = input("\nEnter coordinates (latitude,longitude, e.g., '51.5074,-0.1278'): ")
                lat, lon = map(float, coords.split(','))
                success, data = api.get_by_coordinates(lat, lon, units)
                if success:
                    print(formatter.format_current_weather(data, f"coordinates ({coords})", detailed=True))
                else:
                    print(f"\nError: {data.get('error')}")
            except ValueError:
                print("\nError: Invalid coordinates format. Should be 'latitude,longitude'.")
                
        elif choice == '3':
            city = input("\nEnter city name for forecast: ")
            success, data = api.get_forecast(city, units=units)
            if success:
                print(formatter.format_forecast(data, city))
            else:
                print(f"\nError: {data.get('error')}")
        else:
            print("\nInvalid choice. Please select 1-4.")

if __name__ == "__main__":
    # Check if command line arguments are provided
    import sys
    if len(sys.argv) > 1:
        main()
    else:
        interactive_mode()
