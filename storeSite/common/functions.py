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
    except:
        pass
    try:
        data['catalog'] = Category.getSpecificCatalog(kwargs['cat_id'])
    except:
        pass
    try:
        data['searchResult'] = SearchFor(kwargs['request'].form['searchfield'])
    except:
        pass
    try:
        data['productDates'] = prodDate.getTimesAvaliable(kwargs['prod_id'])
        data['prodInfo'] = product.getProduct(kwargs['prod_id'])
    except:
        pass
    return data