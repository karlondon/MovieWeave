"""
Feature 4: Camera Effects
Apply professional camera effects to videos
"""

from PIL import Image


class CameraEffects:
    """Apply camera effects to video frames"""
    
    @staticmethod
    def apply_zoom(frame, zoom_level: float = 1.5):
        """Apply zoom effect to frame"""
        width, height = frame.size
        new_width = int(width / zoom_level)
        new_height = int(height / zoom_level)
        
        left = (width - new_width) // 2
        top = (height - new_height) // 2
        cropped = frame.crop((left, top, left + new_width, top + new_height))
        
        return cropped.resize((width, height), Image.Resampling.LANCZOS)
    
    @staticmethod
    def apply_pan(frame, pan_amount: float = 0.1):
        """Apply pan (horizontal shift) effect"""
        width, height = frame.size
        offset = int(width * pan_amount)
        
        pixels = frame.load()
        new_frame = Image.new('RGB', (width, height), (255, 255, 255))
        new_pixels = new_frame.load()
        
        for y in range(height):
            for x in range(width):
                src_x = (x + offset) % width
                new_pixels[x, y] = pixels[src_x, y]
        
        return new_frame
    
    @staticmethod
    def apply_fade(frame, fade_progress: float):
        """Apply fade effect (0.0 transparent to 1.0 opaque)"""
        frame_copy = frame.copy()
        alpha = int(255 * fade_progress)
        frame_copy.putalpha(alpha)
        return frame_copy
    
    @staticmethod
    def apply_rotate(frame, angle: float = 5.0):
        """Apply rotation effect"""
        return frame.rotate(angle, expand=False, resample=Image.Resampling.BICUBIC)
