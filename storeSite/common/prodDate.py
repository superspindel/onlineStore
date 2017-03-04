try:
    from database.Database import Database
except:
    from storeSite.database.Database import Database

class prodDate(object):

    def __init__(self, dateStart, dateEnd, prodDateID, prodID = None, quantity = 0):
        self.dateStart = dateStart
        self.dateEnd = dateEnd
        self.prodDateID = prodDateID
        self.prodID = prodID
        self.quantity = quantity

    def format(self):
        return "{}, '{}', '{}', {}, {}".format(self.prodID, self.dateStart, self.dateEnd, self.prodDateID,
                                               self.quantity)

    def insert(self):
        mydb = Database()
        mydb.insert("storeDB.ProductDate", self.format())
        mydb.commit()
        mydb.end()

    @staticmethod
    def getTimesAvaliable(prodID):
        mydb = Database()
        mydb.selectWhereAndLargerThenZero("storeDB.ProductDate.dateStart, storeDB.ProductDate.dateEnd, " +
                                          "storeDB.ProductDate.prodDateID", "storeDB.ProductDate",
                                          "storeDB.ProductDate.prodID", prodID, "quantity")
        prodList = [prodDate(dateStart=dateStart, dateEnd=dateEnd, prodDateID=prodDateID)
                    for dateStart, dateEnd, prodDateID in mydb.cursor]
        mydb.end()
        return prodList

    @staticmethod
    def getProdDateList(cursor):
        return [prodDate(prodID=prodID, dateStart=dateStart, dateEnd=dateEnd, prodDateID=prodDateID, quantity=quantity)
                for prodID, dateStart, dateEnd, prodDateID, quantity in cursor]
