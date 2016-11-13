from flask import Flask, render_template, request
from database.Database import Database
from common.item import item
from common.user import user

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


@storeApp.route('/auth/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html', login=False)
    else:

        if request.form['email'] == 'kalle@mail.com' and request.form['password'] == 'password':
            return render_template('login.html', login=True)


@storeApp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html', register=False)
    else:
        newUser = user


@storeApp.route('/test')
def test():
    itemList = Database.getUserInfo()
    return render_template('test.html', database=itemList)


@storeApp.before_first_request
def initialize_database():
    Database.initialize()
    kalle = user("kalle", "kalle@mail.com", "fiskmas", "97751", "professorsvägen 23", "luleå", "sverige", "070-2675108",
                 "891123-1515", None)
    print(kalle.format())
    Database.insert("User", kalle.format())


def randomItemForCart():
    itemList = []
    itemList.append(item("1","skinka", "39", "skinka med allt"))
    itemList.append(item("2", "senap", "14", "senap till smörgås"))
    itemList.append(item("3", "fisk", "99", "fisk från skärgården"))
    return itemList

if __name__ == '__main__':
    storeApp.run(port=4995)

#host='0.0.0.0'
