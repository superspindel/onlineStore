try:
    from database.Database import Database
except:
    from storeSite.database.Database import Database
import random


class shoppingCart(object):

    def __init__(self, cartID):
        self.cartID = cartID

    @staticmethod
    def insertProduct(cursor):
        cartProducts = []
        for name, prodDateid, price, amount in cursor:
            cartProducts.append(cartProduct(name, prodDateid, price, amount))
        return cartProducts

    @staticmethod
    def addToCart(userID, prodDate_ID, mydb):
        mydb.selectWhere("storeDB.ProductDate.prodID", "storeDB.ProductDate", "prodDateID", prodDate_ID)
        prodID = mydb.cursor.fetchone()[0]
        mydb.selectWhere("storeDB.Product.price, storeDB.Product.SalePrice", "storeDB.Product", "prodID", prodID)
        prices = mydb.cursor.fetchone()
        prodPrice = min(prices[0], prices[1])
        mydb.selectWhere("storeDB.shoppingcart.cartID", "storeDB.shoppingcart", "userID", userID)
        cartID = mydb.cursor.fetchone()[0]
        mydb.startTransaction()
        mydb.updateAnd("storeDB.shoppingProducts", "amount", "amount+1", "cartID", cartID, "prodDateID", prodDate_ID)
        if mydb.cursor.rowcount < 1:
            insertText = str(random.randint(1, 2147483647))+","+"1"+","+str(cartID)+","+"NULL"+","+str(prodDate_ID) +\
                         ","+str(prodPrice)
            mydb.insert("storeDB.shoppingProducts", insertText)
        mydb.update("storeDB.ProductDate", "quantity", "quantity-1", "prodDateID", prodDate_ID)
        mydb.commit()

    @staticmethod
    def getCart(cartID, mydb):
        mydb.nestedSelect("product.name, shopping.prodDateID, shopping.price, shopping.amount",
                          "storeDB.Product as product, storeDB.shoppingProducts as shopping",
                          "shopping.cartID", cartID, "product.prodID", "storeDB.ProductDate.prodID",
                          "storeDB.ProductDate", "storeDB.ProductDate.prodDateID", "shopping.prodDateID")
        #sqlNestedSelect = "SELECT {} FROM {} WHERE {} = {} AND {} = (SELECT {} from {} where {} = {})"
        return shoppingCart.insertProduct(mydb.cursor)


class cartProduct(object):

    def __init__(self, name, prodDateid, price, amount):
        self.name = name
        self.prodDateid = prodDateid
        self.price = price
        self.amount = amount