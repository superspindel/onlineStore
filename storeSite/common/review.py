from random import randint
try:
    from storeSite.common.formCheck import formCheck
except:
    from common.formCheck import formCheck
try:
    from database.Database import Database
except:
    from storeSite.database.Database import Database
try:
    from common.user import user
except:
    from storeSite.common.user import user
try:
    from common.product import product
except:
    from storeSite.common.product import product

    from common.user import user
try:
    from common.product import product
except:
    from common.product import product



class review(object):
    def __init__(self, reviewID, userID, title, Description, grade, approved, prodID):
        self.reviewID = str(randint(1, 2147483646)) if reviewID is None else reviewID
        self.userID = userID
        self.title = title
        self.Description = Description
        self.grade = grade
        self.approved = approved
        self.prodID = prodID

    """
    Function name: registerUser
    Input variables: self, database
    Info: Inserts the user in the database
    """

    def addReview(self, database):
        database.insert("reviews", self.format())
        database.commit()

    """
    Function name: format
    Input variables: self
    Info: Returns an appropriate string to insert into the database for a user
    """

    def format(self):
        return (str(self.reviewID) + "," + "\"" + str(
            self.userID) + "\"" + "," + "\"" + self.title + "\"" + "," + "\"" + self.Description + "\"" + "," + str(
            self.grade) + ","
                + "\"" + str(self.approved) + "\"" + "," + "" + str(self.prodID))


    @staticmethod
    def getReviewList(cursor):
        reviewList = []
        for reviewID, userID, title, Description, grade, approved, prodID in cursor:
            reviewList.append(review(reviewID, userID, title, Description, grade, approved, prodID))
        return reviewList

    @staticmethod
    def fetchReviews(prodID, session):
        mydb = Database()
        currentUserID = user.getUserID(session['email'], mydb)
        mydb.selectWhereAndNot("*", "storeDB.reviews", "prodID", prodID, "userID", currentUserID)
        reviewList = review.getReviewList(mydb.cursor)
        mydb.end()
        return reviewList

    @staticmethod
    def fetchMyReviews(prodID, session):
        mydb = Database()
        currentUserID = user.getUserID(session['email'], mydb)
        mydb.selectWhereAnd("*", "storeDB.reviews", "userID", currentUserID, "prodID", prodID)
        reviewList = review.getReviewList(mydb.cursor)
        mydb.end()
        return reviewList

    @staticmethod
    def removeReview(reviewID, session, prodID):
        mydb = Database()
        mydb.selectWhere("*", "storeDB.reviews", "reviewID", reviewID)
        for reviewID, userID, title, Description, grade, approved, prodID in mydb.cursor:
            newReview = review(reviewID, userID, title, Description, grade, approved, prodID)
        mydb.deleteFrom("storeDB.reviews", "reviewID", reviewID)
        mydb.commit()
        review.updateGrade(prodID, mydb, newReview, 2)
        mydb.end()

    @staticmethod
    def updateGrade(prodID, mydb, reviewObject, switch):
        mydb.selectWhere("*", "Product", "prodID", prodID)
        for (productID, name, description, price, salePrice, grade, numbOfGrades, dateAdded, catID) in mydb.cursor:
            newProd = product(productID, name, description, price, salePrice, grade, numbOfGrades, dateAdded, catID)
        if switch == 1:
            mydb.update("storeDB.Product", "numbOfGrades", "numbOfGrades+1", "prodID", prodID)
            finalGrade = (float(newProd.numbOfGrades) * float(newProd.grade) + float(reviewObject.grade)) / (
            float(newProd.numbOfGrades) + 1)
        elif switch == 2:
            if newProd.numbOfGrades == 0:
                finalGrade = 0.0
            else:
                mydb.update("storeDB.Product", "numbOfGrades", "numbOfGrades-1", "prodID", prodID)
                finalGrade = (newProd.numbOfGrades * newProd.grade - reviewObject.grade) / (newProd.numbOfGrades - 1)
        mydb.startTransaction()
        mydb.update("storeDB.Product", "grade", finalGrade, "prodID", prodID)
        mydb.commit()

    @staticmethod
    def createReview(request, data, session):
        mydb = Database()
        mydb.startTransaction()
        newReview = review(reviewID=None, userID=user.getUserID(session['email'], mydb), title=request.form['titel'],
                           Description=request.form['beskrivning'],
                           grade=request.form['grade'], approved=1, prodID=data)
        newReview.addReview(mydb)
        mydb.commit()
        review.updateGrade(data, mydb, newReview, 1)
        mydb.end()

    @staticmethod
    def getAllReviews():
        mydb = Database()
        mydb.select("*", "storeDB.reviews")
        reviewList = review.getReviewList(mydb.cursor)
        mydb.end()
        return reviewList