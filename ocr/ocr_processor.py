from paddleocr import PaddleOCR
import numpy as np
import re

class OCRProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')

    def process_image(self, image_path):
        """
        Process image and extract items and quantities
        """
        result = self.ocr.ocr(image_path, cls=True)
        items = []
        
        for line in result:
            text = line[1][0]
            # Try to extract item name and quantity
            match = re.search(r'([\w\s]+)\s*(\d+)', text)
            if match:
                item_name = match.group(1).strip()
                quantity = int(match.group(2))
                items.append({
                    'name': item_name,
                    'quantity': quantity
                })
        
        return items

# Singleton instance
ocr_processor = OCRProcessor()

def process_image(image_path):
    return ocr_processor.process_image(image_path)
