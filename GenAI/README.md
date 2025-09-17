# AI Legal Document Simplifier

An intelligent system that simplifies legal documents, translates them into multiple languages, and provides a chatbot interface for document Q&A with risk detection capabilities.

## Features

- **Document Processing**: Upload PDF/DOCX files and extract text
- **AI Summarization**: Convert complex legal text into simple, understandable points
- **Multi-language Support**: Translate summaries and answers into 12+ languages
- **Interactive Chatbot**: Ask questions about your document in your preferred language
- **Risk Detection**: Automatically identify risky clauses (penalties, data sharing, auto-renewals, etc.)
- **User-friendly Interface**: Clean Streamlit-based web interface

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI Model**: Google Gemini API
- **Document Parsing**: PyMuPDF, python-docx
- **Web Scraping**: BeautifulSoup (for future URL support)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd ai-legal-document-simplifier
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 4. Set Environment Variables
Create a `.env` file in the project root:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

Or set it directly in the Streamlit app interface.

### 5. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

### 1. Upload Document
- Go to the "Document Upload" tab
- Upload a PDF or DOCX file (max 10MB)
- Click "Process Document"

### 2. View Summary & Analysis
- Go to the "Summary & Analysis" tab
- Click "Generate Summary" to get a simplified overview
- Click "Detect Risks" to identify potential issues

### 3. Chat with Document
- Go to the "Chat with Document" tab
- Ask questions about your document
- Get answers in your selected language

## Supported Languages

- English
- Spanish
- French
- German
- Italian
- Portuguese
- Hindi
- Chinese (Simplified)
- Japanese
- Korean
- Arabic
- Russian

## Project Structure

```
├── app.py                 # Main Streamlit application
├── document_parser.py     # Document text extraction
├── ai_utils.py           # Gemini API integration
├── config.py             # Configuration and constants
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## API Usage

The system uses Google's Gemini API for:
- Document summarization
- Text translation
- Question answering
- Risk detection

Make sure you have sufficient API quota for your usage.

## Future Enhancements

- [ ] Web scraping for Terms & Conditions from URLs
- [ ] FAISS vector database for improved RAG
- [ ] Advanced risk scoring
- [ ] Document comparison features
- [ ] Export functionality for summaries

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your Gemini API key is correctly set
2. **File Upload Error**: Check file format (PDF/DOCX only) and size (max 10MB)
3. **Processing Error**: Ensure document is not password-protected or corrupted

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify your API key is valid
3. Ensure all dependencies are installed correctly

## License

This project is for educational/hackathon purposes.
