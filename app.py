from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from utils.predictor import predict_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('upload-form.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return "No file uploaded", 400

    file = request.files['image']
    filename = file.filename

    if not filename:
        return "No selected file", 400

    if allowed_file(filename):
        safe_filename = secure_filename(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        file.save(filepath)

        # Get prediction from real model
        result = predict_image(filepath)

        if not result['success']:
            return f"Prediction error: {result['error']}", 500

        # Now result has 'baseline' and 'enhanced'
        baseline_result = result['baseline']
        enhanced_result = result['enhanced']

        return render_template(
            'result.html',
            image_path=safe_filename,
            baseline=baseline_result,
            enhanced=enhanced_result
        )

    return "Invalid file format", 400


if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=5000)