try:
    from database.Database import Database
except:
    from storeSite.database.Database import Database

class prodDate(object):

    def __init__(self, dateStart, dateEnd, prodDateID):
        self.dateStart = dateStart
        self.dateEnd = dateEnd
        self.prodDateID = prodDateID

    @staticmethod
    def getTimesAvaliable(prodID):
        mydb = Database()
        mydb.selectWhereAndLargerThenZero("storeDB.ProductDate.dateStart, storeDB.ProductDate.dateEnd, " +
                                          "storeDB.ProductDate.prodDateID", "storeDB.ProductDate",
                                          "storeDB.ProductDate.prodID", prodID, "quantity")
        prodList = []
        for dateStart, dateEnd, prodDateID in mydb.cursor:
            newProdDate = prodDate(dateStart, dateEnd, prodDateID)
            prodList.append(newProdDate)
        mydb.end()
        return prodList
