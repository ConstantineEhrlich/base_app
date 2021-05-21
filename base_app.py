# Everything starts in this file. It imports the app from the app and all the models
from app import app
from app.models import *


# Then, it assigns some values to the environment so we can run Flask shell
# and use the objects of 'db', 'User', 'Record', etc.
# Test change in Textastic app and then push it from ipad
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Record': Record}
