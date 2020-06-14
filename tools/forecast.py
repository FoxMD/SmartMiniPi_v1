import requests
import json
import time


class Forecast:
    api_key = "Your key"
    temp = 0
    min_temp = 0
    max_temp = 0
    weather = " "
    feels_like = 0
    pressure = 0
    humidity = 0
    wind_speed = 0
    wind_direction = 0
    wind_gust = 0
    rain_1h = 0
    clouds = 0
    country = " "
    sunrise = 0
    sunset = 0
    city = " "

    def __init__(self):
        with open("E:\\Programming\\PycharmProjects\\WebServer\\key.txt", "r") as file:
            key = file.readline()
            print(key)
            self.api_key = str(key)

    def getForecast(self, name="Bautzen", type="partial"):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = name  # input("Enter city name : ")
        complete_url = base_url + "appid=" + self.api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        print(x)
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"] - 273.15
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]

            # print following values
            print(" Temperature (in celsius unit) = " +
                  str(current_temperature) +
                  "\n atmospheric pressure (in hPa unit) = " +
                  str(current_pressure) +
                  "\n humidity (in percentage) = " +
                  str(current_humidity) +
                  "\n description = " +
                  str(weather_description))
            if type == "partial":
                return current_temperature, current_pressure, current_humidity, weather_description
            elif type == "full":
                return x
        else:
            print(" City Not Found ")

    def parseWeatherForecast(self, forecast):
        y = forecast["main"]
        self.temp = y["temp"] - 273.15
        self.min_temp = y["temp_min"] - 273.15
        self.max_temp = y["temp_max"] - 273.15
        self.feels_like = y["feels_like"] - 273.15
        self.pressure = y["pressure"]
        self.humidity = y["humidity"]

        y = forecast["wind"]
        self.wind_speed = y["speed"]
        self.wind_direction = y["deg"]
        try:
            self.wind_gust = y["gust"]
        except KeyError as e:
            self.wind_gust = "None"
            print(e)

        try:
            y = forecast["rain"]
            self.rain_1h = y["1h"]
        except KeyError as e:
            self.rain_1h = "None"

        y = forecast["clouds"]
        self.clouds = y["all"]

        y = forecast["sys"]
        self.country = y["country"]
        self.sunrise = y["sunrise"]
        self.sunset = y["sunset"]

        self.city = str(forecast["name"])

        z = forecast["weather"]
        self.weather = z[0]["description"]
