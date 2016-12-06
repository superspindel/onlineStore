try:
    from database.Database import Database
except:
    from storeSite.database.Database import Database

class product():

    def __init__(self, prodID, name, description, price, salePrice, grade, numbOfGrades,
                 dateAdded, catID):
        self.prodID = prodID
        self.name = name
        self.description = description
        self.price = price
        self.salePrice = salePrice
        self.grade = grade
        self.numbOfGrades = numbOfGrades
        self.dateAdded = dateAdded
        self.catID = catID

    def format(self):
        return (str(self.prodID)+","+"\""+self.name+"\""+","+"\""+self.description+"\""+","+str(self.price)+","+str(self.salePrice)+","
                + str(self.grade) + ","+str(self.numbOfGrades)+","+"\""+str(self.dateAdded)+"\""
                + ","+str(self.catID))

    @staticmethod
    def getfullCatalog():
        mydb = Database()
        mydb.select("*", "storeDB.Product")
        catalog = product.createCatalog(mydb.cursor)
        mydb.end()
        return catalog

    @staticmethod
    def createCatalog(cursor):
        catalog = []
        for (prodID, name, description, price, salePrice, grade, numbOfGrades,
             dateAdded, catID) in cursor:
            catalog.append(product(prodID, name, description, price, salePrice, grade, numbOfGrades,
                                   dateAdded, catID))
        return catalog

    @staticmethod
    def searchForProducts(value):
        mydb = Database()
        mydb.search("*", "storeDB.Product", "name", value)
        prodSearch = product.createCatalog(mydb.cursor)
        return prodSearch

    @staticmethod
    def getProduct(prodID):
        mydb = Database()
        mydb.selectWhere("*", "storeDB.Product", "prodID", int(prodID))
        catalog = product.createCatalog(mydb.cursor)
        mydb.end()
        return catalog[0]