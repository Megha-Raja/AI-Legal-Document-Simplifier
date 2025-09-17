"""
Test script for AI Legal Document Simplifier MVP
Run this to test basic functionality without the Streamlit interface
"""

import os
from document_parser import DocumentParser
from ai_utils import AIProcessor
from config import SUPPORTED_LANGUAGES

def test_document_parser():
    """Test document parser functionality"""
    print("🧪 Testing Document Parser...")
    
    parser = DocumentParser()
    
    # Test file validation
    test_cases = [
        ("test.pdf", 1024, True),
        ("test.docx", 1024, True),
        ("test.txt", 1024, False),
        ("test.pdf", 20 * 1024 * 1024, False),  # Too large
    ]
    
    for filename, size, expected in test_cases:
        result = parser.validate_file(filename, size)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {filename} ({size} bytes): {result}")
    
    print("✅ Document Parser tests completed\n")

def test_ai_processor():
    """Test AI processor functionality"""
    print("🧪 Testing AI Processor...")
    
    # Check if API key is set
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ GEMINI_API_KEY not found. Please set it in your environment.")
        print("   You can set it by running: export GEMINI_API_KEY=your_key_here")
        return False
    
    try:
        ai_processor = AIProcessor()
        print("✅ AI Processor initialized successfully")
        
        # Test language validation
        test_languages = ['English', 'Spanish', 'InvalidLanguage']
        for lang in test_languages:
            result = ai_processor.validate_language(lang)
            status = "✅" if result else "❌"
            print(f"  {status} Language '{lang}': {result}")
        
        # Test supported languages
        languages = ai_processor.get_supported_languages()
        print(f"✅ Supported languages: {len(languages)} languages available")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Processor initialization failed: {str(e)}")
        return False

def test_sample_processing():
    """Test sample text processing"""
    print("🧪 Testing Sample Text Processing...")
    
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ Skipping sample processing - API key not set")
        return
    
    try:
        ai_processor = AIProcessor()
        
        # Sample legal text
        sample_text = """
        TERMS OF SERVICE
        
        1. ACCEPTANCE OF TERMS
        By accessing and using this service, you agree to be bound by these terms.
        
        2. PAYMENT TERMS
        You agree to pay all fees within 30 days. Late payments incur a 5% penalty.
        
        3. DATA COLLECTION
        We may collect and share your personal information with third parties.
        
        4. TERMINATION
        This agreement automatically renews unless terminated with 30 days notice.
        """
        
        print("📝 Processing sample legal text...")
        
        # Test summarization
        print("  🔄 Testing summarization...")
        summary = ai_processor.summarize_document(sample_text, 'English')
        print(f"  ✅ Summary generated: {len(summary['key_points'])} key points")
        
        # Test risk detection
        print("  🔄 Testing risk detection...")
        risks = ai_processor.detect_risks(sample_text, 'English')
        print(f"  ✅ Risk analysis completed: {risks['total_risks']} risks found")
        
        # Test Q&A
        print("  🔄 Testing Q&A...")
        answer = ai_processor.answer_question(
            "What happens if I pay late?", 
            sample_text, 
            'English'
        )
        print(f"  ✅ Q&A working: Answer length {len(answer)} characters")
        
        print("✅ Sample processing tests completed\n")
        
    except Exception as e:
        print(f"❌ Sample processing failed: {str(e)}\n")

def main():
    """Run all tests"""
    print("🚀 AI Legal Document Simplifier - MVP Test Suite\n")
    
    # Test document parser
    test_document_parser()
    
    # Test AI processor
    ai_working = test_ai_processor()
    
    # Test sample processing if AI is working
    if ai_working:
        test_sample_processing()
    
    print("🎉 Test suite completed!")
    print("\n📋 Next steps:")
    print("1. Set your GEMINI_API_KEY if not already done")
    print("2. Run 'streamlit run app.py' to start the web interface")
    print("3. Upload a test document to verify full functionality")

if __name__ == "__main__":
    main()
