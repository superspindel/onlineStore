import mysql.connector


class Database(object):
    cursor = None
    connection = None

    def initialize(self):
        self.connection = mysql.connector.connect(user='root', password='password',
                                                  host='79.136.28.49', database='mydb')
        self.cursor = self.connection.cursor()

    def end(self):
        self.connection.close()
        self.cursor.close()

    def closeDB(self):
        self.connection.close()

    def insert(self, table, data):
        self.cursor.execute("INSERT INTO "+table+" VALUES("+data+")")
        self.connection.commit()
