from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    todos = db.relationship('Todo', backref='Logs', lazy=True) # sets up a relationship to todos which references User

    def toDict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password":self.password
        }
        
        #hashes the password parameter and stores it in the object
        def set_password(self, password):
            """Create hashed password."""
            self.password = generate_password_hash(password, method='sha256')
        
        #Returns true if the parameter is equal to the object's password property
        def check_password(self, password):
            """Check hashed password."""
            return check_password_hash(self.password, password)
        
        #To String method
        def __repr__(self):
            return '<User {}>'.format(self.username)

class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId =  db.Column(db.Integer, nullable=False)
    stream = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def toDict(self):
        return{
            'id': self.id,
            'studentId': self.studentId,
            'stream': self.stream,
            'created': self.created.strftime("%m/%d/%Y, %H:%M:%S")
        }

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  userid = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False) #set userid as a foreign key to user.id
  text = db.Column(db.String(255), nullable=False) 
  likes = db.Column(db.Integer)
  dislikes = db.Column(db.Integer)
  react = db.Column(db.Boolean,nullable=False)
  owner = db.Column(db.Boolean, nullable=False)

  def toDict(self):
   return {
     'id': self.id,
     'text': self.text,
     'userid': self.userid,
     'done': self.done
   }
