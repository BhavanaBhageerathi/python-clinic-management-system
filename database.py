#creating database connectivity
import os

import mysql.connector

class Database:

    def __init__(self):

        self.dbobj = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "clinic_management")
)

        self.dbcursor = self.dbobj.cursor()
        self.__database_name = "clinic_management"

    def get_database_name(self):
        return self.__database_name
        


database = Database()


        



