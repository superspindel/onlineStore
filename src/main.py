from src import *
from flask import Flask, render_template, request
from src.database.Database import Database
from src.common.item import item

storeApp = Flask(__name__)
storeApp.secret_key = "hfudsyf7h4373hfnds9y32nfw93hf"


@storeApp.route('/')
def storeHome():
    storeList = randomItemForCart()
    return render_template('home.html', shoppingcart=storeList)


@storeApp.route('/Category/<string:cat_id>')
def categories(cat_id):
    return render_template('Category.html', category_id=cat_id)


@storeApp.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        return render_template('search.html', searchtext=request.form['searchfield'], shoppingcart=randomItemForCart())


@storeApp.before_first_request
def initialize_database():
    Database.initialize()


def randomItemForCart():
    itemList = []
    itemList.append(item("1","skinka", "39", "skinka med allt"))
    itemList.append(item("2", "senap", "14", "senap till smörgås"))
    itemList.append(item("3", "fisk", "99", "fisk från skärgården"))
    return itemList

if __name__ == '__main__':
    storeApp.run(port=4995)