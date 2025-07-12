import os
import json
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class GeminiCorrector:
    def __init__(self):
        """
        Initialize Gemini corrector with API configuration
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Initialize Gemini model
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        self.client = genai.Client(api_key=api_key)

    def _structure_text(self, ocr_result: List) -> str:
        """
        Structure OCR result into a tabular format
        Args:
            ocr_result: PaddleOCR output with bounding boxes
        Returns:
            str: Structured text with tabs and newlines
        """
        # Sort elements by their vertical position
        text_elements = []
        for line in ocr_result:
            bbox = line[0]
            text = line[1][0].strip()
            confidence = line[1][1]
            
            if text:  # Skip empty text
                text_elements.append({
                    'text': text,
                    'bbox': bbox,
                    'confidence': confidence
                })
        
        # Sort by vertical position
        text_elements.sort(key=lambda x: x['bbox'][0][1])
        
        # Group into rows based on vertical proximity
        rows = []
        current_row = []
        previous_y = None
        
        for element in text_elements:
            y = element['bbox'][0][1]
            if previous_y is not None and abs(y - previous_y) > 10:  # New row threshold
                if current_row:
                    rows.append(current_row)
                    current_row = []
            current_row.append(element)
            previous_y = y
        
        if current_row:
            rows.append(current_row)
        
        # Create structured text
        structured_text = []
        for row in rows:
            # Sort row by horizontal position
            row.sort(key=lambda x: x['bbox'][0][0])
            row_text = '\t'.join([e['text'] for e in row])
            structured_text.append(row_text)
        
        return '\n'.join(structured_text)

    def _call_gemini(self, structured_text: str) -> str:
        """
        Call Gemini API to correct and structure the text
        Args:
            structured_text: Structured text with tabs and newlines
        Returns:
            str: Gemini API response
        """

        prompt = f"""
            Extract grocery items with their quantities from this register text.
            Important:
            1. Correct any errors in item names resulted from OCR
            2. Quantities must represent current inventory count
            3. If multiple quantity columns exist, use the one that represents inventory
            4. Output must be pure JSON string, no json markdown such as "```json```"
            Format: [{{"name": "item", "quantity": count}}]
            Text:
            {structured_text}
        """

        try:
            self.logger.info(f"Calling Gemini API with text:\n{structured_text}")
            response = self.client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            return str(response.text)
        except Exception as e:
            self.logger.error(f"Gemini API call failed: {str(e)}")
            return "[]"

    def _parse_gemini_response(self, response: str) -> List[Dict[str, Any]]:
        """
        Parse Gemini's JSON response into a list of dictionaries
        Args:
            response: Gemini API response text
        Returns:
            List[Dict[str, Any]]: List of item dictionaries
        """
        try:
            # Clean the response by removing any non-JSON text
            response = response.strip()
            if response.startswith("[") and response.endswith("]"):
                return json.loads(response)
            return []
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse Gemini response: {str(e)}")
            return []

    def parse_ocr_result_with_gemini(self, ocr_result: List) -> List[Dict[str, Any]]:
        """
        Process OCR result using Gemini API
        Args:
            ocr_result: PaddleOCR output with bounding boxes
        Returns:
            List[Dict[str, Any]]: List of item dictionaries with names and quantities
        """
        try:
            # Structure the text
            structured_text = self._structure_text(ocr_result)
            self.logger.info(f"Structured text:\n{structured_text}")
            
            # Call Gemini API
            gemini_response = self._call_gemini(structured_text)
            self.logger.info(f"Gemini response:\n{gemini_response}")
            
            # Parse the response
            return self._parse_gemini_response(gemini_response)
            
        except Exception as e:
            self.logger.error(f"Error processing OCR result: {str(e)}")
            return []

# Singleton instance
gemini_corrector = GeminiCorrector()

def parse_ocr_result_with_gemini(ocr_result: List) -> List[Dict[str, Any]]:
    """
    Process OCR result through Gemini API
    Args:
        ocr_result: PaddleOCR output with bounding boxes
    Returns:
        List[Dict[str, Any]]: List of item dictionaries
    """
    return gemini_corrector.parse_ocr_result_with_gemini(ocr_result)
