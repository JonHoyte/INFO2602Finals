#Contents of this exam where referenced from INFO2602 Labs 4-9 and Extra Lab.
#ID: 816013096
import json
from main import app
from models import db,User


db.create_all(app=app)
#initializing database, and creating 2 Users
user = User(username="bob")
user.set_password('bobpass')
db.session.add(user)
user = User(username="john")
user.set_password('johnpass')

db.session.add(user)
db.session.commit()
         


print('database initialized!')