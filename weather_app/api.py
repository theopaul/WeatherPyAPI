import os
import requests
from typing import Dict, Any, Optional, Tuple
import logging
from urllib.parse import quote

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WeatherAPI:
    """Class for interacting with OpenWeatherMap API"""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5/"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the WeatherAPI with API key"""
        # Use the provided API key or get from environment variable
        self.api_key = api_key or os.environ.get('OPENWEATHER_API_KEY')
        
        if not self.api_key:
            raise ValueError("API key must be provided either as a parameter or as an environment variable 'OPENWEATHER_API_KEY'")
    
    def get_current_weather(self, city: str, units: str = "metric") -> Tuple[bool, Dict[str, Any]]:
        """Fetch current weather data for a city
        
        Args:
            city: Name of the city to get weather for
            units: Unit system (metric, imperial, standard)
            
        Returns:
            Tuple of (success, data), where:
            - success: Boolean indicating if the API call succeeded
            - data: Weather data dictionary if successful, error message if failed
        """
        try:
            url = f"{self.BASE_URL}weather?q={quote(city)}&appid={self.api_key}&units={units}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                logger.info(f"Successfully fetched weather data for {city}")
                return True, data
            else:
                error_msg = f"Error {data.get('cod')}: {data.get('message', 'Unknown error')}"
                logger.error(error_msg)
                return False, {"error": error_msg}
                
        except requests.RequestException as e:
            error_msg = f"Network error occurred: {str(e)}"
            logger.error(error_msg)
            return False, {"error": error_msg}
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return False, {"error": error_msg}
    
    def get_forecast(self, city: str, days: int = 5, units: str = "metric") -> Tuple[bool, Dict[str, Any]]:
        """Fetch 5-day forecast data for a city
        
        Args:
            city: Name of the city to get forecast for
            days: Number of days (max 5)
            units: Unit system (metric, imperial, standard)
            
        Returns:
            Tuple of (success, data), where:
            - success: Boolean indicating if the API call succeeded
            - data: Forecast data dictionary if successful, error message if failed
        """
        try:
            url = f"{self.BASE_URL}forecast?q={quote(city)}&cnt={days*8}&appid={self.api_key}&units={units}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                logger.info(f"Successfully fetched forecast data for {city}")
                return True, data
            else:
                error_msg = f"Error {data.get('cod')}: {data.get('message', 'Unknown error')}"
                logger.error(error_msg)
                return False, {"error": error_msg}
                
        except requests.RequestException as e:
            error_msg = f"Network error occurred: {str(e)}"
            logger.error(error_msg)
            return False, {"error": error_msg}
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return False, {"error": error_msg}
    
    def get_by_coordinates(self, lat: float, lon: float, units: str = "metric") -> Tuple[bool, Dict[str, Any]]:
        """Fetch weather data by geographical coordinates
        
        Args:
            lat: Latitude of the location
            lon: Longitude of the location
            units: Unit system (metric, imperial, standard)
            
        Returns:
            Tuple of (success, data), where:
            - success: Boolean indicating if the API call succeeded
            - data: Weather data dictionary if successful, error message if failed
        """
        try:
            url = f"{self.BASE_URL}weather?lat={lat}&lon={lon}&appid={self.api_key}&units={units}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                logger.info(f"Successfully fetched weather data for coordinates ({lat}, {lon})")
                return True, data
            else:
                error_msg = f"Error {data.get('cod')}: {data.get('message', 'Unknown error')}"
                logger.error(error_msg)
                return False, {"error": error_msg}
                
        except requests.RequestException as e:
            error_msg = f"Network error occurred: {str(e)}"
            logger.error(error_msg)
            return False, {"error": error_msg}
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return False, {"error": error_msg}
