try:
    from database.Database import Database
except:
    from storeSite.database.Database import Database

import datetime

class product():

    def __init__(self, prodID, name, description, price, salePrice, catID, picture = None,
                 dateAdded=datetime.date.today(), numbOfGrades=0, grade=0):
        self.prodID = prodID
        self.name = name
        self.description = description
        self.price = price
        self.salePrice = salePrice
        self.grade = grade
        self.numbOfGrades = numbOfGrades
        self.dateAdded = dateAdded
        self.catID = catID
        self.picture = picture

    def format(self):
        return (str(self.prodID)+","+"\""+self.name+"\""+","+"\""+self.description+"\""+","+str(self.price)+","+str(self.salePrice)+","
                + str(self.grade) + ","+str(self.numbOfGrades)+","+"\""+str(self.dateAdded)+"\""
                + ","+str(self.catID))

    def insert(self):
        mydb = Database()
        mydb.insert("storeDB.Product", self.format())
        mydb.commit()
        mydb.end()

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
            thisProduct = product(prodID, name, description, price, salePrice, grade, numbOfGrades,
                                   dateAdded, catID)
            thisProduct.getPicture()
            catalog.append(thisProduct)
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

    def getPicture(self):
        mydb = Database()
        mydb.selectWhere("storeDB.Images.imageSource", "storeDB.Images", "storeDB.Images.prodID", self.prodID)
        try:
            self.picture = mydb.cursor.fetchone()[0]
        except:
            self.picture = "83712837218.jpg"
