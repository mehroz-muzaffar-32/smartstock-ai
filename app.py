from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, login_required, current_user
from werkzeug.utils import secure_filename
import os
import logging
from dotenv import load_dotenv
from models import db, User
from ocr.ocr_processor import process_image
from logic.reorder_logic import generate_reorder_suggestions
from messaging.whatsapp import send_whatsapp_message

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.update({
    'SECRET_KEY': os.getenv('SECRET_KEY', 'dev-key-change-in-production'),
    'UPLOAD_FOLDER': 'uploads',
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,
    'ALLOWED_EXTENSIONS': {'png', 'jpg', 'jpeg', 'gif'},
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///app.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
})

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def validate_phone_number(phone_number):
    return phone_number and len(phone_number) >= 10

# Routes
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    # Validate request
    if 'multipart/form-data' not in request.content_type:
        return jsonify({'error': 'Invalid content type'}), 400
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    try:
        # Process file
        filename = secure_filename(file.filename)
        if not filename:
            return jsonify({'error': 'Invalid filename'}), 400
            
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'Failed to save file'}), 500
        
        # Process image through OCR
        items, upload_id = process_image(filepath)
        if not items:
            return jsonify({'error': 'No items found in image'}), 400
        # Generate reorder suggestions from detected items
        reorder_suggestions = generate_reorder_suggestions(items)
        if not reorder_suggestions:
            return jsonify({'error': 'Failed to generate suggestions'}), 500

        # Handle WhatsApp notification
        whatsapp_status = None
        whatsapp_message = None
        phone_number = request.form.get('phone_number')
        
        if phone_number:
            if not validate_phone_number(phone_number):
                return jsonify({'error': 'Invalid phone number'}), 400
            try:
                send_whatsapp_message(phone_number, reorder_suggestions)
                whatsapp_status = 'success'
                whatsapp_message = 'Message sent successfully'
            except Exception as e:
                app.logger.error(f"WhatsApp error: {str(e)}")
                whatsapp_status = 'error'
                whatsapp_message = 'Failed to send WhatsApp message'

        # Prepare response
        response = {
            'success': True,
            'items': items,
            'reorder_suggestions': reorder_suggestions,
            'saved_file': filename
        }
        
        if whatsapp_status:
            response.update({
                'whatsapp_status': whatsapp_status,
                'whatsapp_message': whatsapp_message
            })

        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Processing error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

# Register blueprints
from auth.routes import auth
from inventory.routes import inventory

# Register authentication blueprint
app.register_blueprint(auth, url_prefix='/auth')

# Register inventory blueprint
app.register_blueprint(inventory, url_prefix='/inventory')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)