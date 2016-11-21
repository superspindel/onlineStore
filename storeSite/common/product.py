class product():

    def __init__(self, prodID, name, description, price, salePrice, grade, numbOfGrades, quantity,
                 dateAdded, dateOfProdStart, dateOfProdEnd, catID):
        self.prodID = prodID
        self.name = name
        self.description = description
        self.price = price
        self.salePrice = salePrice
        self.grade = grade
        self.numbOfGrades = numbOfGrades
        self.quantity = quantity
        self.dateAdded = dateAdded
        self.dateOfProdStart = dateOfProdStart
        self.dateOfProdEnd = dateOfProdEnd
        self.catID = catID

    def format(self):
        return (str(self.prodID)+","+"\""+self.name+"\""+","+"\""+self.description+"\""+","+str(self.price)+","+str(self.salePrice)+","
                + str(self.grade) + ","+str(self.numbOfGrades)+","+str(self.quantity)+","+"\""+str(self.dateAdded)+"\""
                + ","+"\""+str(self.dateOfProdStart)+"\""+","+"\"" + str(self.dateOfProdEnd) + "\""+","+str(self.catID))
