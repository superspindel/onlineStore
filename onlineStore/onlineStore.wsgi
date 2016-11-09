#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/onlineStore/onlineStore/onlineStore")

from onlineStore import storeApp as application
application.secret_key = 'hfudsyf7h4373hfnds9y32nfw93hf'
