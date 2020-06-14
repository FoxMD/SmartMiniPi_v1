from flask import Flask, render_template, request
import requests
import tools
import json
import time


print("Starting script:" + __name__)
app = Flask(__name__)
myBase = tools.DBConnector()
forecast = tools.Forecast()


class Item:
    def __init__(self, name, value):
        self.name = name
        self.value = value


@app.route("/start")
def hello():
    dbtime, temp, hum, press = myBase.getValues()

    measured = [
        Item("Time", dbtime),
        Item("Temperature", str(temp) + " °C"),
        Item("Humidity", str(hum) + " %"),
        Item("Pressure", str(press) + " hPa")
    ]

    ftemp, fpress, fhumid, sforecast = forecast.getForecast()
    forecasted = [
        Item("Temperature", str(ftemp) + " °C"),
        Item("Pressure", str(fpress) + "hPa"),
        Item("Humidity", str(fhumid) + " %"),
        Item("Forecast", str(sforecast))
    ]

    return render_template("start.html", head="Obyvak", items=measured, forecast=forecasted)


@app.route("/test")
def test():
    args = request.args
    city = args.get("name")
    if city is None:
        city = "Bautzen"
    print(city)
    temp, press, humid, sforecast = forecast.getForecast(name=city)

    forecasted = [
        Item("Temperature", str(temp) + " °C"),
        Item("Pressure", str(press) + "hPa"),
        Item("Humidity", str(humid) + " %"),
        Item("Forecast", str(sforecast))
    ]

    return render_template("test.html", param1=city, items=forecasted)


@app.route("/")
def start():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)

