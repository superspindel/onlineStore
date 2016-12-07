try:
    from database.Database import Database
except:
    from storeSite.database.Database import Database

class Image(object):


    def __init__(self, imageID, prodID, imagePlacement, imageSource):
        self.imageID = imageID
        self.prodID = prodID
        self.imagePlacement = imagePlacement
        self.imageSource = imageSource

    def insert(self):
        mydb = Database()
        mydb.insert("storeDB.Images", self.format())
        mydb.end()

    def format(self):
        return str(self.imageID)+","+str(self.prodID)+","+str(self.imagePlacement)+","+"'"+str(self.imageSource)+"'"

    @staticmethod
    def getAllImages():
        mydb = Database()
        mydb.select("*", "storeDB.Images")
        catalog = Image.imageCatalog(mydb.cursor)
        mydb.end()
        return catalog


    @staticmethod
    def imageCatalog(cursor):
        catalog = []
        for imageID, prodID, imagePlacement, imageSource in cursor:
            catalog.append(Image(imageID=imageID, prodID=prodID, imagePlacement=imagePlacement,
                                 imageSource=imageSource))
        return catalog

