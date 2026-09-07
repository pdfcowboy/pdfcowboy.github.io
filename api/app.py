import os
import subprocess
import tempfile
import logging
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

# ── Setup ─────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app, origins=[
    'https://pdfcowboy.github.io',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 25 * 1024 * 1024   # 25 MB
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

ALLOWED_QUALITY = {'screen', 'ebook', 'printer', 'prepress'}

# ── Health / wake-up ping ──────────────────────────────────────────
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'awake'}), 200

# ── Compress endpoint ──────────────────────────────────────────────
@app.route('/compress', methods=['POST'])
def compress():
    # Validate file presence
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    f = request.files['file']
    if not f.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400

    # Validate file size
    f.seek(0, 2)
    size = f.tell()
    f.seek(0)
    if size > MAX_FILE_SIZE:
        return jsonify({'error': f'File too large — maximum 25 MB'}), 413

    # Quality setting
    quality = request.form.get('quality', 'ebook')
    if quality not in ALLOWED_QUALITY:
        quality = 'ebook'

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path  = os.path.join(tmpdir, 'input.pdf')
            output_path = os.path.join(tmpdir, 'output.pdf')

            f.save(input_path)
            input_size = os.path.getsize(input_path)

            # Run Ghostscript
            result = subprocess.run([
                'gs',
                '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.4',
                f'-dPDFSETTINGS=/{quality}',
                '-dNOPAUSE',
                '-dQUIET',
                '-dBATCH',
                '-dDetectDuplicateImages=true',
                '-dCompressFonts=true',
                f'-sOutputFile={output_path}',
                input_path
            ], capture_output=True, text=True, timeout=120)

            if result.returncode != 0:
                logger.error(f'Ghostscript error: {result.stderr}')
                return jsonify({'error': 'Compression failed — invalid or corrupted PDF'}), 500

            output_size = os.path.getsize(output_path)
            saving_bytes = input_size - output_size
            saving_pct   = round((saving_bytes / input_size) * 100, 1) if input_size > 0 else 0

            logger.info(f'Compressed: {input_size} → {output_size} bytes ({saving_pct}% saving)')

            # Build output filename
            original_name = secure_filename(f.filename)
            base_name     = original_name.rsplit('.', 1)[0]
            out_filename  = f'{base_name}_compressed.pdf'

            return send_file(
                output_path,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=out_filename,
                max_age=0,
            )

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Compression timed out — try a smaller file'}), 504
    except Exception as e:
        logger.exception('Unexpected error during compression')
        return jsonify({'error': str(e)}), 500


# ── File too large handler ─────────────────────────────────────────
@app.errorhandler(413)
def file_too_large(e):
    return jsonify({'error': 'File too large — maximum 25 MB'}), 413


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
