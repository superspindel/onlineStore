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


def getChangeDict(**kwargs):
    data = {}
    if kwargs['change'] == 'products':
        data['changeProduct'] = product.getProduct(kwargs['prod_id'])
        data['change'] = 'products'
    return data

def getAdminDict(**kwargs):
    data = {}
    data['products'] = product.getfullCatalog()
    data['primaryCategories'] = Category.getPrimaryCategories()
    data['subCategories'] = Category.getSubCategories()
    data['select'] = kwargs['select']
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
    elif kwargs['select'] == 'orders':
        data['orders'] = order.getAllOrders()
    try:
        data['pictureNames'] = os.listdir("/Users/viktor/PycharmProjects/storeSite/storeSite/static/images/products")
    except:
        data['pictureNames'] = os.listdir("/var/www/onlineStore/storeSite/static/images/products")
    return data


def createFunction(choice, request):
    if choice == 'product':
        return insertProduct(request)
    elif choice == 'image':
        return insertImage(request)
    elif choice == 'prodDate':
        return insertProdDate(request)
    elif choice == 'category':
        return insertCategory(request)
    elif choice == 'subcategory':
        return insertSubCategory(request)

def insertSubCategory(request):
    try:
        category = Category(name=request.form['subCatName'], catID=request.form['subCatID'],
                            subCatID=request.form['subID'])
        category.insertSubCategory()
        return True
    except:
        return False

def insertCategory(request):
    try:
        category = Category(name=request.form['catName'], catID=request.form['catID'])
        category.insertMainCategory()
        return True
    except:
        return False

def insertProduct(request):
    try:
        newProduct = product(prodID=request.form['prodID'], name=request.form['prodName'],
                             description=request.form['prodDesc'], price=request.form['prodPrice'],
                             salePrice=request.form['prodSale'], grade=0, numbOfGrades=0,
                             catID=request.form['prodCatID'])
        newProduct.insert()
        return True
    except:
        return False

def insertImage(request):
    try:
        newImage = Image(imageID=request.form['imageID'], prodID=request.form['imgProdID'],
                         imagePlacement=request.form['imgPlacement'], imageSource=request.form['imgSource'])
        newImage.insert()
        return True
    except:
        return False

def insertProdDate(request):
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

    if 'session' in kwargs:
        if 'email' in kwargs['session']:
            data['userEmail'] = kwargs['session']['email']
            data['shoppingCarts'] = shoppingCart.getCarts(kwargs['session']['email'])
            if 'prod_id' in kwargs:
                data['reviewList'] = review.fetchReviews(kwargs['prod_id'], kwargs['session'])
                data['myReviews'] = review.fetchMyReviews(kwargs['prod_id'], kwargs['session'])
            if 'accountInfo' in kwargs:
                data['user'] = user.getAccountInfo(kwargs['session']['email'])

        if 'cart' in kwargs['session']:
            data['cartProds'] = shoppingCart.getCartProducts(kwargs['session']['cart'])
            data['activeCart'] = kwargs['session']['cart']

        if 'orders' in kwargs:
            data['myOrders'] = order.fetchOrders(kwargs['session'])

    if 'cat_id' in kwargs:
        data['catalog'] = Category.getSpecificCatalog(kwargs['cat_id'])

    if 'request' in kwargs:
        data['searchResult'] = SearchFor(str(kwargs['request'].form['searchfield']))
        data['searchText'] = str(kwargs['request'].form['searchfield'])


    if 'prod_id' in kwargs:
        data['productDates'] = prodDate.getTimesAvaliable(kwargs['prod_id'])
        data['prodInfo'] = product.getProduct(kwargs['prod_id'])
        if not 'email' in kwargs['session']:
            data['allReviews'] = review.fetchAllReviews(kwargs['prod_id'])

    if 'orderID' in kwargs:
        data['myOrderProducts'] = order.fetchOrderProducts(kwargs['orderID'])
        data['myOrderProductsInfo'] = order.fetchOrderProductsInfo(kwargs['orderID'])
        data['myOrderProductsExtra'] = order.fetchOrderProductsExtra(kwargs['orderID'])
        data['currentOrder'] = order.fetchSpecificOrder(kwargs['orderID'])
        data['orderPrice'] = order.getOrderPrice(kwargs['orderID'])

    return data