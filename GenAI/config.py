import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBUhJQeUWiQ2Q6N7O1fhRJXPbP2IGzP23g')

# Supported Indian languages for translation
SUPPORTED_LANGUAGES = {
    'English': 'en',
    'Hindi': 'hi',
    'Bengali': 'bn',
    'Telugu': 'te',
    'Marathi': 'mr',
    'Tamil': 'ta',
    'Gujarati': 'gu',
    'Kannada': 'kn',
    'Malayalam': 'ml',
    'Punjabi': 'pa',
    'Odia': 'or',
    'Assamese': 'as',
    'Urdu': 'ur',
    'Sanskrit': 'sa',
    'Nepali': 'ne',
    'Bhojpuri': 'bh'
}

# Risk keywords for detection (English and Hindi)
RISK_KEYWORDS = {
    'penalties': ['penalty', 'fine', 'charge', 'fee', 'cost', 'damages', 'जुर्माना', 'दंड', 'शुल्क', 'लागत'],
    'data_sharing': ['data', 'information', 'personal', 'privacy', 'share', 'third party', 'डेटा', 'जानकारी', 'निजी', 'गोपनीयता', 'साझा'],
    'auto_renewal': ['auto-renew', 'automatic', 'renewal', 'subscription', 'recurring', 'स्वचालित', 'नवीकरण', 'सदस्यता'],
    'lock_in': ['termination', 'cancel', 'exit', 'lock-in', 'binding', 'commitment', 'समाप्ति', 'रद्द', 'बाध्यकारी', 'प्रतिबद्धता'],
    'unfair_terms': ['liability', 'disclaimer', 'warranty', 'guarantee', 'responsibility', 'दायित्व', 'अस्वीकरण', 'वारंटी', 'जिम्मेदारी']
}
