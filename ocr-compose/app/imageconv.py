# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo

import pytesseract
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anubhav'  # Change this to a secret key for security
app.config['MONGO_URI'] = 'mongodb://mongo:27017/test'  # Update with your MongoDB URI

mongo = PyMongo(app)
db = mongo.db


if 'savestext' not in db.list_collection_names():
    try:
        db.create_collection('savestext')
    except CollectionInvalid:
        # Handle the case where another thread/process created the collection simultaneously
        pass

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Replace this with your actual user authentication logic
users = {'anubhav': {'password': 'anubhav'}}  # Set your default username and password

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        user = User()
        user.id = user_id
        return user

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            user = User()
            user.id = username
            login_user(user)
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/process_image', methods=['POST'])
@login_required
def process_image():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"
    else:
        filename = file.filename

    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    # Store the result text in MongoDB
    db.savestext.insert_one({'filename': filename, 'text': text})

    return render_template('results.html', text=text)

@app.route('/display_results')
@login_required
def display_results():
    # Retrieve results from MongoDB
    results = db.savestext.find()  # Corrected collection name
    return render_template('display_results.html', results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

