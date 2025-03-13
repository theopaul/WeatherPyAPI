import os
import json
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime

def save_to_file(data: Dict[str, Any], filename: str) -> bool:
    """Save weather data to a file
    
    Args:
        data: Weather data dictionary
        filename: Name of the file to save to
        
    Returns:
        Boolean indicating if the save was successful
    """
    try:
        # Make sure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        # Add timestamp to data
        data_with_timestamp = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        with open(filename, 'w') as f:
            json.dump(data_with_timestamp, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving data to file: {str(e)}")
        return False

def load_from_file(filename: str) -> Optional[Dict[str, Any]]:
    """Load weather data from a file
    
    Args:
        filename: Name of the file to load from
        
    Returns:
        Weather data dictionary if successful, None if failed
    """
    try:
        if not os.path.exists(filename):
            return None
            
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data from file: {str(e)}")
        return None

def get_unit_symbol(unit_system: str) -> Tuple[str, str, str]:
    """Get the appropriate units for temperature, speed, and pressure based on the unit system
    
    Args:
        unit_system: Unit system (metric, imperial, standard)
        
    Returns:
        Tuple of (temperature unit, speed unit, pressure unit)
    """
    if unit_system == "imperial":
        return "°F", "mph", "hPa"
    elif unit_system == "metric":
        return "°C", "m/s", "hPa"
    else:  # standard
        return "K", "m/s", "hPa"

def get_wind_direction(degrees: float) -> str:
    """Convert wind direction in degrees to cardinal direction
    
    Args:
        degrees: Wind direction in degrees
        
    Returns:
        Cardinal direction (N, NE, E, etc.)
    """
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
                 "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / (360 / len(directions))) % len(directions)
    return directions[index]
