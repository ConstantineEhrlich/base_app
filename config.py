# this is configuration file
# it uses some functions from os, therefore:
import os
from typing import Optional

basedir = os.path.abspath(os.path.dirname(__file__))


# this is class Config, wehre we're assiging some variables
class Config(object):
    SECRET_KEY = \
        os.environ.get('SECRET_KEY') or 'NONSECRET_KEY'
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get('DATABASE_URL') or ('sqlite:///' + os.path.join(basedir, 'app.db'))
