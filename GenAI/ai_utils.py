"""
AI Utilities Module
Handles all AI operations using Google Gemini API
Includes summarization, translation, Q&A, and risk detection
"""

import google.generativeai as genai
from typing import Dict, List, Any, Optional
import json
import re
from config import GEMINI_API_KEY, SUPPORTED_LANGUAGES, RISK_KEYWORDS


class AIProcessor:
    """Handles all AI operations using Gemini API"""
    
    def __init__(self):
        """Initialize Gemini API"""
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found. Please set it in your environment variables.")
        
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def summarize_document(self, text: str, language: str = 'English') -> Dict[str, Any]:
        """
        Summarize legal document into simple, key points
        
        Args:
            text: Extracted document text
            language: Target language for summary
            
        Returns:
            Dictionary containing summary and key points
        """
        try:
            prompt = f"""
            You are a legal document expert specializing in Indian legal documents. Please analyze this legal document and provide:
            
            1. A brief summary (2-3 sentences) in {language}
            2. Key points in simple, plain language (5-7 bullet points) in {language}
            3. Important dates, deadlines, or timeframes mentioned
            4. Main parties involved
            
            If the language is Hindi or any Indian language, please respond in that language using appropriate script (Devanagari for Hindi, etc.).
            Make the language simple and easy to understand for common people.
            
            Document text:
            {text[:4000]}  # Limit text to avoid token limits
            
            Please format your response as JSON:
            {{
                "summary": "Brief summary here",
                "key_points": ["Point 1", "Point 2", "Point 3"],
                "important_dates": ["Date 1", "Date 2"],
                "parties": ["Party 1", "Party 2"]
            }}
            """
            
            response = self.model.generate_content(prompt)
            result = self._parse_json_response(response.text)
            
            return {
                'summary': result.get('summary', 'Summary not available'),
                'key_points': result.get('key_points', []),
                'important_dates': result.get('important_dates', []),
                'parties': result.get('parties', []),
                'language': language
            }
            
        except Exception as e:
            return {
                'summary': f"Error generating summary: {str(e)}",
                'key_points': [],
                'important_dates': [],
                'parties': [],
                'language': language
            }
    
    def translate_text(self, text: str, target_language: str) -> str:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_language: Target language name (e.g., 'Spanish', 'French')
            
        Returns:
            Translated text
        """
        try:
            prompt = f"""
            Translate the following text to {target_language}. 
            Maintain the original meaning and legal context.
            If translating to Hindi or any Indian language, use the appropriate script (Devanagari for Hindi, etc.).
            Make the translation simple and easy to understand for common people.
            Return only the translated text without any additional formatting.
            
            Text to translate:
            {text}
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return f"Translation error: {str(e)}"
    
    def answer_question(self, question: str, document_text: str, language: str = 'English') -> str:
        """
        Answer questions about the document using context
        
        Args:
            question: User's question
            document_text: Original document text
            language: Language for the answer
            
        Returns:
            Answer in the specified language
        """
        try:
            prompt = f"""
            You are a legal assistant specializing in Indian legal documents. Answer the following question about the legal document.
            Base your answer on the document content provided.
            Respond in {language} in a clear, simple manner.
            If the language is Hindi or any Indian language, use the appropriate script (Devanagari for Hindi, etc.).
            Make your answer easy to understand for common people.
            
            Question: {question}
            
            Document context:
            {document_text[:3000]}  # Limit context to avoid token limits
            
            Please provide a direct, helpful answer based on the document content.
            If the information is not available in the document, say so clearly.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return f"Error answering question: {str(e)}"
    
    def detect_risks_advanced(self, text: str, language: str = 'English') -> Dict[str, Any]:
        """
        Advanced risk detection using LLM analysis instead of keywords
        
        Args:
            text: Document text to analyze
            language: Language for risk descriptions
            
        Returns:
            Dictionary containing detected risks and warnings
        """
        try:
            prompt = f"""
            You are an expert legal risk analyst specializing in Indian legal documents. Analyze this legal document thoroughly and identify potential risks using your understanding of legal language and context.
            
            IMPORTANT: Do not rely on simple keyword matching. Instead, analyze the actual meaning and context of sentences to determine if they pose real risks.
            
            Look for and analyze:
            1. Penalty and fee structures - Are they reasonable or excessive?
            2. Data collection and sharing policies - What data is collected and how is it used?
            3. Auto-renewal and subscription terms - Are users properly informed?
            4. Termination and cancellation clauses - Are they fair to users?
            5. Liability limitations and disclaimers - Are they overly broad?
            6. Unfair contract terms - Any terms that heavily favor one party?
            7. Hidden charges or fees - Any costs not clearly disclosed?
            8. Lock-in periods - Are users trapped in contracts?
            
            For each genuine risk found (not just keyword matches), provide:
            - Risk type (be specific)
            - Clear description in {language} (use appropriate script for Indian languages)
            - Severity level (Low/Medium/High) based on actual impact
            - Relevant text excerpt that shows the risk
            
            Only report risks that are actually problematic, not just because certain words appear.
            
            Document text:
            {text[:4000]}
            
            Format as JSON:
            {{
                "risks": [
                    {{
                        "type": "Specific Risk Type",
                        "description": "Clear description in {language}",
                        "severity": "Low/Medium/High",
                        "excerpt": "Exact text showing the risk"
                    }}
                ]
            }}
            """
            
            response = self.model.generate_content(prompt)
            result = self._parse_json_response(response.text)
            
            risks = result.get('risks', [])
            
            # Add risk count and summary
            risk_summary = {
                'total_risks': len(risks),
                'high_risk_count': len([r for r in risks if r.get('severity') == 'High']),
                'medium_risk_count': len([r for r in risks if r.get('severity') == 'Medium']),
                'low_risk_count': len([r for r in risks if r.get('severity') == 'Low']),
                'risks': risks,
                'language': language
            }
            
            return risk_summary
            
        except Exception as e:
            return {
                'total_risks': 0,
                'high_risk_count': 0,
                'medium_risk_count': 0,
                'low_risk_count': 0,
                'risks': [],
                'language': language,
                'error': str(e)
            }
    
    def get_safety_recommendation(self, text: str, risks: Dict[str, Any], language: str = 'English') -> Dict[str, Any]:
        """
        Get safety recommendation based on document analysis
        
        Args:
            text: Original document text
            risks: Detected risks from risk analysis
            language: Language for recommendation
            
        Returns:
            Dictionary containing safety recommendation
        """
        try:
            prompt = f"""
            You are a legal advisor providing safety recommendations for document signing. Based on the document analysis and detected risks, provide a clear recommendation.
            
            Document risks summary:
            - Total risks: {risks.get('total_risks', 0)}
            - High risk: {risks.get('high_risk_count', 0)}
            - Medium risk: {risks.get('medium_risk_count', 0)}
            - Low risk: {risks.get('low_risk_count', 0)}
            
            Detected risks: {json.dumps(risks.get('risks', []), indent=2)}
            
            Provide a safety recommendation in {language} with:
            1. Overall safety level (SAFE/WARNING/DANGER)
            2. Clear recommendation (should they sign or not?)
            3. Specific reasons based on the risks found
            4. Any specific clauses to negotiate or modify
            
            Consider:
            - High risk count indicates danger
            - Medium risk count indicates caution needed
            - Low risk count is generally acceptable
            - Context and severity of individual risks
            
            Format as JSON:
            {{
                "safety_level": "SAFE/WARNING/DANGER",
                "recommendation": "Clear recommendation in {language}",
                "reasons": ["Reason 1", "Reason 2", "Reason 3"],
                "suggestions": ["Suggestion 1", "Suggestion 2"]
            }}
            """
            
            response = self.model.generate_content(prompt)
            result = self._parse_json_response(response.text)
            
            return {
                'safety_level': result.get('safety_level', 'WARNING'),
                'recommendation': result.get('recommendation', 'Please review the document carefully'),
                'reasons': result.get('reasons', []),
                'suggestions': result.get('suggestions', []),
                'language': language
            }
            
        except Exception as e:
            return {
                'safety_level': 'WARNING',
                'recommendation': f'Unable to analyze safety: {str(e)}',
                'reasons': ['Analysis error occurred'],
                'suggestions': ['Please review the document manually'],
                'language': language
            }
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse JSON response from Gemini API
        
        Args:
            response_text: Raw response text from API
            
        Returns:
            Parsed JSON as dictionary
        """
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # If no JSON found, return empty structure
                return {}
        except json.JSONDecodeError:
            # If JSON parsing fails, return empty structure
            return {}
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get list of supported languages
        
        Returns:
            Dictionary of language names and codes
        """
        return SUPPORTED_LANGUAGES
    
    def validate_language(self, language: str) -> bool:
        """
        Check if language is supported
        
        Args:
            language: Language name to validate
            
        Returns:
            True if supported, False otherwise
        """
        return language in SUPPORTED_LANGUAGES
