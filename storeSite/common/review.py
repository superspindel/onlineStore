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
    def __init__(self, reviewID, userID, title, description, grade, approved, prodID):
        self.reviewID = str(randint(1, 2147483646)) if reviewID is None else reviewID
        self.userID = userID
        self.title = title
        self.description = description
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
        return "{}, {}, '{}', '{}', {}, {}, {}".format(self.reviewID, self.userID, self.title, self.description,
                                                      self.grade, self.approved, self.prodID)


    @staticmethod
    def getReviewList(cursor):
        return [review(reviewID=reviewID, userID=userID, title=title, description=description, grade=grade,
                       approved=approved, prodID=prodID)
                for reviewID, userID, title, description, grade, approved, prodID in cursor]

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
        mydb.startTransaction()
        mydb.selectWhere("*", "storeDB.reviews", "reviewID", reviewID)
        newReview = review.getReviewList(mydb.cursor)[0]
        mydb.deleteFrom("storeDB.reviews", "reviewID", reviewID)
        mydb.commit()
        review.updateGrade(prodID, mydb, newReview, 2)
        mydb.end()

    @staticmethod
    def updateGrade(prodID, mydb, reviewObject, switch):
        mydb.selectWhere("*", "Product", "prodID", prodID)
        newProd = product.createCatalog(mydb.cursor)[0]
        if switch == 1:
            mydb.update("storeDB.Product", "numbOfGrades", "numbOfGrades+1", "prodID", prodID)
            finalGrade = (float(newProd.numbOfGrades) * float(newProd.grade) + float(reviewObject.grade)) /\
                         (float(newProd.numbOfGrades) + 1)
        elif switch == 2:
            if newProd.numbOfGrades == 0:
                finalGrade = 0.0
            else:
                mydb.update("storeDB.Product", "numbOfGrades", "numbOfGrades-1", "prodID", prodID)
                try:
                    finalGrade = (newProd.numbOfGrades * newProd.grade - reviewObject.grade) / (newProd.numbOfGrades - 1)
                except:
                    finalGrade = 0.0
        mydb.update("storeDB.Product", "grade", finalGrade, "prodID", prodID)
        mydb.commit()

    @staticmethod
    def createReview(request, prodID, session):
        mydb = Database()
        mydb.startTransaction()
        newReview = review(reviewID=None, userID=user.getUserID(session['email'], mydb), title=request.form['titel'],
                           description=request.form['beskrivning'],
                           grade=request.form['grade'], approved=1, prodID=prodID)
        review.updateGrade(prodID, mydb, newReview, 1)
        newReview.addReview(mydb)
        mydb.commit()
        mydb.end()

    @staticmethod
    def getAllReviews():
        mydb = Database()
        mydb.select("*", "storeDB.reviews")
        reviewList = review.getReviewList(mydb.cursor)
        mydb.end()
        return reviewList
