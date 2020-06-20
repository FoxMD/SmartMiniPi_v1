from flask import Flask, render_template, request
import tools
from datetime import datetime
import json
import time


print("Starting script:" + __name__)
app = Flask(__name__)
myBase = tools.DBConnector()
forecast = tools.Forecast()
item = tools.Item
point = tools.Graphical


@app.route("/info")
def actual():
    dbtime, temp, hum, press = myBase.getValues()

    measured = [
        tools.Item("Time", dbtime),
        tools.Item("Temperature", str(temp) + " °C"),
        tools.Item("Humidity", str(hum) + " %"),
        tools.Item("Pressure", str(press) + " hPa")
    ]

    ftemp, fpress, fhumid, sforecast = forecast.getForecast()
    forecasted = [
        tools.Item("Temperature", str(ftemp) + " °C"),
        tools.Item("Pressure", str(fpress) + "hPa"),
        tools.Item("Humidity", str(fhumid) + " %"),
        tools.Item("Forecast", str(sforecast))
    ]

    return render_template("local.html", head="Pocasi", items=measured, forecast=forecasted)


@app.route("/fromweb")
def fromweb():
    args = request.args
    city = args.get("name")
    if city is None:
        city = "Bautzen"
    print(city)
    myForecast = forecast.getForecast(name=city, type="full")
    forecast.parseWeatherForecast(myForecast)

    temp = forecast.temp
    feel = forecast.feels_like
    min_temp = forecast.min_temp
    max_temp = forecast.max_temp
    press = forecast.pressure
    humid = forecast.humidity
    weather = forecast.weather
    wind = forecast.wind_speed
    wind_dir = forecast.wind_direction
    wind_gust = forecast.wind_gust
    country = str(forecast.city) + " - " + str(forecast.country)
    rain = forecast.rain_1h
    clouds = forecast.clouds
    sunrise = int(forecast.sunrise)
    sunrise = str(datetime.utcfromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S'))
    sunset = int(forecast.sunset)
    sunset = str(datetime.utcfromtimestamp(sunset).strftime('%Y-%m-%d %H:%M:%S'))

    forecasted = [
        tools.Item("Temperature", str(temp) + " °C"),
        tools.Item("Feels like", str(feel) + " °C"),
        tools.Item("Minimum temperature", str(min_temp) + " °C"),
        tools.Item("Maximum temperature", str(max_temp) + " °C"),
        tools.Item("Pressure", str(press) + "hPa"),
        tools.Item("Humidity", str(humid) + " %"),
        tools.Item("Weather", str(weather)),
        tools.Item("Wind", str(wind)),
        tools.Item("Wind direction", str(wind_dir)),
        tools.Item("Wind gusts", str(wind_gust)),
        tools.Item("Rain", str(rain)),
        tools.Item("Clouds", str(clouds)),
        tools.Item("Sunrise", str(sunrise)),
        tools.Item("Sunset", str(sunset)),
        tools.Item("Place", str(country))
    ]

    return render_template("forecast.html", param1=country, items=forecasted)


@app.route("/graphics")
def graphical():
    dbtime, temp, hum, press = myBase.getValues()

    measured = [
        tools.Graphical(20, 10),
        tools.Graphical(8, 15),
        tools.Graphical(17, 20),
        tools.Graphical(13, 25),
    ]

    return render_template("graphics.html", head="Graf", myValues=measured)


@app.route("/")
def start():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)

