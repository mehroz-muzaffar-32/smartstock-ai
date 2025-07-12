from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from ocr.ocr_processor import process_image
from logic.reorder_logic import generate_reorder_suggestions
from messaging.whatsapp import send_whatsapp_message

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Configuration settings
app.config['UPLOAD_FOLDER'] = 'uploads'  # Store uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Permitted image formats

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def validate_phone_number(phone_number):
    """Basic phone number validation."""
    return phone_number and len(phone_number) >= 10  # Basic length check

@app.route('/')
def index():
    """Main index page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    """Handle file upload and processing."""
    # Validate request contains multipart form data
    if not request.content_type or 'multipart/form-data' not in request.content_type:
        return jsonify({'error': 'Request must be multipart/form-data'}), 400

    # Validate image file exists in request
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    # Check if file was selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Verify file extension is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': f'Allowed file types: {", ".join(app.config["ALLOWED_EXTENSIONS"])}'}), 400

    try:
        # Sanitize filename and verify it's valid
        filename = secure_filename(file.filename)
        if not filename:
            return jsonify({'error': 'Invalid filename'}), 400
            
        # Construct full file path
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the uploaded file
        file.save(filepath)
        
        # Verify file was saved successfully
        if not os.path.exists(filepath):
            return jsonify({'error': 'Failed to save file'}), 500
        
        # Process image through OCR
        items = process_image(filepath)
        if not items:
            return jsonify({'error': 'No items detected in image'}), 400
        
        # Generate reorder suggestions from detected items
        reorder_suggestions = generate_reorder_suggestions(items)
        if not reorder_suggestions:
            return jsonify({'error': 'Failed to generate reorder suggestions'}), 500
        
        # Optional WhatsApp notification if phone number provided
        phone_number = request.form.get('phone_number')
        if phone_number:
            if not validate_phone_number(phone_number):
                return jsonify({'error': 'Invalid phone number format'}), 400
            try:
                send_whatsapp_message(phone_number, reorder_suggestions)
            except Exception as e:
                # Log but don't fail the request if WhatsApp fails
                app.logger.error(f"WhatsApp notification failed: {str(e)}")
        
        # Return successful processing results
        return jsonify({
            'success': True,
            'items': items,
            'reorder_suggestions': reorder_suggestions,
            'saved_file': filename
        })

    except Exception as e:
        # Log unexpected errors and return generic error message
        app.logger.error(f"Upload processing error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred during processing'}), 500

if __name__ == '__main__':
    # Run the application in debug mode
    app.run(debug=True)
