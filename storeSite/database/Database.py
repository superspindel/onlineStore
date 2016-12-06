import mysql.connector


class Database(object):
    cursor = None
    connection = None

    def __init__(self):
        self.connection = mysql.connector.connect(user='storeserver', password='password123',
                                                  host='79.136.28.49', database='storeDB')
        self.cursor = self.connection.cursor(buffered=True)
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

    def commit(self):
        self.connection.commit()

    def startTransaction(self):
        self.commit()
        self.connection.start_transaction()
    """
    Function name: select
    Input variables: self, parameter to get from select, table to get it from, value of column, data for what the columnvalue should be.
    Info: The cursor executes a select statement and gets filled with the data that is returned from the database
    """
    def selectWhere(self, parameter, table, value1, value2):
        sqlSelectWhere = "SELECT {} FROM {} WHERE {} = {}"
        self.cursor.execute(sqlSelectWhere.format(parameter, table, value1, value2))
		
    def selectWhereAnd(self, parameter, table, value1, value2, value3, value4):
        sqlSelectWhereAnd = "SELECT {} FROM {} WHERE {} = {} AND {} = {}"
        self.cursor.execute(sqlSelectWhereAnd.format(parameter, table, value1, value2, value3, value4))
    
    def selectWhereAndNot(self, parameter, table, value1, value2, value3, value4):
        sqlSelectWhereAnd = "SELECT {} FROM {} WHERE {} = {} AND {} <> {}"
        self.cursor.execute(sqlSelectWhereAnd.format(parameter, table, value1, value2, value3, value4))

    def selectWhereAndLargerThenZero(self, parameter, table, value1, value2, value3):
        selectWhereAndLargerThenZero = "SELECT {} FROM {} where {} = {} AND {} > 0"
        self.cursor.execute(selectWhereAndLargerThenZero.format(parameter, table, value1, value2, value3))

    def select(self, parameter, table):
        sqlSelect = "SELECT {} FROM {}"
        self.cursor.execute(sqlSelect.format(parameter, table))

    def selectGroup(self, sortParameter,concatParameter,table, value1, value2 ):
        sqlSelectGroup = "SELECT {}, group_concat({}) from {} where {} = {} group by {}"
        self.cursor.execute(sqlSelectGroup.format(sortParameter, concatParameter, table, value1, value2, sortParameter))

    def search(self, parameter, table, value1, value2):
        sqlSearch = "SELECT {} from {} where {} like"+"\""+"%{}%"+"\""
        self.cursor.execute(sqlSearch.format(parameter, table, value1, value2))

    def update(self, table, colName, setValue, value1, value2):
        sqlUpdate = "UPDATE {} SET {} = {} where {} = {}"
        self.cursor.execute(sqlUpdate.format(table, colName, setValue, value1, value2))

    def updateAnd(self, table, colname, setvalue, value1, value2, value3, value4):
        sqlUpdate = "UPDATE {} SET {} = {} where {} = {} and {} = {}"
        self.cursor.execute(sqlUpdate.format(table, colname, setvalue, value1, value2, value3, value4))

    def nestedSelect(self, parameters, table, value1, value2, value3, nestedParameters, nestedTable, nestedValue1,
                     nestedValue2):
        sqlNestedSelect = "SELECT {} FROM {} WHERE {} = {} AND {} = (SELECT {} from {} where {} = {})"
        self.cursor.execute(sqlNestedSelect.format(parameters, table, value1, value2, value3, nestedParameters,
                                                   nestedTable, nestedValue1, nestedValue2))
    def deleteFromAnd(self, table, value1, value2, value3, value4):
        sqlDelete = "DELETE FROM {} WHERE {} = {} AND {} = {}"
        self.cursor.execute(sqlDelete.format(table, value1, value2, value3, value4))

    def deleteFrom(self, table, value1, value2):
        sqlDelete = "DELETE FROM {} WHERE {} = {}"
        self.cursor.execute(sqlDelete.format(table, value1, value2))

    def selectWhereAnd(self, parameter, table, value1, value2, value3, value4):
        sqlSelectWhereAnd = "SELECT {} FROM {} WHERE {} = {} AND {} = {}"
        self.cursor.execute(sqlSelectWhereAnd.format(parameter, table, value1, value2, value3, value4))

    def selectWhereAndNot(self, parameter, table, value1, value2, value3, value4):
        sqlSelectWhereAnd = "SELECT {} FROM {} WHERE {} = {} AND {} <> {}"
        self.cursor.execute(sqlSelectWhereAnd.format(parameter, table, value1, value2, value3, value4))
