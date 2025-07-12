# 🛒 Kirana Store Reorder Assistant

A web application that helps Pakistani kirana store owners manage their inventory by processing handwritten sales register images and suggesting reorders.

## Features

- Upload handwritten sales register images in Urdu or English
- Automatic item and quantity extraction using OCR
- Smart reorder suggestions based on stock levels
- WhatsApp notifications for reorder suggestions
- Clean and intuitive web interface

## Getting Started

### Initial Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd smartstock-ai
   ```

2. **Switch to Master Branch**
   ```bash
   git checkout master
   ```

3. **Set Up Python Environment**
   - Install Python using pyenv (recommended):
     ```bash
     # Install pyenv if not installed
     curl https://pyenv.run | bash
     
     # Install Python 3.12.11
     pyenv install 3.12.11
     
     # Set Python 3.12.11 as local version
     pyenv local 3.12.11
     ```
   
   - Alternative: Install Python 3.12.11 directly
     - Download from: https://www.python.org/downloads/release/python-31211/
     - Follow installation instructions for your operating system

   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

4. **Configure Environment**
   - Contact the project maintainer to get the `.env` file containing all necessary configuration:
     - Email: mehroz.muzaffar@gmail.com
     - GitHub: @mehroz-muzaffar-32

### Running the Application

1. **Start the Server**
   ```bash
   python app.py
   ```

2. **Access the Application**
   Open your browser and go to `http://localhost:5000`

### Development Workflow

1. **Before Making Changes**
   - Always start by switching to the development branch:
     ```bash
     git checkout feature/created-flask-project
     ```

2. **Creating New Features**
   - Create a new branch for your changes:
     ```bash
     git checkout -b feature/your-feature-name
     ```

3. **After Making Changes**
   - Add your changes:
     ```bash
     git add .
     ```
   - Commit your changes:
     ```bash
     git commit -m "Your descriptive commit message"
     ```
   - Push to your branch:
     ```bash
     git push origin feature/your-feature-name
     ```

4. **Creating Pull Requests**
   - Go to your repository on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Set base branch to `feature/created-flask-project`
   - Write a clear description of your changes
   - Submit the pull request

### Recommended Tools

- **Editor**: Windsurf AI Editor
  - Provides AI-powered assistance for development
  - Helps with code completion and debugging
  - Makes development faster and more efficient

## Core Components

### Main Application (`app.py`)
- Flask web server with routes for:
  - `/`: Main page with upload form
  - `/upload`: API endpoint for image processing
- Configuration:
  - Upload folder: `uploads`
  - Max file size: 16MB
  - Environment variables via dotenv

### OCR Processing (`ocr/ocr_processor.py`)
- Uses PaddleOCR for image processing
- Extracts items and quantities from images
- Supports Urdu and English text

### Reorder Logic (`logic/reorder_logic.py`)
- Generates reorder suggestions
- Threshold-based reorder recommendations
- Default threshold: 3 units

### WhatsApp Integration (`messaging/whatsapp.py`)
- Uses Twilio for WhatsApp messaging
- Sends reorder suggestions to store owners

### Frontend (`templates/index.html`)
- Modern UI with Tailwind CSS

## Technical Stack

### Python Version
- Python 3.12.11 (via pyenv)

### Dependencies
```plaintext
Flask==2.3.3
Pillow==10.3.0
paddlepaddle==2.6.1
paddleocr==2.7.3
twilio==8.11.0
python-dotenv==1.0.1
numpy==1.26.4
setuptools>=65.5.0
```

## Project Structure
```
smartstock-ai/
├── app.py              # Main Flask application
├── ocr/                # OCR processing code
├── logic/              # Business logic
├── messaging/          # WhatsApp messaging
├── templates/          # HTML templates
├── uploads/            # Image uploads
├── static/             # Static files
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
└── .gitignore          # Git ignore rules
```

## Security Considerations
- Environment variables for sensitive data
- File upload validation
- Error handling for OCR processing

## Areas for Improvement

1. Add image preprocessing
2. Implement user authentication
3. Add database integration
4. Enhance reorder logic
5. Add API rate limiting
6. Implement caching
7. Add comprehensive error handling

## Next Steps

1. Implement image preprocessing
2. Add database for storing inventory
3. Enhance reorder suggestions
4. Add user authentication
5. Implement proper logging
6. Add unit tests

## 📸 Demo

| Upload Interface         | Results Table            | WhatsApp Output         |
|--------------------------|---------------------------|--------------------------|
| ![Upload](assets/upload.png) | ![Result](assets/result.png) | ![WhatsApp](assets/whatsapp.png) |

> *(Replace the `assets/` image links with your actual screenshot paths)*

---

## 🚀 How It Works

1. Shopkeeper uploads a register image
2. OCR engine extracts item names and quantities
3. AI logic decides what to reorder
4. Results shown on dashboard and optionally sent on WhatsApp

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit / HTML + Tailwind CSS
- **Backend**: Flask / FastAPI (Python)
- **OCR**: Google Vision API / PaddleOCR
- **Messaging**: Twilio WhatsApp Sandbox
- **Hosting**: Render / Railway / Replit

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/kiryana-stock-agent.git
cd kiryana-stock-agent

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
