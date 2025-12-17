"""
🖼️ Image Processing Service

تحقق و پردازش تصاویر برای تحلیل
"""

import io
from PIL import Image
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class ImageProcessingService:
    """سرویس پردازش و تحقق تصاویر"""
    
    # تنظیمات
    MAX_IMAGE_SIZE_MB = 5
    MIN_IMAGE_WIDTH = 480
    MIN_IMAGE_HEIGHT = 480
    MAX_IMAGE_WIDTH = 4096
    MAX_IMAGE_HEIGHT = 4096
    ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}
    
    def validate_image(self, image_data: bytes) -> Tuple[bool, str]:
        """
        تحقق عکس
        
        Returns:
            (is_valid, error_message)
        """
        try:
            # Size check
            size_mb = len(image_data) / (1024 * 1024)
            if size_mb > self.MAX_IMAGE_SIZE_MB:
                return False, f"Image too large: {size_mb:.1f}MB (max {self.MAX_IMAGE_SIZE_MB}MB)"
            
            # Open image
            image = Image.open(io.BytesIO(image_data))
            
            # Format check
            if image.format not in self.ALLOWED_FORMATS:
                return False, f"Invalid format: {image.format}. Allowed: {self.ALLOWED_FORMATS}"
            
            # Dimension check
            width, height = image.size
            if width < self.MIN_IMAGE_WIDTH or height < self.MIN_IMAGE_HEIGHT:
                return False, f"Image too small: {width}x{height}. Min: {self.MIN_IMAGE_WIDTH}x{self.MIN_IMAGE_HEIGHT}"
            
            if width > self.MAX_IMAGE_WIDTH or height > self.MAX_IMAGE_HEIGHT:
                return False, f"Image too large: {width}x{height}. Max: {self.MAX_IMAGE_WIDTH}x{self.MAX_IMAGE_HEIGHT}"
            
            logger.info(f"✅ Image valid: {width}x{height}, {size_mb:.1f}MB, format: {image.format}")
            return True, ""
            
        except Exception as e:
            logger.error(f"❌ Image validation error: {str(e)}")
            return False, f"Invalid image: {str(e)}"
    
    def resize_image(self, image_data: bytes, max_width: int = 1024) -> bytes:
        """
        تغییر اندازه عکس برای بهتری
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            
            if image.width > max_width:
                ratio = max_width / image.width
                new_height = int(image.height * ratio)
                image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Save as JPEG
                output = io.BytesIO()
                image.save(output, format="JPEG", quality=85)
                logger.info(f"✅ Image resized to {image.width}x{image.height}")
                return output.getvalue()
            
            return image_data
            
        except Exception as e:
            logger.error(f"❌ Resize error: {str(e)}")
            return image_data
    
    def convert_to_rgb(self, image_data: bytes) -> bytes:
        """
        تبدیل عکس به RGB
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            
            if image.mode != "RGB":
                image = image.convert("RGB")
                
                output = io.BytesIO()
                image.save(output, format="JPEG", quality=90)
                logger.info(f"✅ Image converted to RGB")
                return output.getvalue()
            
            return image_data
            
        except Exception as e:
            logger.error(f"❌ Conversion error: {str(e)}")
            return image_data
    
    def process_image(self, image_data: bytes) -> bytes:
        """
        پردازش کامل عکس
        """
        try:
            # Validate
            is_valid, error = self.validate_image(image_data)
            if not is_valid:
                raise Exception(error)
            
            # Convert to RGB
            processed = self.convert_to_rgb(image_data)
            
            # Resize if needed
            processed = self.resize_image(processed)
            
            logger.info("✅ Image processed successfully")
            return processed
            
        except Exception as e:
            logger.error(f"❌ Processing error: {str(e)}")
            raise
    
    def get_image_info(self, image_data: bytes) -> dict:
        """
        دریافت اطلاعات تصویر
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            
            return {
                "format": image.format,
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
                "size_bytes": len(image_data),
                "size_mb": len(image_data) / (1024 * 1024),
            }
            
        except Exception as e:
            logger.error(f"❌ Info error: {str(e)}")
            return {}
