import random
from datetime import date
try:
    from storeSite.common.formCheck import formCheck
except:
    from common.formCheck import formCheck
try:
    from database.Database import Database
except:
    from storeSite.database.Database import Database
import hashlib


class user(object):
    def __init__(self, name, email, password, zip, address, city, country, phone, ssn, userID, userLevel = None,
                 regDate = None, newUser = True, balance = None):
        self.name = name
        self.email = email
        self.password = (hashlib.sha1(password.encode()).hexdigest()) if newUser else password
        self.zip = zip
        self.address = address
        self.city = city
        self.country = country
        self.phone = phone
        self.userLvl = "1" if userLevel is None else userLevel
        self.ssn = ssn
        self.userID = str(random.randint(1, 2147483646)) if userID is None else userID
        self.registrationDate = date.today() if regDate is None else regDate
        self.balance = 0.0 if balance is None else balance

    """
    Function name: controllUser
    Input variables: self
    Info: returns if the formCheck of the created user is correct. Not used at the moment.
    """
    def controllUser(self):
        return formCheck(self.name, self.email, self.zip, self.address, self.city, self.country, self.phone, self.ssn)

    """
    Function name: registerUser
    Input variables: self, database
    Info: Inserts the user in the database
    """
    def registerUser(self, database):
        try:
            database.insert("User", self.format())
            database.commit()
            return True
        except:
            return False

    """
    Function name: format
    Input variables: self
    Info: Returns an appropriate string to insert into the database for a user
    """
    def format(self):
        return (self.userID+","+"\""+self.email+"\""+","+"\""+self.password+"\""+","+"\""+self.name+"\""+","+self.zip+","
                + "\"" + self.address + "\"" + ","+"\""+self.city+"\""+","+"\""+self.country+"\""+","+"\""+self.phone+"\""+","+self.userLvl+","
                + "\"" + str(self.registrationDate) + "\"" + ","+"\""+self.ssn+"\""+","+self.balance)

    @staticmethod
    def getUserID(email, mydb):
        mydb.selectWhere("userID", "storeDB.User", "email", "\"" + str(email) + "\"")
        return mydb.cursor.fetchone()[0]

    @staticmethod
    def createUser(request):
        mydb = Database()
        newUser = user(name=request.form['name'], email=request.form['email'], password=request.form['password'],
                       ssn=request.form['ssn'], zip=request.form['ZIP'], address=request.form['address'],
                       city=request.form['city'], country=request.form['country'], phone=request.form['phone'],
                       userID=None)
        newUser.registerUser(mydb)
        mydb.end()

    @staticmethod
    def checkUserLogin(request):
        mydb = Database()
        userEmail = request.form['email']
        mydb.selectWhere("password", "storeDB.User", "email", "\"" + userEmail + "\"")
        try:
            dbpassword = mydb.cursor.fetchone()[0]
        except:
            return False
        hashedUserPassword = (hashlib.sha1(request.form['password'].encode()).hexdigest())
        mydb.end()
        return hashedUserPassword == dbpassword

    @staticmethod
    def createUserCart(userEmail):
        mydb = Database()
        userID = user.getUserID(userEmail, mydb)
        mydb.insert("storeDB.shoppingcart", str(random.randint(1, 2147483647)) + "," + str(userID))
        mydb.commit()
        mydb.end()

    @staticmethod
    def getAccountInfo(userEmail):
        mydb = Database()
        mydb.selectWhere("*", "storeDB.User as user", "email", '"'+ userEmail +'"')
        userInfo = user.getUserList(mydb.cursor)[0]
        mydb.end()
        return userInfo

    @staticmethod
    def getUserList(cursor):
        userList = []
        for userID, email, password, name, zip, adress, city, country, phone, userLevel, registrationDate, \
            ssn, accountBalance in cursor :
            userList.append(user(name=name, email=email, password=password, zip=zip, address=adress, city=city,
                                 regDate=registrationDate, country=country, phone=phone, ssn=ssn, userID=userID,
                                 newUser=False, balance=accountBalance))
        return userList

    @staticmethod
    def change(column, session, setValue):
        mydb = Database()
        success = False
        try:
            mydb.update("storeDB.User", column, "'"+setValue+"'", "email", "'"+session['email']+"'")
            if column == "email":
                session['email'] = setValue
            success = True
        except:
            pass
        mydb.commit()
        mydb.end()
        return success

    @staticmethod
    def addMoney(session, request):
        mydb = Database()
        success = 0
        if      (request.form['Month'] is None or request.form['Month']== "") or \
                (request.form['OCR'] is None or request.form['OCR']== "") or \
                (request.form['cardnumber'] is None or request.form['cardnumber']== ""):
            mydb.commit()
            mydb.end()
            return 1
        try:
            mydb.update("storeDB.User", "accountBalance", "accountBalance+"+str(request.form['Amount']), "email", "'"+session['email']+
                        "'")
            success = 2
        except:
            pass
        mydb.commit()
        mydb.end()
        return success

    @staticmethod
    def isAdmin(session):
        if 'isAdmin' in session:
            return True
        else:
            mydb = Database()
            mydb.selectWhere("storeDB.User.userLevel", "storeDB.User", "email", '"'+session['email']+'"')
            if mydb.cursor.fetchone()[0] > 4:
                return True
            return False

    @staticmethod
    def GetAllUsers():
        mydb = Database()
        mydb.select("*", "storeDB.User")
        userList = user.getUserList(mydb.cursor)
        mydb.end()
        return userList