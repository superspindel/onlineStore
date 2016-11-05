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
        Database.connection = mysql.connector.connect(user='storeServer', password='storepassword',
                                                      host='192.168.1.87', database='store')
        Database.cursor = Database.connection.cursor()

    @staticmethod
    def getItems():
        Database.cursor.execute(Database.findItemsQuery)

    @staticmethod
    def closeDB():
        Database.connection.close()

    @staticmethod
    def getCategories():
        Database.cursor.exectute("SELECT name, parent FROM categories")
        catList = Database.setCategoryList(Database.cursor)
        return catList

    @staticmethod
    def setCategoryList(cursor):
        catList = []
        for(name, parent) in cursor:
            Database.insertCatList(name, parent, catList)
        return catList

    @staticmethod
    def insertCatList(name, parent, catlist):
        pass

    @staticmethod
    def getUserInfo():
        Database.cursor.exectute("SELECT * from users;")

