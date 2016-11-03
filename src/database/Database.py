import mysql.connector


class Database(object):
    cursor = None
    connection = None
    findItemsQuery = "SELECT name, price, description FROM store"
    insertItemsQuery = ("INSERT INTO store "
                        "(name, price, review, gender, birth_date) "
                        "VALUES (%s, %s, %s, %s, %s)")

    @staticmethod
    def initialize():
        Database.connection = mysql.connector.connect(user='store', password='StorePassword123!',
                                                      host='192.168.1.51', database='store')
        Database.cursor = Database.connection.cursor()

    @staticmethod
    def getItems():
        Database.cursor.execute(Database.findItemsQuery)

    @staticmethod
    def closeDB():
        Database.connection.close()

    #@staticmethod
    #def createTable():
    #    Database.curso