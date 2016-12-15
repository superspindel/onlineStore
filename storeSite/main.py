from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask import request, url_for
try:
    from storeSite.common.functions import SearchFor, getDictionary, getAdminDict, createFunction, getChangeDict
except:
    from common.functions import SearchFor, getDictionary, getAdminDict, createFunction, getChangeDict
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
try:
    from storeSite.common.orders import order
except:
    from common.orders import order
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


@storeApp.route('/Review/<int:prodID>', methods=['POST', 'GET'])
def Review(prodID):
    if request.method == 'POST':
        if 'email' in session:
            review.createReview(request=request, prodID=prodID, session=session)
            return redirect(request.referrer)
        else:
            return register()
    else:
        return showProductDates(prodID)


@storeApp.route('/removeReview/<int:reviewID>/<string:prodID>', methods=['POST', 'GET'])
def removeFromReviews(reviewID, prodID):
    try:
        review.removeReview(reviewID, session, prodID)
    except:
        pass
    return showProductDates(prodID)

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
    if request.method=='GET':
        return storeHome()
    if user.checkUserLogin(request):
        session['email'] = request.form['email']
        try:
            session['cart'] = shoppingCart.getCarts(session['email'])[0]
        except:
            user.createUserCart(session['email'])
            session['cart'] = shoppingCart.getCarts(session['email'])[0]
        if 'product' in session:
            if shoppingCart.addProduct(int(session['product']), session):
                session.pop('product', None)
                return storeHome()
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
        if user.createUser(request):
            flash("Registrering genomförd", category="register")
        else:
            flash("Registrering gick inte att genomföra", category="register")
    return render_template('register.html', dictionary=data)


@storeApp.route('/buy/<string:cartID>', methods=['POST', 'GET'])
def performOrder(cartID):
    result = order.createOrder(request, session, cartID)
    flash(result, category="order")
    return redirect(request.referrer)


@storeApp.route('/showOrders', methods=['POST', 'GET'])
def showOrders():
    data = getDictionary(session=session)
    return render_template('showOrder.html', dictionary=data)


@storeApp.route('/showOrderProducts/<int:orderID>', methods=['POST', 'GET'])
def showOrderProducts(orderID):
    data = getDictionary(orderID=orderID, session=session)
    return render_template('showOrderProducts.html', dictionary=data)
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
    try:
        return redirect(request.referrer)
    except:
        return storeHome()


@storeApp.route('/more/<string:prod_id>')
def showProductDates(prod_id):
    data = getDictionary(session=session, prod_id=int(prod_id))
    return render_template('test.html', dictionary=data)


@storeApp.route('/add/<string:prodDate_id>', methods=['POST', 'GET'])
def addToCart(prodDate_id):
    if shoppingCart.addProduct(int(prodDate_id), session):
        session.pop('product', None)
        return redirect(request.referrer)
    else:
        session['product'] = prodDate_id
        return createCart()


@storeApp.route('/remove/<string:prodDate_id>', methods=['POST', 'GET'])
def removeFromCart(prodDate_id):
    if shoppingCart.removeProduct(int(prodDate_id), session):
        return redirect(request.referrer)
    return storeHome()


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


@storeApp.route('/account', methods=['POST', 'GET'])
def accountPage():
    if request.method == 'POST':
        depositSuccess = user.addMoney(session, request)
        flash(depositSuccess, category="money")
    data = getDictionary(session=session, accountInfo = True)
    return render_template('konto.html', dictionary = data)


@storeApp.route('/change/<string:column>', methods=['POST', 'GET'])
def changeAccount(column):
    if not user.change(column, session, request.form[column]):
        flash("Gick inte att genomföra byte av "+column, category=column)
    return redirect(request.referrer)


@storeApp.route('/delete/<int:cart_id>')
def removeCart(cart_id):
    shoppingCart.removeCart(cart_id)
    try:
        session['cart'] = shoppingCart.getCarts(session['email'])[0]
    except:
        session.pop('cart', None)
    return redirect(request.referrer)



"""
    ADMIN SITES
"""

@storeApp.route('/Admin')
def adminHome():
    if user.isAdmin(session):
        session['isAdmin'] = True
        return render_template("adminBase.html", dictionary=getAdminDict(select=None))
    return storeHome()

@storeApp.route('/Admin/view/<string:activity>')
def adminSelect(activity):
    adminDictionary = getAdminDict(select=activity)
    if user.isAdmin(session):
        return render_template("admin.html", dictionary=adminDictionary)
    return storeHome()

@storeApp.route('/Admin/create/<string:activity>', methods=['POST', 'GET'])
def create(activity):
    if user.isAdmin(session):
        if request.method == 'POST':
            if createFunction(choice=activity, request=request):
                flash("Insättning genomförd av " + activity, category=activity)
            else:
                flash("Gick inte att genomföra insättning av " + activity, category=activity)
        return redirect(request.referrer)
    else:
        return storeHome()

@storeApp.route('/Admin/finishOrder')
def finishOrder():
    if user.isAdmin(session):
        return render_template("adminOrderFinish.html", dictionary=getAdminDict(select='orders'))
    return redirect(request.referrer)

@storeApp.route('/Admin/finishOrder/<string:order_id>')
def sendOrder(order_id):
    if user.isAdmin(session):
        order.send(order_id)
        return render_template("adminOrderFinish.html", dictionary=getAdminDict(select='orders'))
    return redirect(request.referrer)

@storeApp.route('/Admin/orderInfo/<string:order_id>')
def orderInfo(order_id):
    if user.isAdmin(session):
        orderInfo = order.getOrderInfo(order_id)
        return render_template("adminOrderInfo.html", dictionary=getAdminDict(select='orders'), orderInfo=orderInfo)
    return redirect(request.referrer)

@storeApp.route('/Admin/changeProduct/<string:prod_id>', methods=['GET', 'POST'])
def changeProduct(prod_id):
    if user.isAdmin(session):
        if request.method == 'GET':
            return render_template("adminChange.html",
                                   changeDictionary=getChangeDict(change='products', prod_id=prod_id),
                                   dictionary = getAdminDict(select='products'))
        else:
            Error = product.update(request, prod_id)
            flash(Error, category='changeProduct')
            return redirect(request.referrer)
    else:
        return storeHome()


@storeApp.route('/Admin/deleteReview/<int:reviewID>/<string:prodID>')
def deleteReview(reviewID, prodID):
    if user.isAdmin(session):
        try:
            review.removeReview(reviewID, session, prodID)
        except:
            pass
        return redirect(request.referrer)
    return storeHome()


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




