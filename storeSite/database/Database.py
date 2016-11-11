import mysql.connector
from common.user import user


class Database(object):
    cursor = None
    connection = None
    findItemsQuery = "SELECT name, age from test;"
    insertItemsQuery = ("INSERT INTO store "
                        "(name, price, review, gender, birth_date) "
                        "VALUES (%s, %s, %s, %s, %s)")

    @staticmethod
    def initialize():
        Database.connection = mysql.connector.connect(user='storeserver', password='storepass',
                                                      host='79.136.28.49', database='store')
        Database.cursor = Database.connection.cursor()

    @staticmethod
    def getItems():
        userList = []
        Database.cursor.execute(Database.findItemsQuery)
        for (name, age) in Database.cursor:
            userList.append((name, age))

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
        Database.cursor.execute("SELECT * from user;")
        listan = []
        for(name, age) in Database.cursor:
            listan.append(user(name, age))
        return listan


