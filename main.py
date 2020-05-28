#Contents of this exam where referenced from INFO2602 Labs 4-9 and Extra Lab.
#ID: 816013096
import json
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required
from flask import Flask, request, render_template, redirect, flash, url_for
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 

from models import db, Logs , Todo, User #add application models
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
  app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) # uncomment if using flsk jwt
  CORS(app)
  login_manager.init_app(app) # uncomment if using flask login
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()
db.create_all(app=app)
''' End Boilerplate Code '''


''' Set up JWT here (if using flask JWT)'''
def authenticate(uname, password):
  user = User.query.filter_by(username=uname).first()
  #if user is found and password matches
  if user and user.check_password(password):
      return user

 ##Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
   return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''


@app.route('/index', methods=['POST'])
def login():
    data = request.form
    user = User.query.filter_by(username = data['username']).first()
    if user and user.check_password(data['password']): # check credentials
      flash('Logged in successfully.') # send message to next page
      login_user(user) # login the user
      return redirect(url_for('get_app')) # redirect to main page if login successful
    else:
      flash('Invalid username or password') # send message to next page
    return render_template('index.html')

@app.route('/', methods=['GET'])
def login_page():
  return render_template('index.html')


#@app.route('/app', methods=['GET'])
#@login_required
#def Quips():
  #QuipStack = Todo.query.filter_by(user_id=current_user.id).all()

  #if QuipStack is None:
     #QuipStack = []

  #form = Status()

  #if form.validate_on_submit():
    #data = request.form
    #newQuip = Status(Thought=data['name'], user_id=current_user.id)
    #db.session.add(newQuip)
    #db.session.commit()
    #flash('Quip Added')
    #return redirect(url_for('Quips'))

  #return render_template('app.html', form=form, Todo=QuipStack)

#imported stuff
@app.route('/app', methods=['GET'])
@login_required
def get_app():
  todos = todos = Todo.query.filter_by(userid=current_user.id).all()
  return render_template('app.html', todos=todos)

@app.route('/identify')
@jwt_required()
def protected():
    return json.dumps(current_identity.username)

@app.route('/todo', methods=['POST'])
@jwt_required()
def create_todo():
  data = request.get_json()
  todo = Todo(text=data['text'], userid=current_identity.id, done=False)
  db.session.add(todo)
  db.session.commit()
  return json.dumps({ 'id' : todo.id}), 201 # return data and set the status code

@app.route('/todo', methods=['GET'])
@jwt_required()
def get_todos():
  todos = Todo.query.filter_by(userid=current_identity.id).all()
  todos = [todo.toDict() for todo in todos] # list comprehension which converts todo objects to dictionaries
  return json.dumps(todos)

@app.route('/todo/<id>', methods=['GET'])
@jwt_required()
def get_todo(id):
  todo = Todo.query.filter_by(userid=current_identity.id, id=id).first()
  if todo == None:
    return 'Invalid id or unauthorized'
  return json.dumps(todo.toDict())

@app.route('/todo/<id>', methods=['PUT'])
@jwt_required()
def update_todo(id):
  todo = Todo.query.filter_by(userid=current_identity.id, id=id).first()
  if todo == None:
    return 'Invalid id or unauthorized'
  data = request.get_json()
  if 'text' in data: # we can't assume what the user is updating wo we check for the field
    todo.text = data['text']
  if 'done' in data:
    todo.done = data['done']
  db.session.add(todo)
  db.session.commit()
  return 'Updated', 201

@app.route('/todo/<id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
  todo = Todo.query.filter_by(userid=current_identity.id, id=id).first()
  if todo == None:
    return 'Invalid id or unauthorized'
  db.session.delete(todo) # delete the object
  db.session.commit()
  return 'Deleted', 204

@app.route('/users', methods=['GET'])
def get_users():
  users = User.query.all()
  results = []
  for user in users:
    rec = user.toDic() # convert user object to dictionary record
    rec['num_todos'] = user.getNumTodos() # add num todos to dictionary record
    rec['num_done'] = user.getDoneTodos() # add num done todos to dictionary record
    results.append(rec)
  return json.dumps(results)

@app.route('/createTodo', methods=['POST'])
@login_required
def create_todo2():
  data = request.form
  todo = Todo(text=data['text'], userid=current_user.id, done=False)
  db.session.add(todo)
  db.session.commit()
  flash('Created')
  return redirect(url_for('get_app'))

@app.route('/updateTodo/<id>', methods=['POST'])
@login_required
def update_todo2(id):
  done = request.form.get('done') # either 'on' or 'None'
  todo = Todo.query.filter_by(userid=current_user.id, id=id).first()
  if todo == None:
    flash('Invalid id or unauthorized') 
  todo.done = True if done == 'on' else False
  flash('Done!') if todo.done else flash ('Not Done!')
  db.session.add(todo)
  db.session.commit()
  
  return redirect(url_for('get_app'))


@app.route('/deleteTodo/<id>', methods=["GET"])
@login_required
def delete_todo2(id):
  todo = Todo.query.filter_by(userid=current_user.id, id=id).first()
  if todo == None:
    flash ('Invalid id or unauthorized')
  db.session.delete(todo) # delete the object
  db.session.commit()
  flash ('Deleted!')
  return redirect(url_for('get_app'))


#@app.route('/app')
#def client_app():
 # return app.send_static_file('app.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
