import requests
import json
import time


class Forecast:
    api_key = "Your key"

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
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]

            # print following values
            print(" Temperature (in celsius unit) = " +
                  str(current_temperature) +
                  "\n atmospheric pressure (in hPa unit) = " +
                  str(current_pressure) +
                  "\n humidity (in percentage) = " +
                  str(current_humidiy) +
                  "\n description = " +
                  str(weather_description))
            if type == "partial":
                return current_temperature, current_pressure, current_humidiy, weather_description
            elif type == "full":
                return x
        else:
            print(" City Not Found ")

    def parseWeatherForecast(self, forecast):
        pass
