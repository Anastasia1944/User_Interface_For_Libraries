import pyodbc
from datetime import datetime


class Sql:
    def __init__(self, database, server="LAPTOP-IIPUTD84"):
        self.cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                   "Server=" + server + ";"
                                    "Database=" + database + ";"
                                    "Trusted_Connection=yes;")
        self.query = "-- {}\n\n-- Made in Python".format(datetime.now()
                                                         .strftime("%d/%m/%Y"))
