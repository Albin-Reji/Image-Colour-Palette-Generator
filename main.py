import os
from flask import Flask, render_template, request
from PIL import Image
from collections import Counter

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_most_common_colors(image_path, num_colors=5):
    image = Image.open(image_path)
    image = image.convert('RGB')
    image_colors = image.getdata()
    color_counter = Counter(image_colors)
    most_common_colors = color_counter.most_common(num_colors)
    return most_common_colors

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error='No selected file')

        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            most_common_colors = get_most_common_colors(filename)
            return render_template('index.html', filename=file.filename, colors=most_common_colors)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
