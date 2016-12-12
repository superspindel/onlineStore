try:
    from storeSite.common.user import user
except:
    from common.user import user
try:
    from database.Database import Database
except:
    from storeSite.database.Database import Database
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
try:
    from common.shoppingCart import shoppingCart, cartProduct
except:
    from storeSite.common.shoppingCart import shoppingCart, cartProduct
try:
    from storeSite.common.review import review
except:
    from common.review import review
try:
    from common.Image import Image
except:
    from storeSite.common.Image import Image
try:
    from storeSite.common.orders import order
except:
    from common.orders import order
import os

"""
Function name: createUser
Input variables: request that comes from the register route
Info: Takes a specific request and takes all the data needed to create a user and returns an object of the class user
"""


"""
Function name: checkUserLogin
Input variables: request that comes from the login route
Info: Creates an object with a connection to the database, gets the login email from the request, initialized the database,
Selects from the database the password of the user who is trying to log in, from the cursor that contains the returned data we try to
get the password, then rehashes the password from the request, closes the database connection and then returns a boolean depending
on if the password is correct.
"""
def getAdminDict(**kwargs):
    data = {}
    data['products'] = product.getfullCatalog()
    if kwargs['select'] == 'categories':
        data['categories'] = Category.getCategories()
    elif kwargs['select'] == 'users':
        data['users'] = user.GetAllUsers()
    elif kwargs['select'] == 'shoppingCarts':
        data['shoppingCarts'] = shoppingCart.getAllCarts()
    elif kwargs['select'] == 'Images':
        data['images'] = Image.getAllImages()
    elif kwargs['select'] == 'reviews':
        data['reviews'] = review.getAllReviews()
    try:
        data['pictureNames'] = os.listdir("/Users/viktor/PycharmProjects/storeSite/storeSite/static/images/products")
    except:
        data['pictureNames'] = os.listdir("/var/www/onlineStore/storeSite/static/images/products")
    data['select'] = kwargs['select']
    return data


def createFunction(choice, request):
    if choice == 'product':
        try:
            newProduct = product(prodID=request.form['prodID'], name=request.form['prodName'],
                                 description=request.form['prodDesc'], price=request.form['prodPrice'],
                                 salePrice=request.form['prodSale'], grade=0, numbOfGrades=0, catID=request.form['catID'])
            newProduct.insert()
            return True
        except:
            return False
    elif choice == 'image':
        try:
            newImage = Image(imageID=request.form['imageID'], prodID=request.form['imgProdID'],
                             imagePlacement=request.form['imgPlacement'], imageSource=request.form['imgSource'])
            newImage.insert()
            return True
        except:
            return False
    elif choice == 'prodDate':
        try:
            newDate = prodDate(dateStart=request.form['dateStart'], dateEnd=request.form['dateEnd'],
                               prodDateID=request.form['prodDateID'], prodID=request.form['prodDateProdID'],
                               quantity=request.form['quantity'])
            newDate.insert()
            return True
        except:
            return False

def SearchFor(value):
    searchDict = {}
    searchDict['products'] = product.searchForProducts(value)
    searchDict['subCategories'] = Category.searchForSubCategories(value)
    return searchDict


def getDictionary(**kwargs):
    data = {'categories': Category.getCategories()}
    try:
        data['userEmail'] = kwargs['session']['email']
        data['shoppingCarts'] = shoppingCart.getCarts(kwargs['session']['email'])
        data['cartProds'] = shoppingCart.getCartProducts(kwargs['session']['cart'])
        data['activeCart'] = kwargs['session']['cart']
    except:
        pass
    try:
        data['catalog'] = Category.getSpecificCatalog(kwargs['cat_id'])
    except:
        pass
    try:
        data['searchResult'] = SearchFor(str(kwargs['request'].form['searchfield']))
    except:
        pass
    try:
        data['productDates'] = prodDate.getTimesAvaliable(kwargs['prod_id'])
        data['prodInfo'] = product.getProduct(kwargs['prod_id'])
    except:
        pass
    try:
        data['reviewList'] = review.fetchReviews(kwargs['prod_id'], kwargs['session'])
        data['myReviews'] = review.fetchMyReviews(kwargs['prod_id'], kwargs['session'])
    except:
        pass
    try:
        if kwargs['accountInfo']:
            data['user'] = user.getAccountInfo(kwargs['session']['email'])
    except:
        pass
    try:
        data['searchText'] = str(kwargs['request'].form['searchfield'])
    except:
        pass
    try:
        data['allReviews'] = review.fetchAllReviews(kwargs['prod_id'])
    except:
        pass
    try:
        data['myOrders'] = order.fetchOrders(kwargs['session'])
    except:
        pass
    try:
        data['myOrderProducts'] = order.fetchOrderProducts(kwargs['orderID'])
        data['currentOrder'] = order.fetchSpecificOrder(kwargs['orderID'])
        data['orderPrice'] = order.getOrderPrice(kwargs['orderID'])
    except:
        pass
    return data