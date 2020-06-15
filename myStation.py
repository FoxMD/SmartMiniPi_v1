#!/usr/bin/python3
import time
import board
import busio
import adafruit_si7021
import struct, array, io, fcntl, lcddriver, datetime
import sqlite3
import digitalio
import adafruit_bmp280
import adafruit_max31865

# database connection
database = '/home/pi/Documents/Sensors_Database/betaDB.db'
conn = sqlite3.connect(database)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(unix REAL, datestamp TEXT, keyword1 TEXT, value1 REAL, keyword2 TEXT, value2 REAL, keyword3 TEXT, value3 REAL)')
conn.close()

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
h_sensor = adafruit_si7021.SI7021(i2c)

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
p_cs = digitalio.DigitalInOut(board.D24)
p_sensor = adafruit_bmp280.Adafruit_BMP280_SPI(spi, p_cs)

t_cs = digitalio.DigitalInOut(board.D17)
t_sensor = adafruit_max31865.Adafruit_MAX31865_SPI(spi, t_cs)

display = lcddriver.lcd()

while True:
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    dPressure = str(p_sensor.pressure)
    dTemp = str(p_sensor.temperature)
    dHumidity = str(h_sensor.relative_humidity)
    dTime = datetime.datetime.now().time()
    oTemp = str(t_sensor.temperature)

    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("INSERT INTO stuffToPlot (unix, datestamp, keyword1, value1, keyword2, value2, keyword3, value3) VALUES (?,?,?,?,?,?,?,?)", (unix, date, "Temperature", dTemp, "Humidity", dHumidity, "Pressure", dPressure))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()

    display.lcd_display_string("Pressure: " + '%.6s' % dPressure + " hPa", 1)
    display.lcd_display_string("Humidity: " + '%.4s' % dHumidity + " %", 2)
    display.lcd_display_string("Temp in:  " + '%.4s' % dTemp + " " + "Time", 3)
    display.lcd_display_string("Temp out: " + '%.4s' % oTemp + " " + '%.5s' % dTime, 4)
    time.sleep(30)

