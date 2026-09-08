import os
import tempfile
import logging
import fitz  # PyMuPDF
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 25 * 1024 * 1024
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

QUALITY_SETTINGS = {
    'screen':   {'image_quality': 30,  'garbage': 4, 'clean': True},
    'ebook':    {'image_quality': 60,  'garbage': 3, 'clean': True},
    'printer':  {'image_quality': 80,  'garbage': 2, 'clean': True},
    'prepress': {'image_quality': 95,  'garbage': 1, 'clean': False},
}

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'awake'}), 200

@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    f = request.files['file']
    if not f.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400
    f.seek(0, 2); size = f.tell(); f.seek(0)
    if size > MAX_FILE_SIZE:
        return jsonify({'error': 'File too large — maximum 25 MB'}), 413

    quality = request.form.get('quality', 'ebook')
    if quality not in QUALITY_SETTINGS:
        quality = 'ebook'
    settings = QUALITY_SETTINGS[quality]

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path  = os.path.join(tmpdir, 'input.pdf')
            output_path = os.path.join(tmpdir, 'output.pdf')
            f.save(input_path)
            input_size = os.path.getsize(input_path)

            doc = fitz.open(input_path)
            doc.save(
                output_path,
                garbage=settings['garbage'],
                deflate=True,
                clean=settings['clean'],
                deflate_images=True,
                deflate_fonts=True,
                image_quality=settings['image_quality'],
            )
            doc.close()

            output_size = os.path.getsize(output_path)
            saving_pct  = round(((input_size - output_size) / input_size) * 100, 1)
            logger.info(f'Compressed: {input_size} -> {output_size} bytes ({saving_pct}% saving)')

            base_name = secure_filename(f.filename).rsplit('.', 1)[0]
            return send_file(output_path, mimetype='application/pdf',
                as_attachment=True,
                download_name=f'{base_name}_compressed.pdf',
                max_age=0)

    except Exception as e:
        logger.exception('Compression error')
        return jsonify({'error': str(e)}), 500

@app.errorhandler(413)
def file_too_large(e):
    return jsonify({'error': 'File too large — maximum 25 MB'}), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
