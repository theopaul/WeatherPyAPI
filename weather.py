import requests

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def fetch_weather(city, api_key):
    complete_url = f"{BASE_URL}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] == 200:
        display_weather(data, city)
    else:
        print(f"Error: {data['cod']} - {data.get('message', 'Unknown error')}")

def display_weather(data, city):
    main_data = data["main"]
    weather_data = data["weather"][0]
    
    temperature = main_data["temp"]
    pressure = main_data["pressure"]
    humidity = main_data["humidity"]
    weather_description = weather_data["description"]
    
    print(f"Weather in {city}:")
    print(f"Temperature: {temperature}°C")
    print(f"Pressure: {pressure} hPa")
    print(f"Humidity: {humidity}%")
    print(f"Description: {weather_description.capitalize()}\n")

if __name__ == "__main__":
    api_key = "b4d919ed01568afb6b3c1adc314de19e"  # Replace with your API key
    while True:
        city = input("Enter city name (or 'exit' to quit): ")
        if city.lower() == 'exit':
            break
        fetch_weather(city, api_key)
