# this has the featue of image download and all 

from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo
import requests
import os
import tempfile
from werkzeug.utils import secure_filename

import pytesseract
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anubhav'  # Change this to a secret key for security
app.config['MONGO_URI'] = 'mongodb://mongo:27017/testdb'  # Update with your MongoDB URI

mongo = PyMongo(app)
db = mongo.db
if 'savestext' not in db.list_collection_names():
    try:
        db.create_collection('savestext')
    except CollectionInvalid:
        # Handle the case where another thread/process created the collection simultaneously
        pass # Corrected collection creation

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

def process_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Use a temporary file to save the downloaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as file:
            file.write(response.content)
            return file.name
    else:
        return None

@app.route('/process_image', methods=['POST'])
@login_required
def process_image():
    if 'file' not in request.files and 'image_url' not in request.form:
        return "No file or image URL provided"

    if 'file' in request.files:
        file = request.files['file']

        if file.filename == '':
            return "No selected file"

        filename = secure_filename(file.filename)  # Use secure_filename to sanitize the filename

        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        db.savestext.insert_one({'filename': filename, 'text': text})

    elif 'image_url' in request.form:
        image_url = request.form['image_url']

        if not image_url:
            return "No image URL provided"

        imagename = process_image_from_url(image_url)

        if not imagename:
            return "Failed to download the image from the provided URL"

        image = Image.open(imagename)
        text = pytesseract.image_to_string(image)
        db.savestext.insert_one({'filename': imagename, 'text': text})

    return render_template('results.html', text=text)

@app.route('/display_results')
@login_required
def display_results():
    # Retrieve results from MongoDB
    results = db.savestext.find()  # Corrected collection name
    return render_template('display_results.html', results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
