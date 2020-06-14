import sqlite3


class DBConnector:
    database = './betaDB.db'
    dbtime = "0"
    temp = "0"
    hum = "0"
    press = "0"

    def readDB(self):
        try:
            conn = sqlite3.connect(self.database)
            curs = conn.cursor()
            for row in curs.execute("SELECT * FROM stuffToPlot ORDER BY datestamp DESC LIMIT 1"):
                self.dbtime = str(row[1])
                self.temp = round(row[3], 1)
                self.hum = round(row[5], 1)
                self.press = round(row[7], 1)
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def getValues(self):
        self.readDB()
        return self.dbtime, self.temp, self.hum, self.press

    def lastSixHours(self):
        pass
