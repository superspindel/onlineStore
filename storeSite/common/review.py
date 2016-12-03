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
				
    def fetchReviews(prodID):
        selectWhere("title, Description, grade", "reviews", "prodID", prodID)
		
    def createReview(request, data, session):
        mydb = Database()
        mydb.initialize()
        newReview = review(reviewID=None, userID=user.getUserID(session['email'], mydb), title=request.form['titel'], Description=request.form['beskrivning'],
        grade=request.form['grade'], approved=1, prodID=data)
        newReview.addReview(mydb)
        mydb.end()
