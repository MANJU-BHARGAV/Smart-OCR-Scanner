from flask import Flask, render_template, request
import os

from scanner import scan_document
from ocr import extract_text

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def home():

    image_path = None
    scanned_path = None
    extracted_text = ""

    if request.method == 'POST':

        file = request.files['image']

        if file:

            filepath = os.path.join(
                app.config['UPLOAD_FOLDER'],
                file.filename
            )

            file.save(filepath)

            image_path = filepath

            scanned_path = scan_document(filepath)

            if scanned_path:

                extracted_text = extract_text(
                    scanned_path
                )

    return render_template(
        'index.html',
        image_path=image_path,
        scanned_path=scanned_path,
        extracted_text=extracted_text
    )


if __name__ == '__main__':
    app.run(debug=True)