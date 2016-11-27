class Category(object):
    def __init__(self, name, subCategories=None, catID=None):
        self.name = name
        self.subCategories = None if subCategories is None else subCategories
        self.catID = None if catID is None else catID

    def formatSubCategories(self):
        self.subCategories = self.subCategories.split(",")
        prelimList = []
        for catInfo in self.subCategories:
            catInfo = catInfo.split(":")
            prelimList.append(catInfo)
        self.subCategories = prelimList