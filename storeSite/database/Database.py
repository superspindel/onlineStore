import mysql.connector


class Database(object):
    cursor = None
    connection = None

    """
    Function name: initialize
    Input variables: self
    Info: Creates the connection to the database and sets the connection and cursor variable
    """
    def initialize(self):
        self.connection = mysql.connector.connect(user='storeserver', password='password123',
                                                  host='79.136.28.49', database='storeDB')
        self.cursor = self.connection.cursor()

    """
    Function name: end
    Input variables: self
    Info: Closes the objects connection to the database
    """
    def end(self):
        self.connection.close()
        self.cursor.close()

    """
    Function name: insert
    Input variables: self, the table, the data
    Info: Inserts the data to the table and commits the changes.
    """
    def insert(self, table, data):
        sqlInsert = "INSERT INTO {} VALUES({})"
        self.cursor.execute(sqlInsert.format(table, data))
        self.connection.commit()

    """
    Function name: select
    Input variables: self, parameter to get from select, table to get it from, value of column, data for what the columnvalue should be.
    Info: The cursor executes a select statement and gets filled with the data that is returned from the database
    """
    def selectWhere(self, parameter, table, value, data):
        sqlSelectWhere = "SELECT {} FROM {} WHERE {} = {}"
        self.cursor.execute(sqlSelectWhere.format(parameter, table, value, data))

    def select(self, parameter, table):
        sqlSelect = "SELECT {} FROM {}"
        self.cursor.execute(sqlSelect.format(parameter, table))