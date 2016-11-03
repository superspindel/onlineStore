from flask import Flask, render_template
from src.database.Database import Database

storeApp = Flask(__name__)
storeApp.secret_key = "hfudsyf7h4373hfnds9y32nfw93hf"


@storeApp.route('/')
def storeHome():
    return render_template('base.html')


#@storeApp.before_first_request
#def initialize_database():
#    Database.initialize()

if __name__ == '__main__':
    storeApp.run(port=4995)