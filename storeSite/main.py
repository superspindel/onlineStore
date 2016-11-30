from flask import Flask, render_template, request, session, redirect
try:
    from common.functions import createUser, checkUserLogin, getfullCatalog, getSpecificCatalog, getCategories, \
        getTimesAvaliable, SearchFor, getProduct, createUserCart, addProduct, getCarts, getCartProducts
except:
    from storeSite.common.functions import createUser, checkUserLogin, getfullCatalog, getSpecificCatalog, \
        getCategories, getTimesAvaliable, SearchFor, getProduct, createUserCart, addProduct, getCarts, getCartProducts

storeApp = Flask(__name__)
storeApp.secret_key = "hfudsyf7h4373hfnds9y32nfw93hf"

"""
Function name: storeHome
Input variables:
Info: returns the home.html template
"""
@storeApp.route('/')
def storeHome():
    catList = getCategories()
    if 'email' in session:
        userEmail = session['email']
        return render_template('home.html', userEmail=userEmail, categories=catList)
    else:
        return render_template('home.html', categories=catList)


"""
Function name: categories
Input variables: cat_id
Info: returns the category.html template for the selected cat_id, should be fetched from the database and contain the data of the
objects in that category.
"""
@storeApp.route('/Category/<string:cat_id>')
def categories(cat_id):
    catList = getCategories()
    catalog = getSpecificCatalog(int(cat_id))
    if 'email' in session:
        return render_template('generera.html', Database=catalog, categories=catList, userEmail=session['email'])
    else:
        return render_template('generera.html', Database=catalog, categories=catList)


"""
Function name: search
Input variables:
Info: Should get from database the data that matches the searchword in request.form['searchfield']
"""
@storeApp.route('/search', methods=['POST', 'GET'])
def search():
    catList = getCategories()
    if request.method == 'GET':
        return storeHome()
    else:
        searchResult = SearchFor(request.form['searchfield'])
        if 'email' in session:
            return render_template('search.html', searchResult=searchResult, categories=catList, userEmail=session['email'])
        else:
            return render_template('search.html', searchResult=searchResult, categories=catList)


"""
Function name: login
Input variables:
Info: If get then not trying to login, so it should return home.html template
if post it uses the function chechUserLogin with the current request to see if the user can login using those credentials.
"""
@storeApp.route('/auth/login', methods=['POST', 'GET'])
def login():
    catList = getCategories()
    if request.method == 'GET':
        return render_template('home.html')
    else:
        if checkUserLogin(request):
            session['email'] = request.form['email']
            return render_template('home.html', userEmail=session['email'], categories=catList)
        else:
            return render_template('home.html', categories=catList)



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
    catList = getCategories()
    if request.method == 'GET':
        return render_template('register.html', register=False, categories=catList)
    else:
        createUser(request)
        return render_template('home.html', categories=catList)


"""
Function name: test
Input variables:
Info: Test route for testing
"""
@storeApp.route('/test')
def test():
    catList = getCategories()
    carts = getCarts(session['email'])
    cartProducts = getCartProducts(session['cart'])
    return render_template('home.html', categories=catList, shoppingCarts=carts, userEmail=session['email'],
                           cartProds=cartProducts)


@storeApp.route('/logout')
def logout():
    catList = getCategories()
    session.clear()
    return render_template('home.html', categories=catList)


@storeApp.route('/more/<string:prod_id>')
def showProductDates(prod_id):
    catList = getCategories()
    prodDates = getTimesAvaliable(int(prod_id))
    getProductInfo = getProduct(int(prod_id))
    if 'email' in session:
        return render_template('test.html', categories=catList, productDates=prodDates, prodInfo=getProductInfo,
                               userEmail=session['email'])
    else:
        return render_template('test.html', categories=catList, productDates=prodDates, prodInfo=getProductInfo)


@storeApp.route('/add/<string:prodDate_id>', methods=['POST', 'GET'])
def addToCart(prodDate_id):
    if addProduct(int(prodDate_id), session):
        return storeHome()
    else:
        return storeHome()

@storeApp.route('/createCart')
def createCart():
    if 'email' in session:
        userEmail = session['email']
        createUserCart(userEmail)
        return storeHome()
    else:
        return storeHome()

@storeApp.route('/changeCart/<string:cart_ID>')
def changeCart(cart_ID):
    session['cart'] = cart_ID
    return test()
"""
Function name: beforeFirstRequest
Input variables:
Info: If something needs to be done before the first request, those functions get called here
"""
@storeApp.before_first_request
def beforeFirstRequest():
    session.permanent = False

if __name__ == '__main__':
    storeApp.run(port=4995)#,host='0.0.0.0')


