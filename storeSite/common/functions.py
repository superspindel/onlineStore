try:
    from storeSite.common.user import user
except:
    from common.user import user
try:
    from database.Database import Database
except:
    from storeSite.database.Database import Database
import hashlib
try:
    from common.product import product
except:
    from storeSite.common.product import product
try:
    from common.Category import Category
except:
    from storeSite.common.Category import Category
try:
    from common.prodDate import prodDate
except:
    from storeSite.common.prodDate import prodDate


"""
Function name: createUser
Input variables: request that comes from the register route
Info: Takes a specific request and takes all the data needed to create a user and returns an object of the class user
"""
def createUser(request):
    mydb = Database()
    mydb.initialize()
    newUser = user(name=request.form['name'], email=request.form['email'], password=request.form['password'], ssn=request.form['ssn'],
                zip=request.form['ZIP'], address=request.form['address'], city=request.form['city'], country=request.form['country'],
                phone=request.form['phone'], userID=None)
    newUser.registerUser(mydb)
    mydb.end()

"""
Function name: checkUserLogin
Input variables: request that comes from the login route
Info: Creates an object with a connection to the database, gets the login email from the request, initialized the database,
Selects from the database the password of the user who is trying to log in, from the cursor that contains the returned data we try to
get the password, then rehashes the password from the request, closes the database connection and then returns a boolean depending
on if the password is correct.
"""
def checkUserLogin(request):
    mydb = Database()
    # get user email
    userEmail = request.form['email']
    # lookup db
    mydb.initialize()
    mydb.selectWhere("password", "User", "email", "\"" + userEmail + "\"")
    try:
        dbpassword = mydb.cursor.fetchone()[0]
    except:
        return False
    hashedUserPassword = (hashlib.sha1(request.form['password'].encode()).hexdigest())
    mydb.end()
    return hashedUserPassword == dbpassword


def getfullCatalog():
    mydb = Database()
    mydb.initialize()
    mydb.select("*", "storeDB.Product")
    catalog = []
    for(prodID, name, description, price, salePrice, grade, numbOfGrades,
                 dateAdded, catID) in mydb.cursor:
        newProd = product(prodID, name, description, price, salePrice, grade, numbOfGrades,
                 dateAdded, catID)
        catalog.append(newProd)
    mydb.end()
    return catalog

def createCatalog(cursor):
    catalog = []
    for(prodID, name, description, price, salePrice, grade, numbOfGrades,
                 dateAdded, catID) in cursor:
        catalog.append(product(prodID, name, description, price, salePrice, grade, numbOfGrades,
                 dateAdded, catID))
    return catalog

def getSpecificCatalog(data):
    mydb = Database()
    mydb.initialize()
    mydb.selectWhere("*", "storeDB.Product", "catID", int(data))
    catalog = createCatalog(mydb.cursor)
    mydb.end()
    return catalog


def getCategories():
    mydb = Database()
    mydb.initialize()
    mydb.selectGroup("storeDB.categories.name", "storeDB.subCategories.name,"+"\""+":"+"\""+
                     ",storeDB.subCategories.subCatID", "storeDB.categories, storeDB.subCategories",
                     "storeDB.categories.catID", "storeDB.subCategories.catID")
    catList = []
    for name, subCatList in mydb.cursor:
        newCat = Category(name, subCatList)
        newCat.formatSubCategories()
        catList.append(newCat)
    mydb.end()
    return catList


def getTimesAvaliable(prodID):
    mydb = Database()
    mydb.initialize()
    mydb.selectWhere("storeDB.ProductDate.dateStart, storeDB.ProductDate.dateEnd, storeDB.ProductDate.prodDateID",
                     "storeDB.ProductDate", "storeDB.ProductDate.prodID", prodID)
    prodList = []
    for dateStart, dateEnd, prodDateID in mydb.cursor:
        newProdDate = prodDate(dateStart, dateEnd, prodDateID)
        prodList.append(newProdDate)
    mydb.end()
    return prodList


def SearchFor(value):
    mydb = Database()
    mydb.initialize()
    searchDict = {}
    searchDict['products'] = searchForProducts(value, mydb)
    searchDict['subCategories'] = searchForSubCategories(value, mydb)
    mydb.end()
    return searchDict


def searchForProducts(value, mydb):
    mydb.search("*", "storeDB.Product", "name", value)
    prodSearch = createCatalog(mydb.cursor)
    return prodSearch


def searchForSubCategories(value, mydb):
    subSearch = []
    mydb.search("storeDB.subCategories.name, storeDB.subCategories.subCatID", "storeDB.subCategories", "name", value)
    for (name, subCatID) in mydb.cursor:
        subSearch.append(Category(catID=subCatID, name=name))
    return subSearch


def getProduct(prodID):
    mydb = Database()
    mydb.initialize()
    mydb.selectWhere("*", "storeDB.Product", "prodID", int(prodID))
    catalog = createCatalog(mydb.cursor)
    return catalog[0]