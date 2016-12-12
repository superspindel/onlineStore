from datetime import date
from random import randint
try:
    from database.Database import Database
except:
    from storeSite.database.Database import Database
try:
    from storeSite.common.user import user
except:
    from common.user import user
try:
    from storeSite.common.product import shoppingProduct, product
except:
    from common.product import shoppingProduct, product
	
class order(object):
    def __init__(self, orderID, orderDate, orderStatus, userID, discCode):
        self.orderID = str(randint(1, 2147483646)) if orderID is None else orderID
        self.orderDate = date.today()
        self.orderStatus = orderStatus
        self.userID = userID
        self.discCode = discCode
		
    @staticmethod
    def fetchOrders(session):
        mydb = Database()
        currentUserID = user.getUserID(session['email'], mydb)
        mydb.selectWhere("*", "storeDB.orders", "userID", currentUserID)
        orderList = order.getOrderList(mydb.cursor)
        mydb.end()
        return orderList

    @staticmethod
    def getOrderList(cursor):
        return [order(orderID, orderDate, orderStatus, userID, discCode)
                     for orderID, orderDate, orderStatus, userID, discCode in cursor]

    @staticmethod
    def fetchSpecificOrder(orderID):
        mydb = Database()
        mydb.selectWhere("*", "storeDB.orders", "orderID", orderID)
        newOrder = order.getOrderList(mydb.cursor)[0]
        mydb.end()
        return newOrder
		
    @staticmethod
    def fetchOrderProducts(orderID):
        mydb = Database()
        mydb.selectMaxxa("*", "storeDB.Product", "prodID", "prodID", "storeDB.ProductDate", "ProdDateID", "ProdDateID", "storeDB.shoppingProducts", "orderID", orderID)
        productList = product.createCatalog(mydb.cursor)
        mydb.end()
        return productList
		
    def addOrder(self, mydb):
        mydb.insert("storeDB.orders", self.format())
        mydb.commit()
		
    def format(self):
        if not self.discCode:
            return "{}, '{}', {}, {}, NULL".format(self.orderID, self.orderDate, self.orderStatus, self.userID)
        return "{}, '{}', {}, {}, '{}'".format(self.orderID, self.orderDate, self.orderStatus, self.userID,
                                               self.discCode)
		
    @staticmethod
    def createOrder(request, session, cartID):
        mydb = Database()
        totalPrice = order.getPrice(mydb, cartID)
        userInfo = user.getAccountInfo(session['email'])
        if userInfo.balance > totalPrice:
            mydb.selectWhere("*", "storeDB.discounts", "code", "'"+request.form['discount']+"'")
            if mydb.cursor.rowcount < 1:
                mydb.startTransaction()
                newOrder = order(orderID=None, orderDate = date.today(), orderStatus = 1, userID = user.getUserID(session['email'], mydb), discCode = False)
                newOrder.addOrder(mydb)
                order.updateProducts(mydb, cartID, newOrder.orderID)
            else:
                mydb.startTransaction()
                newOrder = order(orderID=None, orderDate = date.today(), orderStatus = 1, userID = user.getUserID(session['email'], mydb), discCode = request.form['discount'])
                newOrder.addOrder(mydb)
                order.updateProducts(mydb, cartID, newOrder.orderID)
            order.updateBalance(mydb, totalPrice, userInfo)
            mydb.end()
            return True
        else:
            return False

    @staticmethod
    def updateBalance(mydb, totalPrice, userInfo):
        newBalance = userInfo.balance - totalPrice
        mydb.update("storeDB.User", "accountBalance", newBalance, "userID", userInfo.userID)
        mydb.commit()

    @staticmethod
    def getPrice(mydb, cartID):
        mydb.selectWhere("*", "storeDB.shoppingProducts", "cartID", cartID)
        productList = shoppingProduct.getShoppingProductList(mydb.cursor)
        return sum(product.Price for product in productList)

    @staticmethod
    def getOrderPrice(orderID):
        mydb = Database()
        mydb.selectWhere("*", "storeDB.shoppingProducts", "orderID", orderID)
        productList = shoppingProduct.getShoppingProductList(mydb.cursor)
        mydb.end()
        return sum(product.Price for product in productList)

    @staticmethod
    def updateProducts(mydb, cartID, orderID):
        mydb.update("storeDB.shoppingProducts", "orderID", orderID, "cartID", cartID)
        mydb.update("storeDB.shoppingProducts", "cartID", "NULL", "cartID", cartID)
        mydb.commit()