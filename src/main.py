from flask import Flask, render_template, request
from src.database.Database import Database

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


#@storeApp.before_first_request
def initialize_database():
    Database.initialize()

if __name__ == '__main__':
    storeApp.run(port=4995)