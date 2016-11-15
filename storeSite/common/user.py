from random import randint
from datetime import date
from storeSite.common.formCheck import formCheck
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

    def controllUser(self):
        return formCheck(self.name, self.email, self.zip, self.address, self.city, self.country, self.phone, self.ssn)

    def registerUser(self, database):
        database.insert("User", self.format())

    def format(self):
        return (self.userID+","+"\""+self.email+"\""+","+"\""+self.password+"\""+","+"\""+self.name+"\""+","+self.zip+","
                + "\"" + self.address + "\"" + ","+"\""+self.city+"\""+","+"\""+self.country+"\""+","+"\""+self.phone+"\""+","+self.userLvl+","
                + "\"" + str(self.registrationDate) + "\"" + ","+"\""+self.ssn+"\""+","+self.balance)