#!/usr/bin/env python3
"""
🖼️ BAARLICLAW IMAGE TOOLKIT
Bildebehandling og generering
"""

import os
import sys
import subprocess
from typing import Optional, Tuple, List
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import requests
from io import BytesIO
import base64

# Legg til toolkit i path
sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging, validate_url

logger = setup_logging("ImageToolkit")

class ImageProcessor:
    """Handle all image operations"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
        
    def load_image(self, source: str) -> Optional[Image.Image]:
        """
        Load image from file path or URL
        
        Args:
            source: File path or URL
        """
        try:
            if validate_url(source):
                # Load from URL
                response = requests.get(source, timeout=30)
                response.raise_for_status()
                return Image.open(BytesIO(response.content))
            else:
                # Load from file
                if os.path.exists(source):
                    return Image.open(source)
                else:
                    logger.error(f"File not found: {source}")
                    return None
        except Exception as e:
            logger.error(f"Failed to load image: {e}")
            return None
    
    def save_image(self, image: Image.Image, output_path: str, 
                   quality: int = 95) -> bool:
        """Save image to file"""
        try:
            # Convert RGBA to RGB if saving as JPEG
            if output_path.lower().endswith(('.jpg', '.jpeg')) and image.mode == 'RGBA':
                image = image.convert('RGB')
            
            image.save(output_path, quality=quality)
            logger.info(f"Saved: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save image: {e}")
            return False
    
    def resize(self, image: Image.Image, width: Optional[int] = None,
               height: Optional[int] = None, maintain_aspect: bool = True) -> Image.Image:
        """
        Resize image
        
        Args:
            image: PIL Image
            width: New width (optional)
            height: New height (optional)
            maintain_aspect: Keep aspect ratio
        """
        if maintain_aspect and (width or height):
            orig_width, orig_height = image.size
            
            if width and not height:
                ratio = width / orig_width
                height = int(orig_height * ratio)
            elif height and not width:
                ratio = height / orig_height
                width = int(orig_width * ratio)
            elif width and height:
                # Use the dimension that results in smaller image
                ratio_w = width / orig_width
                ratio_h = height / orig_height
                ratio = min(ratio_w, ratio_h)
                width = int(orig_width * ratio)
                height = int(orig_height * ratio)
        
        return image.resize((width, height), Image.Resampling.LANCZOS)
    
    def crop(self, image: Image.Image, box: Tuple[int, int, int, int]) -> Image.Image:
        """
        Crop image
        
        Args:
            image: PIL Image
            box: (left, top, right, bottom)
        """
        return image.crop(box)
    
    def crop_to_aspect(self, image: Image.Image, aspect_ratio: float) -> Image.Image:
        """
        Crop image to specific aspect ratio (width/height)
        
        Common ratios:
        - 16/9 = 1.78 (YouTube thumbnail)
        - 1/1 = 1.0 (Square)
        - 9/16 = 0.56 (Instagram Story)
        - 4/3 = 1.33 (Standard photo)
        """
        width, height = image.size
        current_ratio = width / height
        
        if current_ratio > aspect_ratio:
            # Image is too wide, crop width
            new_width = int(height * aspect_ratio)
            left = (width - new_width) // 2
            return image.crop((left, 0, left + new_width, height))
        else:
            # Image is too tall, crop height
            new_height = int(width / aspect_ratio)
            top = (height - new_height) // 2
            return image.crop((0, top, width, top + new_height))
    
    def add_text(self, image: Image.Image, text: str, 
                 position: Tuple[int, int] = (10, 10),
                 font_size: int = 40,
                 color: Tuple[int, int, int] = (255, 255, 255),
                 stroke_color: Optional[Tuple[int, int, int]] = (0, 0, 0),
                 stroke_width: int = 2) -> Image.Image:
        """Add text to image"""
        draw = ImageDraw.Draw(image)
        
        # Try to load a font, fallback to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Draw text with stroke for readability
        if stroke_color:
            # Draw stroke
            for dx in range(-stroke_width, stroke_width + 1):
                for dy in range(-stroke_width, stroke_width + 1):
                    if dx != 0 or dy != 0:
                        draw.text((position[0] + dx, position[1] + dy), 
                                 text, font=font, fill=stroke_color)
        
        # Draw main text
        draw.text(position, text, font=font, fill=color)
        
        return image
    
    def create_thumbnail(self, image: Image.Image, 
                        size: Tuple[int, int] = (1280, 720),
                        text: Optional[str] = None) -> Image.Image:
        """
        Create YouTube-style thumbnail
        
        Args:
            image: Source image
            size: Output size (default 1280x720)
            text: Optional text overlay
        """
        # Crop to 16:9 aspect ratio
        img = self.crop_to_aspect(image, 16/9)
        
        # Resize to target
        img = self.resize(img, size[0], size[1], maintain_aspect=False)
        
        # Add text if provided
        if text:
            # Calculate position (centered horizontally, near bottom)
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            # Get text size
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            
            x = (size[0] - text_width) // 2
            y = size[1] - 150
            
            img = self.add_text(img, text, (x, y), font_size=60, 
                               color=(255, 255, 0), stroke_color=(0, 0, 0), stroke_width=3)
        
        return img
    
    def apply_filter(self, image: Image.Image, filter_type: str) -> Image.Image:
        """
        Apply filter to image
        
        Filters: blur, sharpen, contour, emboss, brightness, contrast
        """
        if filter_type == 'blur':
            return image.filter(ImageFilter.GaussianBlur(radius=2))
        elif filter_type == 'sharpen':
            return image.filter(ImageFilter.SHARPEN)
        elif filter_type == 'contour':
            return image.filter(ImageFilter.CONTOUR)
        elif filter_type == 'emboss':
            return image.filter(ImageFilter.EMBOSS)
        elif filter_type == 'brightness':
            enhancer = ImageEnhance.Brightness(image)
            return enhancer.enhance(1.2)
        elif filter_type == 'contrast':
            enhancer = ImageEnhance.Contrast(image)
            return enhancer.enhance(1.3)
        else:
            return image
    
    def create_collage(self, images: List[Image.Image], 
                      layout: str = 'grid') -> Image.Image:
        """
        Create collage from multiple images
        
        Layouts: grid (2x2), horizontal, vertical
        """
        if not images:
            return None
        
        if layout == 'grid' and len(images) >= 4:
            # 2x2 grid
            width = max(images[0].width, images[1].width)
            height = max(images[0].height, images[2].height)
            
            collage = Image.new('RGB', (width * 2, height * 2))
            
            for i, img in enumerate(images[:4]):
                x = (i % 2) * width
                y = (i // 2) * height
                collage.paste(img.resize((width, height)), (x, y))
            
            return collage
        
        elif layout == 'horizontal':
            total_width = sum(img.width for img in images)
            max_height = max(img.height for img in images)
            
            collage = Image.new('RGB', (total_width, max_height))
            x_offset = 0
            for img in images:
                collage.paste(img, (x_offset, 0))
                x_offset += img.width
            
            return collage
        
        elif layout == 'vertical':
            max_width = max(img.width for img in images)
            total_height = sum(img.height for img in images)
            
            collage = Image.new('RGB', (max_width, total_height))
            y_offset = 0
            for img in images:
                collage.paste(img, (0, y_offset))
                y_offset += img.height
            
            return collage
        
        return images[0]

class ImageGenerator:
    """Generate images using AI services"""
    
    def __init__(self, openai_key: Optional[str] = None):
        self.openai_key = openai_key or os.environ.get('OPENAI_API_KEY')
        
    def generate_with_dalle(self, prompt: str, size: str = "1024x1024") -> Optional[str]:
        """
        Generate image with DALL-E
        
        Returns URL of generated image
        """
        if not self.openai_key:
            logger.error("No OpenAI API key provided")
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.openai_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'dall-e-3',
                'prompt': prompt,
                'size': size,
                'n': 1
            }
            
            response = requests.post(
                'https://api.openai.com/v1/images/generations',
                headers=headers,
                json=data,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result['data'][0]['url']
            
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return None

# === CONVENIENCE FUNCTIONS ===
def quick_resize(input_path: str, output_path: str, 
                 width: Optional[int] = None, height: Optional[int] = None) -> bool:
    """Quick resize function"""
    processor = ImageProcessor()
    img = processor.load_image(input_path)
    if img:
        resized = processor.resize(img, width, height)
        return processor.save_image(resized, output_path)
    return False

def quick_thumbnail(input_path: str, output_path: str, 
                   text: Optional[str] = None) -> bool:
    """Quick thumbnail creation"""
    processor = ImageProcessor()
    img = processor.load_image(input_path)
    if img:
        thumb = processor.create_thumbnail(img, text=text)
        return processor.save_image(thumb, output_path)
    return False

def download_image(url: str, output_path: str) -> bool:
    """Download image from URL"""
    processor = ImageProcessor()
    img = processor.load_image(url)
    if img:
        return processor.save_image(img, output_path)
    return False

# === TESTING ===
if __name__ == "__main__":
    print("🖼️ BaarliClaw Image Toolkit - Testing")
    print("=" * 50)
    
    processor = ImageProcessor()
    
    # Test with a sample image if available
    test_images = [
        "/tmp/test_image.jpg",
        "/root/.openclaw/workspace/assets/test.png"
    ]
    
    found_image = None
    for img_path in test_images:
        if os.path.exists(img_path):
            found_image = img_path
            break
    
    if found_image:
        print(f"Testing with: {found_image}")
        img = processor.load_image(found_image)
        if img:
            print(f"✅ Loaded: {img.size}")
            
            # Test resize
            resized = processor.resize(img, width=300)
            print(f"✅ Resized: {resized.size}")
            
            # Test crop to aspect
            cropped = processor.crop_to_aspect(img, 16/9)
            print(f"✅ Cropped to 16:9: {cropped.size}")
    else:
        print("ℹ️ No test image found, skipping image tests")
    
    # Test URL validation
    print(f"✅ URL validation works: {validate_url('https://example.com/image.jpg')}")
    
    print("\n✅ Image Toolkit ready!")
