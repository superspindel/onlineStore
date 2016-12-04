from flask import Flask, render_template, request, session, redirect, url_for
from urllib.parse import urlparse, urljoin
from flask import request, url_for
try:
    from storeSite.common.functions import SearchFor, getDictionary
except:
    from common.functions import SearchFor, getDictionary
try:
    from storeSite.common.user import user
except:
    from common.user import user
try:
    from storeSite.common.shoppingCart import shoppingCart
except:
    from common.shoppingCart import shoppingCart
try:
    from common.product import product
except:
    from storeSite.common.product import product
try:
    from storeSite.common.review import review
except:
    from common.review import review
storeApp = Flask(__name__)
storeApp.secret_key = "hfudsyf7h4373hfnds9y32nfw93hf"

"""
Function name: storeHome
Input variables:
Info: returns the home.html template
"""
@storeApp.route('/')
def storeHome():
    data = getDictionary(session=session)
    return render_template('home.html', dictionary=data)


"""
Function name: categories
Input variables: cat_id
Info: returns the category.html template for the selected cat_id, should be fetched from the database and contain the data of the
objects in that category.
"""
@storeApp.route('/Category/<string:cat_id>')
def categories(cat_id):
    data = getDictionary(session=session, cat_id=cat_id)
    return render_template('generera.html', dictionary=data)


@storeApp.route('/Review/<int:prodID>', methods=['POST'])
def Review(prodID):
	if 'email' in session:
		review.createReview(request, data = prodID, session=session)
		return storeHome()
	else:
		return register()
	
"""
Function name: search
Input variables:
Info: Should get from database the data that matches the searchword in request.form['searchfield']
"""
@storeApp.route('/search', methods=['POST', 'GET'])
def search():
    data = getDictionary(session=session, request=request)
    if request.method == 'GET':
        return storeHome()
    else:
        return render_template('search.html', dictionary=data)



"""
Function name: login
Input variables:
Info: If get then not trying to login, so it should return home.html template
if post it uses the function chechUserLogin with the current request to see if the user can login using those credentials.
"""
@storeApp.route('/auth/login', methods=['POST', 'GET'])
def login():
    if user.checkUserLogin(request):
        session['email'] = request.form['email']
        try:
            session['cart'] = shoppingCart.getCarts(session['email'])[0]
        except:
            pass
    return redirect(request.referrer)



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
    data = getDictionary(session=session)
    if request.method == 'POST':
        user.createUser(request)
    return render_template('register.html', dictionary=data)



"""
Function name: test
Input variables:
Info: Test route for testing
"""
@storeApp.route('/test')
def test():
    data = getDictionary(session=session)
    return render_template('home.html', dictionary=data)


@storeApp.route('/logout')
def logout():
    session.clear()
    return redirect(request.referrer)


@storeApp.route('/more/<string:prod_id>')
def showProductDates(prod_id):
    data = getDictionary(session=session, prod_id=int(prod_id))
    return render_template('test.html', dictionary=data)


@storeApp.route('/add/<string:prodDate_id>', methods=['POST', 'GET'])
def addToCart(prodDate_id):
    if shoppingCart.addProduct(int(prodDate_id), session):
        return redirect(request.referrer)
    else:
        session['product'] = prodDate_id
        return createCart()


@storeApp.route('/remove/<string:prodDate_id>', methods=['POST', 'GET'])
def removeFromCart(prodDate_id):
    shoppingCart.removeProduct(int(prodDate_id), session)
    return redirect(request.referrer)


@storeApp.route('/createCart')
def createCart():
    if 'email' in session:
        user.createUserCart(session['email'])
        session['cart'] = shoppingCart.getCarts(session['email'])[0]
        if 'product' in session:
            return addToCart(session['product'])
        else:
            return redirect(request.referrer)
    else:
        return register()


@storeApp.route('/changeCart/<string:cart_ID>')
def changeCart(cart_ID):
    session['cart'] = cart_ID
    return redirect(request.referrer)


@storeApp.route('/account')
def accountPage():
    data = getDictionary(session=session, accountEmail = session['email'])
    return render_template('konto.html', dictionary = data)

"""
Function name: beforeFirstRequest
Input variables:
Info: If something needs to be done before the first request, those functions get called here
"""
@storeApp.before_first_request
def beforeFirstRequest():
    session.permanent = False

if __name__ == '__main__':
    storeApp.run(port=4995, host='0.0.0.0')

