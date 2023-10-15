#!/usr/bin/env python

import requests
import time

#LOCATION = '35.199458,-111.6514259' # Flagstaff
LOCATION = '86024'
OUTPUT_FILE = 'weather_data.txt'
LAST_WEATHER_DATA = ''

def get_weather():
    # Update the URL and format parameter to request temperature in Celsius, humidity, and wind speed
    url = f'https://wttr.in/{LOCATION}?format=%C+%t+%w+%h+%P+%p'

    try:
        response = requests.get(url)
        weather_data = response.text.strip()
        return weather_data
    except Exception as e:
        return f'Error: {str(e)}'

def calculate_dew_point(temperature, humidity):
    try:
        temperature = float(temperature)
        humidity = float(humidity)
        dew_point = temperature - ((100 - humidity) / 5)
        return dew_point
    except ValueError:
        return None

def main():
    while True:
        weather_data = get_weather()

        # Extract temperature (T) and relative humidity (H) from the weather data
        data_parts = weather_data.split()
            
        # Extract the numeric part of temperature and humidity
        temperature_str = data_parts[1]
        humidity_str = data_parts[3]
            
        # Remove the '°F' and '%' symbols, then convert to float
        temperature = float(temperature_str[:-2])
        humidity = float(humidity_str[:-1])

        # Calculate the dew point
        dew_point = calculate_dew_point(temperature, humidity)
                   
            
        # Open the file in write mode to clear existing content
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
            timestamp = time.strftime('%H:%M:%S', time.gmtime())  # Use time.gmtime() to get UTC time
            file.write(f'{timestamp} [Weather Data]: {data_parts[0]}, T={data_parts[1]}, Winds {data_parts[2]}, RH={data_parts[3]}, DP={dew_point}°F, Precip={data_parts[5]}, P={data_parts[4]}\n')

            print(f'{timestamp} Weather data written to {OUTPUT_FILE}')

        with open(OUTPUT_FILE, 'r') as f:
            mylist = f.readlines()

        # Poll every 60s
        time.sleep(60)

if __name__ == "__main__":
    main()
