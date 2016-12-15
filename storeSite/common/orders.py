import datetime
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
try:
    from common.prodDate import prodDate
except:
    from storeSite.common.prodDate import prodDate

class order(object):
    def __init__(self, orderID, orderStatus, userID, discCode, orderDate=None):
        self.orderID = str(randint(1, 2147483646)) if orderID is None else orderID
        self.orderDate = datetime.datetime.today() if orderDate is None else orderDate
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
        return [order(orderID=orderID, orderDate=orderDate, orderStatus=orderStatus, userID=userID, discCode=discCode)
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
        mydb.selectWhere("*", "storeDB.shoppingProducts", "orderID", orderID)
        productList = [shoppingProduct(shoppingProdID, amount, cartID, orderId, prodDateID, Price) for
                       shoppingProdID, amount, cartID, orderId, prodDateID, Price in mydb.cursor]
        mydb.end()
        return productList

    @staticmethod
    def fetchOrderProductsInfo(orderID):
        mydb = Database()
        mydb.selectMaxxa("*", "storeDB.Product", "prodID", "prodID", "storeDB.ProductDate", "ProdDateID", "ProdDateID",
                         "storeDB.shoppingProducts", "orderID", orderID)
        productList = [product(prodID=prodID, name=name, description=description, price=price, salePrice=salePrice,
                               grade=grade, numbOfGrades=numbOfGrades, dateAdded=dateAdded, catID=catID) for
                       prodID, name, description, price, salePrice, grade, numbOfGrades, dateAdded, catID in
                       mydb.cursor]
        mydb.end()
        return productList

    @staticmethod
    def fetchOrderProductsExtra(orderID):
        mydb = Database()
        mydb.selectMaxxaMindre("*", "storeDB.ProductDate", "prodDateID", "prodDateID", "storeDB.shoppingProducts",
                               "orderID", orderID)
        productList = [prodDate(prodID=prodID, dateStart=dateStart, dateEnd=dateEnd, prodDateID=prodDateID, quantity=quantity) for
                       prodID, dateStart, dateEnd, prodDateID, quantity in mydb.cursor]
        mydb.end()
        return productList
		
    def addOrder(self, mydb):
        mydb.insert("storeDB.orders", self.format())
		
    def format(self):
        if not self.discCode:
            return "{}, '{}', {}, {}, NULL".format(self.orderID, self.orderDate, self.orderStatus, self.userID)
        return "{}, '{}', {}, {}, '{}'".format(self.orderID, self.orderDate, self.orderStatus, self.userID,
                                               self.discCode)
		
    @staticmethod
    def createOrder(request, session, cartID):
        mydb = Database()
        mydb.startTransaction()
        totalPrice = order.getPrice(mydb, cartID)
        if totalPrice == 0:
            return "Inga produkter i din korg"
        userInfo = user.getAccountInfo(session['email'])
        if userInfo.balance > totalPrice:
            mydb.selectWhere("*", "storeDB.discounts", "code", "'"+request.form['discount']+"'")
            if mydb.cursor.rowcount < 1:
                newOrder = order(orderID=None, orderStatus=1,
                                 userID=user.getUserID(session['email'], mydb), discCode=False)
                newOrder.addOrder(mydb)
                order.updateProducts(mydb, cartID, newOrder.orderID)
            else:
                newOrder = order(orderID=None, orderStatus=1,
                                 userID=user.getUserID(session['email'], mydb), discCode=request.form['discount'])
                newOrder.addOrder(mydb)
                order.updateProducts(mydb, cartID, newOrder.orderID)
            order.updateBalance(mydb, totalPrice, userInfo)
            mydb.commit()
            mydb.end()
            return "Beställning genomförd"
        else:
            return "Inte nog med pengar på ditt konto"

    @staticmethod
    def updateBalance(mydb, totalPrice, userInfo):
        newBalance = userInfo.balance - totalPrice
        mydb.update("storeDB.User", "accountBalance", newBalance, "userID", userInfo.userID)

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

    @staticmethod
    def getAllOrders():
        mydb = Database()
        mydb.select("*", "storeDB.orders")
        orderList = order.getOrderList(mydb.cursor)
        mydb.end()
        return orderList

    @staticmethod
    def send(orderID):
        mydb = Database()
        mydb.update("storeDB.orders", "orderStatus", 2, "orderID", orderID)
        mydb.commit()
        mydb.end()

    @staticmethod
    def getOrderInfo(order_id):
        mydb = Database()
        mydb.selectWhere("storeDB.shoppingProducts.prodDateID", "storeDB.shoppingProducts",
                         "storeDB.shoppingProducts.orderID", order_id)
        prodDateIDList = [id[0] for id in mydb.cursor]
        listan = [order.getOrderProdDate(id) for id in prodDateIDList]
        return prodDate.getProdDateList(listan)

    @staticmethod
    def getOrderProdDate(id):
        mydb=Database()
        mydb.selectWhere("*", "storeDB.ProductDate", "storeDB.ProductDate.prodDateID", id)
        y = mydb.cursor.fetchone()
        mydb.end()
        return y




