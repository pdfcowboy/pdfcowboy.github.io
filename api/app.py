import os
import tempfile
import logging
import pikepdf
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 25 * 1024 * 1024
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

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

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path  = os.path.join(tmpdir, 'input.pdf')
            output_path = os.path.join(tmpdir, 'output.pdf')
            f.save(input_path)
            input_size = os.path.getsize(input_path)

            # Open and re-save with compression
            with pikepdf.open(input_path) as pdf:
                # Set compression level based on quality
                compress_streams = True
                if quality == 'screen':
                    pdf.save(output_path,
                        compress_streams=True,
                        object_stream_mode=pikepdf.ObjectStreamMode.generate,
                        recompress_flate=True,
                        normalize_content=True)
                elif quality == 'prepress':
                    pdf.save(output_path,
                        compress_streams=False,
                        object_stream_mode=pikepdf.ObjectStreamMode.disable)
                else:
                    pdf.save(output_path,
                        compress_streams=True,
                        object_stream_mode=pikepdf.ObjectStreamMode.generate,
                        recompress_flate=True)

            output_size = os.path.getsize(output_path)
            logger.info(f'Compressed: {input_size} → {output_size} bytes')

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
