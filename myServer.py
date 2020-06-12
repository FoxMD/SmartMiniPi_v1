from flask import Flask, render_template, request
import requests
import json
import time
import sqlite3

print("Starting script:" + __name__)
app = Flask(__name__)


def getValues():
    database = './betaDB.db'
    try:
        conn = sqlite3.connect(database)
        curs = conn.cursor()
        for row in curs.execute("SELECT * FROM stuffToPlot ORDER BY datestamp DESC LIMIT 1"):
            dbtime = str(row[1])
            temp = round(row[3], 1)
            hum = round(row[5], 1)
            press = round(row[7], 1)
    except sqlite3.Error as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()

    return dbtime, temp, hum, press


def getForecast():
    api_key = "3d3ef5783c2114c889d915ac669ef188"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "bautzen"  # input("Enter city name : ")
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    print(x)
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]

        # print following values
        print(" Temperature (in kelvin unit) = " +
              str(current_temperature) +
              "\n atmospheric pressure (in hPa unit) = " +
              str(current_pressure) +
              "\n humidity (in percentage) = " +
              str(current_humidiy) +
              "\n description = " +
              str(weather_description))

        return current_temperature, current_pressure, current_humidiy, weather_description

    else:
        print(" City Not Found ")


class DBValues:
    def __init__(self):
        pass
        # self.temperature = temperature
        # self.humidity = humidity
        # self.pressure = pressure
        # self.time = time

    def getLastValues(self):
        pass
        # return time, temp, hum, press


class Item:
    def __init__(self, name, value):
        self.name = name
        self.value = value


@app.route("/start")
def hello():
    dbtime, temp, hum, press = getValues()

    items = [
        Item("Time", dbtime),
        Item("Temperature", str(temp) + " °C"),
        Item("Humidity", str(hum) + " %"),
        Item("Pressure", str(press) + " hPa")
    ]
    print(getForecast())
    return render_template("start.html", head="Obyvak", items=items)


@app.route("/test")
def test():
    args = request.args
    name = args.get("name")
    print(name)
    return render_template("test.html", param1=name)


@app.route("/")
def start():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)
