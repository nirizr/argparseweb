#!/usr/bin/env python

# TODO: replace with your application path
# i found now way to get it automatically in wsgi :/
APP_DIR = '/var/www/myapp'

import sys, os
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from myapp import application
