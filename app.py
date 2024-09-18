from flask import Flask, render_template_string, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    receiver = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    with open('index.html', 'r') as f:
        return f.read()

@socketio.on('send_message')
def handle_message(data):
    new_message = Message(sender=data['sender'], receiver=data['receiver'], content=data['message'])
    db.session.add(new_message)
    db.session.commit()
    emit('receive_message', data, broadcast=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables within the app context
    socketio.run(app)