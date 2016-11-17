from flask import Flask, render_template, request
from database.Database import Database
from common.functions import createUser, checkUserLogin

storeApp = Flask(__name__)
storeApp.secret_key = "hfudsyf7h4373hfnds9y32nfw93hf"


@storeApp.route('/')
def storeHome():
    return render_template('home.html')


@storeApp.route('/Category/<string:cat_id>')
def categories(cat_id):
    return render_template('Category.html', category_id=cat_id)


@storeApp.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        return render_template('search.html', searchtext=request.form['searchfield'])


@storeApp.route('/auth/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        if checkUserLogin(request):
            return render_template('test.html', status="True")
        else:
            return render_template('test.html', status="False")
        #set session
        #return homepage

@storeApp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html', register=False)
    else:
        newUser = createUser(request)
        mydb = Database()
        mydb.initialize()
        newUser.registerUser(mydb)
        mydb.end()
        return render_template('home.html')


@storeApp.route('/test')
def test():
    itemList = Database.getUserInfo()
    return render_template('test.html', database=itemList)


@storeApp.before_first_request
def initialize_database():
    pass

if __name__ == '__main__':
    storeApp.run(port=4995, host='0.0.0.0')
