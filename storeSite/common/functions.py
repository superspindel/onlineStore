try:
    from storeSite.common.user import user
    import hashlib
except:
    pass


def createUser(request):
    return user(name=request.form['name'], email=request.form['email'], password=request.form['password'], ssn=request.form['ssn'],
                zip=request.form['ZIP'], address=request.form['address'], city=request.form['city'], country=request.form['country'],
                phone=request.form['phone'], userID=None)

def checkUserLogin(request, mydb):
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
    return hashedUserPassword == dbpassword
