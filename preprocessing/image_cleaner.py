import cv2
import numpy as np
from PIL import Image
import os

class ImageCleaner:
    def __init__(self, max_width=1000):
        """
        Initialize the image cleaner with maximum width for resizing
        Args:
            max_width (int): Maximum width for resized images
        """
        self.max_width = max_width

    def load_image(self, image):
        """
        Load image from either PIL Image or file path
        Args:
            image: PIL Image object or file path
        Returns:
            np.ndarray: OpenCV image (NumPy array)
        """
        if isinstance(image, str):
            # Load from file path
            return cv2.imread(image)
        elif isinstance(image, Image.Image):
            # Convert PIL Image to OpenCV format
            return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        else:
            raise ValueError("Input must be either a file path or PIL Image")

    def grayscale(self, image):
        """
        Convert image to grayscale
        Args:
            image: OpenCV image (NumPy array)
        Returns:
            np.ndarray: Grayscale image
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def resize_image(self, image):
        """
        Resize image while maintaining aspect ratio
        Args:
            image: OpenCV image (NumPy array)
        Returns:
            np.ndarray: Resized image
        """
        height, width = image.shape[:2]
        if width > self.max_width:
            ratio = self.max_width / width
            new_height = int(height * ratio)
            image = cv2.resize(image, (self.max_width, new_height))
        return image

    def apply_blur(self, image, kernel_size=(5, 5)):
        """
        Apply Gaussian blur to reduce noise
        Args:
            image: OpenCV image (NumPy array)
            kernel_size: Size of the Gaussian kernel
        Returns:
            np.ndarray: Blurred image
        """
        return cv2.GaussianBlur(image, kernel_size, 0)

    def process_image(self, image, save_intermediate=False, output_dir='debug'):
        """
        Process image through the entire pipeline
        Args:
            image: PIL Image object or file path
            save_intermediate: Whether to save intermediate steps
            output_dir: Directory to save intermediate images
        Returns:
            np.ndarray: Cleaned image
        """
        # Create output directory if saving intermediate steps
        if save_intermediate:
            os.makedirs(output_dir, exist_ok=True)

        # Load image
        img = self.load_image(image)
        if save_intermediate:
            cv2.imwrite(os.path.join(output_dir, '01_original.jpg'), img)

        # Convert to grayscale
        img = self.grayscale(img)
        if save_intermediate:
            cv2.imwrite(os.path.join(output_dir, '02_grayscale.jpg'), img)

        # Resize image
        img = self.resize_image(img)
        if save_intermediate:
            cv2.imwrite(os.path.join(output_dir, '03_resized.jpg'), img)

        # Apply blur
        img = self.apply_blur(img)
        if save_intermediate:
            cv2.imwrite(os.path.join(output_dir, '04_blurred.jpg'), img)

        return img

    def test_pipeline(self, image_paths, output_dir='test_output'):
        """
        Test the image processing pipeline with sample images
        Args:
            image_paths: List of image file paths to test
            output_dir: Directory to save processed images
        """
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"Testing image processing pipeline with {len(image_paths)} images...")
        
        for i, image_path in enumerate(image_paths, 1):
            print(f"\nProcessing image {i}: {image_path}")
            try:
                # Process image with intermediate steps saved
                result = self.process_image(
                    image_path,
                    save_intermediate=True,
                    output_dir=os.path.join(output_dir, f'image_{i}')
                )
                print("Processing complete!")
            except Exception as e:
                print(f"Error processing image: {str(e)}")

# Example usage
def main():
    # Create cleaner instance
    cleaner = ImageCleaner()
    
    # Test with sample images
    test_images = [
        'path/to/sample1.jpg',
        'path/to/sample2.jpg'
    ]
    
    cleaner.test_pipeline(test_images)

if __name__ == '__main__':
    main()
