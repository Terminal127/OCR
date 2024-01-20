from flask import Flask, render_template, request
import pytesseract
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    image = Image.open(file)
    text = pytesseract.image_to_string(image)

    return render_template('result.html', text=text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

