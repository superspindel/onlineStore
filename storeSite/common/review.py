from random import randint
from datetime import date
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
    from common.user import user
try:
    from common.product import product
except:
    from common.product import product
import hashlib


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
        return (str(self.reviewID)+","+"\""+str(self.userID)+"\""+","+"\""+self.title+"\""+","+"\""+self.Description+"\""+","+str(self.grade)+","
                + "\"" + str(self.approved) + "\"" + ","+""+str(self.prodID))
				
    def fetchReviews(prodID, session):
        mydb = Database()
        mydb.initialize()
        reviewList = []
        currentUserID = user.getUserID(session['email'], mydb)
        mydb.selectWhereAndNot("*", "storeDB.reviews", "prodID", prodID, "userID", currentUserID)
        for reviewID, userID, title, Description, grade, approved, prodID in mydb.cursor:
            newReview = review(reviewID, userID, title, Description, grade, approved, prodID)
            reviewList.append(newReview)
        mydb.end()
        return reviewList
		
    def fetchMyReviews(prodID, session):
        mydb = Database()
        mydb.initialize()
        reviewList = []
        currentUserID = user.getUserID(session['email'], mydb)
        mydb.selectWhereAnd("*", "storeDB.reviews", "userID", currentUserID, "prodID", prodID)
        for reviewID, userID, title, Description, grade, approved, prodID in mydb.cursor:
            newReview = review(reviewID, userID, title, Description, grade, approved, prodID)
            reviewList.append(newReview)
        mydb.end()
        return reviewList
		
    def removeReview(reviewID, session, prodID):
        mydb = Database()
        mydb.initialize()
        mydb.deleteFromAnd("storeDB.reviews", "reviewID", reviewID, "userID", user.getUserID(session['email'], mydb))
        mydb.update("storeDB.Product", "numbOfGrades", "numbOfGrades-1", "prodID", prodID)
        mydb.commit()
        review.updateGrade(prodID, mydb)
        mydb.end()
		
    def updateGrade(prodID, mydb):
        mydb.selectWhere("*", "Product", "prodID", prodID)
        for (prodID, name, description, price, salePrice, grade, numbOfGrades, dateAdded, catID) in mydb.cursor:
            newProd = product(prodID, name, description, price, salePrice, grade, numbOfGrades,dateAdded, catID)
        finalGrade = 0
        mydb.selectWhere("*", "storeDB.reviews", "prodID", prodID)
        for reviewID, userID, title, Description, grade, approved, prodID in mydb.cursor:
            newReview = review(reviewID, userID, title, Description, grade, approved, prodID)
            finalGrade = finalGrade + newReview.grade
        if newProd.numbOfGrades == 0:
            finalGrade = 0
        else:
            finalGrade = finalGrade / newProd.numbOfGrades
        mydb.startTransaction()
        mydb.update("storeDB.Product", "grade", finalGrade, "prodID", prodID)
        mydb.commit()
		
    def createReview(request, data, session):
        mydb = Database()
        mydb.initialize()
        mydb.startTransaction()
        newReview = review(reviewID=None, userID=user.getUserID(session['email'], mydb), title=request.form['titel'], Description=request.form['beskrivning'],
        grade=request.form['grade'], approved=1, prodID=data)
        newReview.addReview(mydb)
        mydb.update("storeDB.Product", "numbOfGrades", "numbOfGrades+1", "prodID", data)
        mydb.commit()
        review.updateGrade(data, mydb)
        mydb.end()
