import unittest
from unittest.mock import patch, MagicMock, call
from corrector.gemini_corrector import GeminiCorrector
import logging

class TestGeminiCorrector(unittest.TestCase):
    def setUp(self):
        # Mock OCR result with bounding boxes
        self.mock_ocr_result = [
            # First row (item names)
            [
                [[10, 20], [100, 20], [100, 40], [10, 40]],
                ["milk", 0.95]
            ],
            [
                [[120, 20], [210, 20], [210, 40], [120, 40]],
                ["eggs", 0.92]
            ],
            # Second row (quantities)
            [
                [[10, 50], [100, 50], [100, 70], [10, 70]],
                ["2", 0.85]
            ],
            [
                [[120, 50], [210, 50], [210, 70], [120, 70]],
                ["12", 0.88]
            ]
        ]

    def test_parse_ocr_result_with_gemini(self):
        """Test successful parsing of OCR results"""
        # Initialize corrector
        corrector = GeminiCorrector()
        
        # Mock the client's models
        mock_client = MagicMock()
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '[{"name": "milk", "quantity": 2}, {"name": "eggs", "quantity": 12}]'
        mock_model.generate_content.return_value = mock_response
        mock_client.models = mock_model
        corrector.client = mock_client
        mock_logger = MagicMock()
        corrector.logger = mock_logger

        # Call the function
        result = corrector.parse_ocr_result_with_gemini(self.mock_ocr_result)

        # Verify the result
        expected_result = [
            {'name': 'milk', 'quantity': 2},
            {'name': 'eggs', 'quantity': 12}
        ]
        self.assertEqual(result, expected_result)

        # Verify logging calls
        mock_logger.info.assert_has_calls([
            call(f"Structured text:\nmilk\teggs\n2\t12"),
            call('Calling Gemini API with text:\nmilk\teggs\n2\t12'),
            call("Gemini response:\n[{\"name\": \"milk\", \"quantity\": 2}, {\"name\": \"eggs\", \"quantity\": 12}]")
        ])

        # Verify Gemini was called with the correct prompt
        mock_model.generate_content.assert_called_once()
        call_args = mock_model.generate_content.call_args[1]['contents']
        self.assertIn("milk\teggs", call_args)
        self.assertIn("2\t12", call_args)

    def test_parse_ocr_result_with_gemini_empty(self):
        """Test empty OCR result handling"""
        # Mock OCR result with empty text
        mock_ocr_result = [
            [[10, 20], [100, 20], [100, 40], [10, 40]],
            ["", 0.95]
        ]

        # Mock the client's models
        mock_client = MagicMock()
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '[]'
        mock_model.generate_content.return_value = mock_response
        mock_client.models = mock_model
        corrector = GeminiCorrector()
        corrector.client = mock_client

        mock_logger = MagicMock()
        corrector.logger = mock_logger
        
        # Call the function
        result = corrector.parse_ocr_result_with_gemini(mock_ocr_result)

        # Verify empty result
        self.assertEqual(result, [])

    def test_parse_ocr_result_with_gemini_error(self):
        """Test error handling when Gemini API fails"""
        # Mock OCR result
        mock_ocr_result = [
            [[10, 20], [100, 20], [100, 40], [10, 40]],
            ["milk", 0.95]
        ]

        # Mock the client's models
        mock_client = MagicMock()
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_client.models = mock_model
        corrector = GeminiCorrector()
        corrector.client = mock_client
        mock_logger = MagicMock()
        corrector.logger = mock_logger
        
        # Call the function
        result = corrector.parse_ocr_result_with_gemini(mock_ocr_result)

        # Verify empty result on error
        self.assertEqual(result, [])

        # Verify logging
        mock_logger.error.assert_called_once()

    def test_parse_ocr_result_with_gemini_malformed_json(self):
        """Test handling of malformed JSON response"""
        # Mock OCR result
        mock_ocr_result = [
            [[10, 20], [100, 20], [100, 40], [10, 40]],
            ["milk", 0.95]
        ]

        # Mock the client's models
        mock_client = MagicMock()
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '[{"name": "milk", "quantity": 2}]'  # Missing closing bracket
        mock_model.generate_content.return_value = mock_response
        mock_client.models = mock_model
        corrector = GeminiCorrector()
        corrector.client = mock_client
        mock_logger = MagicMock()
        corrector.logger = mock_logger
        
        # Call the function
        result = corrector.parse_ocr_result_with_gemini(mock_ocr_result)

        # Verify empty result on malformed JSON
        self.assertEqual(result, [])

        # Verify logging
        mock_logger.error.assert_called_once()

if __name__ == '__main__':
    unittest.main()
