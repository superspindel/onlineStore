try:
    from database.Database import Database
except:
    from storeSite.database.Database import Database
try:
    from common.product import product
except:
    from storeSite.common.product import product


class Category(object):
    def __init__(self, name, subCategories=None, catID=None, subCatID=None):
        self.name = name
        self.subCategories = subCategories
        self.catID = catID
        self.subCatID = subCatID
        if subCategories is not None:
            self.splitSubCategories()

    def splitSubCategories(self):
        self.subCategories = self.subCategories.split(",")
        self.subCategories = [catInfo.split(":") for catInfo in self.subCategories]

    def formatMainCategory(self):
        return "{}, '{}'".format(self.catID, self.name)

    def formatSubCategory(self):
        return "'{}', {}, {}".format(self.name, self.catID, self.subCatID)

    def insertMainCategory(self):
        mydb = Database()
        mydb.insert("storeDB.categories", self.formatMainCategory())
        mydb.commit()
        mydb.end()

    def insertSubCategory(self):
        mydb = Database()
        mydb.insert("storeDB.subCategories", self.formatSubCategory())
        mydb.commit()
        mydb.end()

    @staticmethod
    def getPrimaryCategories():
        mydb = Database()
        mydb.select("*", "storeDB.categories")
        list = mydb.cursor.fetchall()
        mydb.end()
        return [Category(catID=catId, name=name) for catId, name in list]

    @staticmethod
    def getSubCategories():
        mydb = Database()
        mydb.select("*", "storeDB.subCategories")
        list = mydb.cursor.fetchall()
        mydb.end()
        return [Category(name=name, catID=catID, subCatID=subCatID) for name, catID, subCatID in list]

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
        categoriesWithSub = [Category(name=name, subCategories=subCatList) for name, subCatList in mydb.cursor]
        mydb.selectFromNotIn("*", "storeDB.categories", "storeDB.categories.catID", "storeDB.subCategories.catID",
                             "storeDB.subCategories")
        categoriesNotSub = [Category(catID=catid, name=name) for catid, name in mydb.cursor]
        mydb.end()
        return(categoriesWithSub+categoriesNotSub)

    @staticmethod
    def searchForSubCategories(value):
        mydb = Database()
        mydb.search("storeDB.subCategories.name, storeDB.subCategories.subCatID", "storeDB.subCategories", "name",
                    value)
        subSearch = [Category(catID=subCatID, name=name) for name, subCatID in mydb.cursor]
        mydb.end()
        return subSearch