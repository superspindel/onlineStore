try:
    from database.Database import Database
except:
    from storeSite.database.Database import Database
try:
    from common.product import product
except:
    from storeSite.common.product import product


class Category(object):
    def __init__(self, name, subCategories=None, catID=None):
        self.name = name
        self.subCategories = subCategories
        self.catID = catID
        if subCategories is not None:
            self.formatSubCategories()

    def formatSubCategories(self):
        self.subCategories = self.subCategories.split(",")
        self.subCategories = [catInfo.split(":") for catInfo in self.subCategories]

    @staticmethod
    def getSpecificCatalog(data):
        mydb = Database()
        mydb.selectWhere("*", "storeDB.Product", "catID", data)
        catalog = product.createCatalog(mydb.cursor)
        mydb.end()
        return catalog

    @staticmethod
    def getCategories():
        mydb = Database()
        mydb.selectGroup("storeDB.categories.name", "storeDB.subCategories.name," + "\"" + ":" + "\"" +
                         ",storeDB.subCategories.subCatID", "storeDB.categories, storeDB.subCategories",
                         "storeDB.categories.catID", "storeDB.subCategories.catID")
        catList = [Category(name=name, subCategories=subCatList) for name, subCatList in mydb.cursor]
        mydb.end()
        return catList

    @staticmethod
    def searchForSubCategories(value):
        mydb = Database()
        mydb.search("storeDB.subCategories.name, storeDB.subCategories.subCatID", "storeDB.subCategories", "name",
                    value)
        subSearch = [Category(catID=subCatID, name=name) for name, subCatID in mydb.cursor]
        mydb.end()
        return subSearch