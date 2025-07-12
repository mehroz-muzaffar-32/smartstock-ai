from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from ocr.ocr_processor import process_image
from logic.reorder_logic import generate_reorder_suggestions
from messaging.whatsapp import send_whatsapp_message

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Process image with OCR
            items = process_image(filepath)
            
            # Generate reorder suggestions
            reorder_suggestions = generate_reorder_suggestions(items)
            
            # Send WhatsApp message
            phone_number = request.form.get('phone_number')
            if phone_number:
                send_whatsapp_message(phone_number, reorder_suggestions)
            
            return jsonify({
                'success': True,
                'items': items,
                'reorder_suggestions': reorder_suggestions
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
