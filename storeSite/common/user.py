from random import randint
from datetime import date
try:
    from storeSite.common.formCheck import formCheck
except:
    from common.formCheck import formCheck
import hashlib


class user(object):
    def __init__(self, name, email, password, zip, address, city, country, phone, ssn, userID):
        self.name = name
        self.email = email
        self.password = (hashlib.sha1(password.encode()).hexdigest())
        self.zip = zip
        self.address = address
        self.city = city
        self.country = country
        self.phone = phone
        self.userLvl = "1"
        self.ssn = ssn
        self.userID = str(randint(1, 2147483646)) if userID is None else userID
        self.registrationDate = date.today()
        self.balance = "0.0"

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
        database.insert("User", self.format())

    """
    Function name: format
    Input variables: self
    Info: Returns an appropriate string to insert into the database for a user
    """
    def format(self):
        return (self.userID+","+"\""+self.email+"\""+","+"\""+self.password+"\""+","+"\""+self.name+"\""+","+self.zip+","
                + "\"" + self.address + "\"" + ","+"\""+self.city+"\""+","+"\""+self.country+"\""+","+"\""+self.phone+"\""+","+self.userLvl+","
                + "\"" + str(self.registrationDate) + "\"" + ","+"\""+self.ssn+"\""+","+self.balance)