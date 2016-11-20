from flask import Flask, render_template, request, session
from database.Database import Database
from common.functions import createUser, checkUserLogin, getCatalog
from common.product import product


storeApp = Flask(__name__)
storeApp.secret_key = "hfudsyf7h4373hfnds9y32nfw93hf"

"""
Function name: storeHome
Input variables:
Info: returns the home.html template
"""
@storeApp.route('/')
def storeHome():
    if 'email' in session:
        userEmail = session['email']
        return render_template('home.html', userEmail=userEmail)
    else:
        return render_template('home.html')


"""
Function name: categories
Input variables: cat_id
Info: returns the category.html template for the selected cat_id, should be fetched from the database and contain the data of the
objects in that category.
"""
@storeApp.route('/Category/<string:cat_id>')
def categories(cat_id):
    return render_template('Category.html', category_id=cat_id)

	
@storeApp.route('/generera')
def generera():
    mydb = Database()
    mydb.initialize()
    mydb.selectWhere("prodID, name, description, price, salePrice, grade, numbOfGrades, quantity, dateAdded, dateOfProdStart, dateOfProdEnd, catID", "Product", "catID", "1")
    productList = []
    for(prodID, name, description, price, salePrice, grade, numbOfGrades, quantity, dateAdded, dateOfProdStart, dateOfProdEnd, catID) in mydb.cursor:
        prod = product(prodID, name, description, price, salePrice, grade, numbOfGrades, quantity, dateAdded, dateOfProdStart, dateOfProdEnd, catID)
        productList.append(prod)
	mydb.end()
    return render_template('generera.html', database = productList)

"""
Function name: search
Input variables:
Info: Should get from database the data that matches the searchword in request.form['searchfield']
"""
@storeApp.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        return render_template('search.html', searchtext=request.form['searchfield'])


"""
Function name: login
Input variables:
Info: If get then not trying to login, so it should return home.html template
if post it uses the function chechUserLogin with the current request to see if the user can login using those credentials.
"""
@storeApp.route('/auth/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        if checkUserLogin(request):
            session['email'] = request.form['email']
            return render_template('home.html', userEmail=session['email'])
        else:
            session['email'] = None
            return render_template('home.html')



"""
Function name: register
Input variables:
Info: If GET request, return the form to sign up,
If post the user is trying to sign up, we create a user using the createUser function aswell as the current request
then initializes a database connection and uses the registerUser class function to insert the data into the database
then closes the connection
"""
@storeApp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html', register=False)
    else:
        newUser = createUser(request)
        mydb = Database()
        mydb.initialize()
        newUser.registerUser(mydb)
        mydb.end()
        return render_template('home.html')


"""
Function name: test
Input variables:
Info: Test route for testing
"""
@storeApp.route('/test')
def test():
    mydb = Database()
    catalog = getCatalog(mydb)
    return render_template('home.html', Catalog=catalog)


"""
Function name: beforeFirstRequest
Input variables:
Info: If something needs to be done before the first request, those functions get called here
"""
@storeApp.before_first_request
def beforeFirstRequest():
    pass

if __name__ == '__main__':
    storeApp.run(port=4995)#, host='0.0.0.0')
