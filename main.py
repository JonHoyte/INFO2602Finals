import json
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required
from flask import Flask, request, render_template, redirect, flash, url_for
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 

from models import db, Logs , Todo, User #add application models
from forms import LogIn , Status
''' Begin boilerplate code '''

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
        return User.query.get(user_id)

''' End Flask Login Functions '''

def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  #app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) # uncomment if using flsk jwt
  CORS(app)
  # login_manager.init_app(app) # uncomment if using flask login
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()
db.create_all(app=app)
''' End Boilerplate Code '''

''' Set up JWT here (if using flask JWT)'''
#def authenticate(uname, password):
  #user = User.query.filter_by(username=uname).first()
  #if user is found and password matches
  #if user and user.check_password(password):
    #return user

 ##Payload is a dictionary which is passed to the function by Flask JWT
#def identity(payload):
  # return User.query.get(payload['identity'])

#jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''


@app.route('/', methods=['GET', 'POST'])
def login():
  form = LogIn()
  if form.validate_on_submit(): # respond to form submission
    data = request.form
    user = User.query.filter_by(username = data['username']).first()
    if user and user.check_password(data['password']): # check credentials
      flash('Logged in successfully.') # send message to next page
      login_user(user) # login the user
      return redirect(url_for('app')) # redirect to main page if login successful
    else:
      flash('Invalid username or password') # send message to next page
      return redirect(url_for('login')) # redirect to login page if login unsuccessful
  return render_template('index.html', form=form)


#@app.route('/app', methods=['GET', 'POST'])
#@login_required
#def Quips():
  #QuipStack = Todo.query.filter_by(user_id=current_user.id).all()

  #if QuipStack is None:
     # QuipStack = []

  #form = Status()

  #if form.validate_on_submit():
    #data = request.form
    #newQuip = Status(Thought=data['name'], user_id=current_user.id)
    #db.session.add(newQuip)
    #db.session.commit()
    #flash('Quip Added')
    #return redirect(url_for('Quips'))

  #return render_template('app.html', form=form, Todo=QuipStack)

#@app.route('/Todo/<id>', methods=['POST'])
#@login_required
 #def delete_Quip(id):
  #remove = Todo.query.filter_by(user_id=current_user.id, id=id).first() # retrieve ingredient to remove
  #if remove == None:
    #return 'Invalid id or unauthorized'
  #db.session.delete(remove) # delete the ingredient
  #db.session.commit()
  #flash('Quip Deleted!')
  #return redirect(url_for('Quips'))


#@app.route('/app')
#def client_app():
 # return app.send_static_file('app.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
