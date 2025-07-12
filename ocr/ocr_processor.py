from paddleocr import PaddleOCR
from preprocessing.image_cleaner import ImageCleaner
from corrector.gemini_corrector import parse_ocr_result_with_gemini
import cv2
import os
import logging
import numpy as np
import re
from typing import List, Dict

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class OCRProcessor:
    """
    Process images to extract items and quantities using OCR with Gemini correction
    """
    def __init__(self):
        """
        Initialize OCR processor with PaddleOCR and image cleaner
        """
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        self.cleaner = ImageCleaner()
        self.logger = logger

    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess image for OCR
        Args:
            image_path: Path to the image file
        Returns:
            np.ndarray: Preprocessed image ready for OCR
        Raises:
            Exception: If preprocessing fails
        """
        try:
            self.logger.info(f"Preprocessing image: {image_path}")
            return self.cleaner.process_image(image_path)
        except Exception as e:
            self.logger.error(f"Preprocessing failed for {image_path}: {str(e)}")
            raise

    def process_image(self, image_path):
        """
        Process image and extract items and quantities using OCR with Gemini correction
        Args:
            image_path: Path to the image file
        Returns:
            list: List of items with names and quantities
        """
        try:
            # Preprocess image first
            preprocessed_image = self.preprocess_image(image_path)
            
            # Convert NumPy array to temporary file for PaddleOCR
            temp_file = f"{os.path.splitext(image_path)[0]}_processed.jpg"
            cv2.imwrite(temp_file, preprocessed_image)
            
            # Run OCR on processed image
            result = self.ocr.ocr(temp_file, cls=True)
            
            # Clean up temporary file
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            # Use Gemini corrector to process OCR result
            items = parse_ocr_result_with_gemini(result[0])
            
            # Log if no items were found
            if not items:
                self.logger.warning(f"No items found in image {image_path}")
            
            return items
            
        except Exception as e:
            self.logger.error(f"Error processing image {image_path}: {str(e)}")
            return []

# Singleton instance
ocr_processor = OCRProcessor()

def process_image(image_path):
    """
    Process image through OCR with preprocessing
    Args:
        image_path: Path to the image file
    Returns:
        list: List of items with names and quantities
    """
    return ocr_processor.process_image(image_path)
