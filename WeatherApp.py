import tkinter as tk
from tkinter import ttk
import requests

def display_weather(data):
    if data and 'main' in data:
        city_name = data['name']
        country = data['sys']['country']
        temperature_celsius = data['main']['temp'] - 273.15
        weather_condition = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        pressure = data['main']['pressure']

        result = f"City: {city_name}, {country}\n"
        result += f"Temperature: {temperature_celsius:.2f}°C\n"
        result += f"Weather: {weather_condition}\n"
        result += f"Humidity: {humidity}%\n"
        result += f"Wind Speed: {wind_speed} m/s\n"
        result += f"Pressure: {pressure} hPa"
        
        result_label.config(text=result)
    else:
        result_label.config(text="City not found or an error occurred.")

def on_get_weather():
    city = city_entry.get()
    api_key = 'cf837ef98b157befed60a0d522c42471'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    try:
        response = requests.get(url)
        if response.status_code == 401:
            result_label.config(text="Error 401: Unauthorized. Check API key.")
            return
        response.raise_for_status()
        data = response.json()
        display_weather(data)
    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Error: {e}")
    except KeyError:
        result_label.config(text="Invalid response. Please check the city name.")

root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")
root.config(bg="#f0f0f0")
pad_options = {'padx': 10, 'pady': 5}
bold_font = ("Helvetica", 12, "bold")

title_label = tk.Label(root, text="Weather App", font=("Helvetica", 20, "bold"),fg="#5D3FD3", bg="#f0f0f0")
title_label.pack(pady=10)

city_label = tk.Label(root, text="Enter city:", font=("Helvetica", 16),fg="#5D3FD3", bg="#f0f0f0")
city_label.pack(pady=5)

city_entry = tk.Entry(root, font=("Helvetica", 12), bg="navy", fg="white", insertbackground="white")
city_entry.pack(pady=5)

tk.Button(root, text="Get Weather", command=on_get_weather, fg="#0000FF", bg="white", font=bold_font).pack(**pad_options)

result_label = tk.Label(root, text="", font=("Helvetica", 12), wraplength=300, justify="left",fg="#0000FF", bg="#f0f0f0")
result_label.pack(pady=10)

root.mainloop()
