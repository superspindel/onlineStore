try:
    from storeSite.common.user import user
    import hashlib
    from database.Database import Database
except:
    pass

"""
Function name: createUser
Input variables: request that comes from the register route
Info: Takes a specific request and takes all the data needed to create a user and returns an object of the class user
"""
def createUser(request):
    return user(name=request.form['name'], email=request.form['email'], password=request.form['password'], ssn=request.form['ssn'],
                zip=request.form['ZIP'], address=request.form['address'], city=request.form['city'], country=request.form['country'],
                phone=request.form['phone'], userID=None)

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
    mydb.select("password", "User", "email", "\"" + userEmail + "\"")
    try:
        dbpassword = mydb.cursor.fetchone()[0]
    except:
        return False
    hashedUserPassword = (hashlib.sha1(request.form['password'].encode()).hexdigest())
    mydb.end()
    return hashedUserPassword == dbpassword
