try:
    from database.Database import Database
except:
    from storeSite.database.Database import Database
try:
    from storeSite.common.user import user
except:
    from common.user import user
import random


class shoppingCart(object):

    def __init__(self, cartID, userID):
        self.cartID = cartID
        self.userID = userID

    @staticmethod
    def insertProduct(cursor):
        cartProducts = []
        for name, prodDateid, price, amount , prodID in cursor:
            cartProducts.append(cartProduct(name, prodDateid, price, amount, prodID))
        return cartProducts

    @staticmethod
    def addToCart(cartID, prodDate_ID, mydb):
        mydb.selectWhere("storeDB.ProductDate.prodID", "storeDB.ProductDate", "prodDateID", prodDate_ID)
        prodID = mydb.cursor.fetchone()[0]
        mydb.selectWhere("storeDB.Product.price, storeDB.Product.SalePrice", "storeDB.Product", "prodID", prodID)
        prices = mydb.cursor.fetchone()
        prodPrice = min(prices[0], prices[1])
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
        mydb.nestedSelect("product.name, shopping.prodDateID, shopping.price, shopping.amount, product.prodID",
                          "storeDB.Product as product, storeDB.shoppingProducts as shopping",
                          "shopping.cartID", cartID, "product.prodID", "storeDB.ProductDate.prodID",
                          "storeDB.ProductDate", "storeDB.ProductDate.prodDateID", "shopping.prodDateID")
        return shoppingCart.insertProduct(mydb.cursor)

    @staticmethod
    def removeProductFromCart(prodDate_id, cartID, mydb):
        mydb.startTransaction()
        mydb.updateAnd("storeDB.shoppingProducts", "amount", "amount-1", "cartID", cartID, "prodDateID", prodDate_id)
        if mydb.cursor.rowcount < 1:
            mydb.deleteFromAnd("storeDB.shoppingProducts", "prodDateID", prodDate_id, "cartID", cartID)
        mydb.update("storeDB.ProductDate", "quantity", "quantity+1", "prodDateID", prodDate_id)
        mydb.commit()
        mydb.deleteFromAnd("storeDB.shoppingProducts", "amount", 0, "cartID", cartID)
        mydb.commit()

    @staticmethod
    def removeProduct(prodDate_id, session):
        cartID = session['cart']
        mydb = Database()
        shoppingCart.removeProductFromCart(prodDate_id, cartID, mydb)
        mydb.end()

    @staticmethod
    def getCarts(userEmail):
        mydb = Database()
        userID = user.getUserID(userEmail, mydb)
        carts = []
        mydb.selectWhere("storeDB.shoppingcart.cartID", "storeDB.shoppingcart", "userID", userID)
        for cartID in mydb.cursor:
            carts.append(cartID[0])
        mydb.end()
        return carts

    @staticmethod
    def getCartProducts(cartID=None):
        mydb = Database()
        return shoppingCart.getCart(cartID, mydb)

    @staticmethod
    def addProduct(prodDate_id, session):
        if 'cart' in session:
            mydb = Database()
            mydb.selectWhere("storeDB.ProductDate.quantity", "storeDB.ProductDate", "prodDateID", prodDate_id)
            if mydb.cursor.fetchone()[0] > 0:
                shoppingCart.addToCart(session['cart'], prodDate_id, mydb)
            mydb.end()
            return True
        else:
            return False

    @staticmethod
    def removeCart(cart_id):
        mydb = Database()
        mydb.startTransaction()
        prodList = []
        mydb.selectWhere("storeDB.shoppingProducts.prodDateID, storeDB.shoppingProducts.amount",
                         "storeDB.shoppingProducts", "cartID", cart_id)
        for prodDateID, amount in mydb.cursor:
            prodList.append([prodDateID, amount])
        for prodDateID, amount in prodList:
            mydb.update("storeDB.ProductDate", "quantity", "quantity+"+str(amount), "prodDateID", prodDateID)
        mydb.deleteFrom("storeDB.shoppingProducts", "cartID", cart_id)
        mydb.deleteFrom("storeDB.shoppingcart", "cartID", cart_id)
        mydb.commit()
        mydb.end()

    @staticmethod
    def cartList(cursor):
        cartList = []
        for cartID, userID in cursor:
            cartList.append(shoppingCart(cartID, userID))
        return cartList

    @staticmethod
    def getAllCarts():
        mydb = Database()
        mydb.select("*", "storeDB.shoppingcart")
        cartList = shoppingCart.cartList(mydb.cursor)
        mydb.end()
        return cartList


class cartProduct(object):

    def __init__(self, name, prodDateid, price, amount, prodID):
        self.name = name
        self.prodDateid = prodDateid
        self.price = price
        self.amount = amount
        self.prodID = prodID