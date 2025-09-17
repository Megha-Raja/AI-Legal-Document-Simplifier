"""
AI Legal Document Simplifier - Flask Application
Modern, elegant web interface for legal document analysis
"""

from flask import Flask, render_template, request, jsonify, session
import os
import json
from werkzeug.utils import secure_filename
from document_parser import DocumentParser
from ai_utils import AIProcessor
from config import SUPPORTED_LANGUAGES

app = Flask(__name__)
app.secret_key = 'ai-legal-doc-simplifier-2024-secure-key'  # Secret key for session encryption

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize components
parser = DocumentParser()
ai_processor = None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def initialize_ai():
    """Initialize AI processor"""
    global ai_processor
    try:
        ai_processor = AIProcessor()
        return True
    except Exception as e:
        print(f"AI initialization error: {e}")
        return False

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', languages=SUPPORTED_LANGUAGES)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF or DOCX files only.'}), 400
        
        # Validate file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'File too large. Maximum size is 10MB.'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse document
        with open(filepath, 'rb') as f:
            file_content = f.read()
        
        document_data = parser.extract_text(file_content, filename)
        
        # Store in session
        session['document_data'] = document_data
        session['filename'] = filename
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'word_count': document_data['word_count'],
            'format': document_data['format']
        })
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/analyze', methods=['POST'])
def analyze_document():
    """Analyze uploaded document"""
    try:
        if not session.get('document_data'):
            return jsonify({'error': 'No document uploaded'}), 400
        
        if not ai_processor:
            if not initialize_ai():
                return jsonify({'error': 'AI service unavailable'}), 500
        
        data = request.get_json()
        language = data.get('language', 'English')
        
        document_data = session['document_data']
        
        # Generate summary
        summary = ai_processor.summarize_document(document_data['text'], language)
        
        # Store summary in session
        session['summary'] = summary
        
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/risks', methods=['POST'])
def detect_risks():
    """Detect risks in document using LLM analysis"""
    try:
        if not session.get('document_data'):
            return jsonify({'error': 'No document uploaded'}), 400
        
        if not ai_processor:
            return jsonify({'error': 'AI service unavailable'}), 500
        
        data = request.get_json()
        language = data.get('language', 'English')
        
        document_data = session['document_data']
        
        # Detect risks using LLM
        risks = ai_processor.detect_risks_advanced(document_data['text'], language)
        
        # Store risks in session
        session['risks'] = risks
        
        return jsonify({
            'success': True,
            'risks': risks
        })
        
    except Exception as e:
        return jsonify({'error': f'Risk detection failed: {str(e)}'}), 500

@app.route('/safety', methods=['POST'])
def get_safety_recommendation():
    """Get safety recommendation for the document"""
    try:
        if not session.get('document_data') or not session.get('risks'):
            return jsonify({'error': 'Document analysis required'}), 400
        
        if not ai_processor:
            return jsonify({'error': 'AI service unavailable'}), 500
        
        data = request.get_json()
        language = data.get('language', 'English')
        
        document_data = session['document_data']
        risks = session['risks']
        
        # Get safety recommendation
        recommendation = ai_processor.get_safety_recommendation(
            document_data['text'], 
            risks, 
            language
        )
        
        return jsonify({
            'success': True,
            'recommendation': recommendation
        })
        
    except Exception as e:
        return jsonify({'error': f'Safety analysis failed: {str(e)}'}), 500

@app.route('/chat', methods=['POST'])
def chat_with_document():
    """Handle chatbot queries"""
    try:
        if not session.get('document_data'):
            return jsonify({'error': 'No document uploaded'}), 400
        
        if not ai_processor:
            return jsonify({'error': 'AI service unavailable'}), 500
        
        data = request.get_json()
        question = data.get('question', '')
        language = data.get('language', 'English')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        document_data = session['document_data']
        
        # Get answer
        answer = ai_processor.answer_question(question, document_data['text'], language)
        
        return jsonify({
            'success': True,
            'answer': answer
        })
        
    except Exception as e:
        return jsonify({'error': f'Chat failed: {str(e)}'}), 500

if __name__ == '__main__':
    # Initialize AI on startup
    initialize_ai()
    app.run(debug=True, host='0.0.0.0', port=5000)
