class Category(object):
    def __init__(self, name, subCategories):
        self.name = name
        self.subCategories = subCategories

    def formatSubCategories(self):
        self.subCategories = self.subCategories.split(",")
        prelimList = []
        for catInfo in self.subCategories:
            catInfo = catInfo.split(":")
            prelimList.append(catInfo)
        self.subCategories = prelimList