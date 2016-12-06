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

    def formatSubCategories(self):
        self.subCategories = self.subCategories.split(",")
        prelimList = []
        for catInfo in self.subCategories:
            catInfo = catInfo.split(":")
            prelimList.append(catInfo)
        self.subCategories = prelimList

    @staticmethod
    def getSpecificCatalog(data):
        mydb = Database()
        mydb.selectWhere("*", "storeDB.Product", "catID", int(data))
        catalog = product.createCatalog(mydb.cursor)
        mydb.end()
        return catalog

    @staticmethod
    def getCategories():
        mydb = Database()
        mydb.selectGroup("storeDB.categories.name", "storeDB.subCategories.name," + "\"" + ":" + "\"" +
                         ",storeDB.subCategories.subCatID", "storeDB.categories, storeDB.subCategories",
                         "storeDB.categories.catID", "storeDB.subCategories.catID")
        catList = []
        for name, subCatList in mydb.cursor:
            newCat = Category(name, subCatList)
            newCat.formatSubCategories()
            catList.append(newCat)
        mydb.end()
        return catList

    @staticmethod
    def searchForSubCategories(value):
        mydb = Database()
        subSearch = []
        mydb.search("storeDB.subCategories.name, storeDB.subCategories.subCatID", "storeDB.subCategories", "name",
                    value)
        for (name, subCatID) in mydb.cursor:
            subSearch.append(Category(catID=subCatID, name=name))
        mydb.end()
        return subSearch