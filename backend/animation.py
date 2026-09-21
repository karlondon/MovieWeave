"""
Stick figure animation module for creating MP4 videos with animated characters
"""
import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeVideoClip
import random

logger = logging.getLogger(__name__)

# Video settings
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
FPS = 24
BG_COLOR = (30, 30, 50)  # Dark blue-gray background


class StickFigure:
    """Draw and animate stick figure characters"""
    
    def __init__(self, character_type='male'):
        """character_type: 'male', 'female', 'animal' (dog/cat, etc)"""
        self.character_type = character_type
        self.x = VIDEO_WIDTH // 2
        self.y = VIDEO_HEIGHT // 2
        
    def draw(self, image: Image.Image, frame: int, animation_state: str = 'idle'):
        """Draw stick figure on image at specific frame"""
        draw = ImageDraw.Draw(image)
        
        if self.character_type == 'male':
            self._draw_male(draw, self.x, self.y, frame, animation_state)
        elif self.character_type == 'female':
            self._draw_female(draw, self.x, self.y, frame, animation_state)
        elif self.character_type == 'animal':
            self._draw_animal(draw, self.x, self.y, frame, animation_state)
        
        return image
    
    def _draw_male(self, draw, cx, cy, frame, state):
        """Draw male stick figure with animation"""
        head_radius = 30
        body_length = 50
        arm_length = 40
        leg_length = 50
        
        # Head
        draw.ellipse(
            [cx - head_radius, cy - head_radius, cx + head_radius, cy + head_radius],
            outline=(200, 180, 150),
            width=3
        )
        
        # Eyes and mouth
        eye_offset = 12
        draw.ellipse([cx - eye_offset - 5, cy - 10, cx - eye_offset + 5, cy], 
                    fill=(0, 0, 0))
        draw.ellipse([cx + eye_offset - 5, cy - 10, cx + eye_offset + 5, cy], 
                    fill=(0, 0, 0))
        draw.arc([cx - 10, cy + 5, cx + 10, cy + 20], 0, 180, fill=(0, 0, 0), width=2)
        
        # Body
        body_top = cy + head_radius
        body_bottom = body_top + body_length
        draw.line([cx, body_top, cx, body_bottom], fill=(100, 150, 255), width=3)
        
        # Arms with animation
        if state == 'talking':
            arm_angle = 25 + (frame % 10) * 3
        else:
            arm_angle = 20
        
        arm_left_x = cx - arm_length * (arm_angle / 90)
        arm_right_x = cx + arm_length * (arm_angle / 90)
        arm_y = body_top + 15
        
        draw.line([cx, arm_y, arm_left_x, arm_y - 10], fill=(200, 180, 150), width=2)
        draw.line([cx, arm_y, arm_right_x, arm_y - 10], fill=(200, 180, 150), width=2)
        
        # Legs
    
    def _draw_female(self, draw, cx, cy, frame, state):
        """Draw female stick figure with animation"""
        head_radius = 30
        body_length = 55
        arm_length = 38
        leg_length = 50
        
        # Head
        draw.ellipse(
            [cx - head_radius, cy - head_radius, cx + head_radius, cy + head_radius],
            outline=(220, 190, 160),
            width=3
        )
        
        # Eyes and smile
        eye_offset = 12
        draw.ellipse([cx - eye_offset - 5, cy - 10, cx - eye_offset + 5, cy], 
                    fill=(0, 0, 0))
        draw.ellipse([cx + eye_offset - 5, cy - 10, cx + eye_offset + 5, cy], 
                    fill=(0, 0, 0))
        draw.arc([cx - 12, cy + 3, cx + 12, cy + 18], 0, 180, fill=(0, 0, 0), width=2)
        
        # Hair (triangle on top)
        draw.polygon([cx - 35, cy - 32, cx + 35, cy - 32, cx, cy - 55], 
                    fill=(100, 50, 50), outline=(100, 50, 50))
        
        # Body (dress-like)
        body_top = cy + head_radius
        body_bottom = body_top + body_length
        draw.line([cx, body_top, cx, body_bottom], fill=(255, 100, 150), width=4)
        
        # Arms with animation
        if state == 'talking':
            arm_angle = 30 + (frame % 8) * 4
        else:
            arm_angle = 25
        
        arm_left_x = cx - arm_length * (arm_angle / 90)
        arm_right_x = cx + arm_length * (arm_angle / 90)
        arm_y = body_top + 12
        
        draw.line([cx, arm_y, arm_left_x, arm_y - 12], fill=(220, 190, 160), width=2)
        draw.line([cx, arm_y, arm_right_x, arm_y - 12], fill=(220, 190, 160), width=2)
        
        # Legs
        draw.line([cx, body_bottom, cx - 12, body_bottom + leg_length], 
                 fill=(50, 50, 100), width=2)
        draw.line([cx, body_bottom, cx + 12, body_bottom + leg_length], 
                 fill=(50, 50, 100), width=2)
    
    def _draw_animal(self, draw, cx, cy, frame, state):
        """Draw simple animal (dog/cat) stick figure"""
        # Head circle
        head_radius = 35
        draw.ellipse(
            [cx - head_radius, cy - head_radius, cx + head_radius, cy + head_radius],
            outline=(180, 120, 80),
            width=3
        )
        
        # Ears (triangles)
        ear_offset = 25
        draw.polygon([cx - ear_offset - 15, cy - head_radius, 
                     cx - ear_offset - 5, cy - head_radius - 25,
                     cx - ear_offset + 5, cy - head_radius], 
                    outline=(180, 120, 80), fill=(180, 120, 80))
        draw.polygon([cx + ear_offset - 5, cy - head_radius,
                     cx + ear_offset + 5, cy - head_radius - 25,
                     cx + ear_offset + 15, cy - head_radius], 
                    outline=(180, 120, 80), fill=(180, 120, 80))
        
        # Eyes
        draw.ellipse([cx - 12, cy - 15, cx - 5, cy - 8], fill=(0, 0, 0))
        draw.ellipse([cx + 5, cy - 15, cx + 12, cy - 8], fill=(0, 0, 0))
        
        # Snout
        draw.ellipse([cx - 15, cy + 10, cx + 15, cy + 30], 
                    outline=(180, 120, 80), width=2)
        
        # Body
        body_top = cy + head_radius
        body_bottom = body_top + 50
        body_width = 40
        draw.ellipse([cx - body_width, body_top, cx + body_width, body_bottom],
                    outline=(180, 120, 80), width=3)
        
        # Tail with animation
        tail_angle = 20 + (frame % 12) * 3
        tail_end_x = cx + body_width + 30 * (tail_angle / 90)
        tail_end_y = body_top + 20
        draw.line([cx + body_width, body_top + 20, tail_end_x, tail_end_y],
                 fill=(180, 120, 80), width=3)
        
        # Legs
        leg_y_bottom = body_bottom + 40
        draw.line([cx - 20, body_bottom, cx - 20, leg_y_bottom], 
                 fill=(180, 120, 80), width=2)
        draw.line([cx + 20, body_bottom, cx + 20, leg_y_bottom], 
                 fill=(180, 120, 80), width=2)


def create_frame(text: str, frame: int, character: StickFigure) -> Image.Image:
    """Create a single frame with background, character, and text"""
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Draw character
    character.draw(img, frame, animation_state='talking')
    
    # Draw subtitle text at bottom
    if text:
        # Draw semi-transparent background for text
        text_y = VIDEO_HEIGHT - 120
        draw.rectangle(
            [20, text_y - 10, VIDEO_WIDTH - 20, VIDEO_HEIGHT - 20],
            fill=(0, 0, 0),
            outline=(100, 150, 255),
            width=2
        )
        
        # Draw text with word wrapping
        font_size = 32
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Simple word wrap
        words = text.split()
        lines = []
        current_line = []
        max_width = VIDEO_WIDTH - 60
        
        for word in words:
            current_line.append(word)
            line_text = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), line_text, font=font)
            line_width = bbox[2] - bbox[0]
            
            if line_width > max_width and len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        
        lines.append(' '.join(current_line))
        
        # Draw text lines
        text_x = 40
        text_y = VIDEO_HEIGHT - 100
        for line in lines[-2:]:  # Show last 2 lines max
            draw.text((text_x, text_y), line, fill=(255, 255, 255), font=font)
            text_y += 40
    
    return img


def split_text_into_chunks(text: str, chunk_duration: float = 2.0) -> list:
    """Split text into chunks for subtitle timing"""
    words = text.split()
    if not words:
        return []
    
    # Estimate: ~150 words per minute = 2.5 words per second
    words_per_chunk = max(1, int(2.5 * chunk_duration))
    chunks = []
    
    for i in range(0, len(words), words_per_chunk):
        chunk = ' '.join(words[i:i + words_per_chunk])
        chunks.append(chunk)
    
    return chunks



def create_animated_video(
    audio_path: Path,
    text_content: str,
    output_path: Path,
    character_type: str = 'male',
    progress_callback=None
) -> bool:
    """
    Create MP4 video with animated stick figure and subtitles
    
    Args:
        audio_path: Path to MP3 audio file
        text_content: Text to display as subtitles
        output_path: Where to save the MP4
        character_type: 'male', 'female', or 'animal'
        progress_callback: Function to call with progress (0-100)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"🎬 Starting video generation with {character_type} character")
        
        # Load audio
        if progress_callback:
            progress_callback(5)
        
        audio = AudioFileClip(str(audio_path))
        duration = audio.duration
        logger.info(f"⏱️ Audio duration: {duration:.1f} seconds")
        
        # Create character
        character = StickFigure(character_type)
        
        # Split text into chunks for subtitle timing
        text_chunks = split_text_into_chunks(text_content, chunk_duration=2.0)
        
        if not text_chunks:
            text_chunks = [text_content[:100]]
        
        logger.info(f"📝 Split text into {len(text_chunks)} subtitle chunks")
        
        # Generate frames
        if progress_callback:
            progress_callback(10)
        
        num_frames = int(duration * FPS)
        frames = []
        
        # Calculate which text chunk for each frame
        chunk_duration_frames = num_frames / len(text_chunks) if text_chunks else 1
        
        logger.info(f"🖼️ Generating {num_frames} frames at {FPS} FPS...")
        
        for frame_idx in range(num_frames):
            # Determine which text chunk to show
            chunk_idx = min(int(frame_idx / chunk_duration_frames), len(text_chunks) - 1)
            current_text = text_chunks[chunk_idx]
            
            # Create frame
            frame = create_frame(current_text, frame_idx, character)
            frames.append(frame)
            
            # Update progress
            if progress_callback and frame_idx % 30 == 0:  # Update every 30 frames
                progress = 10 + (frame_idx / num_frames) * 50
                progress_callback(int(progress))
        
        logger.info(f"✅ Generated {len(frames)} frames")
        
        # Create video clip from frames
        if progress_callback:
            progress_callback(65)
        
        logger.info("🎥 Creating video clip from frames...")
        video = ImageSequenceClip(frames, fps=FPS)
        
        # Set audio
        if progress_callback:
            progress_callback(75)
        
        logger.info("🔊 Adding audio to video...")
        video_with_audio = video.set_audio(audio)
        
        # Write to file
        if progress_callback:
            progress_callback(85)
        
        logger.info(f"💾 Writing MP4 to {output_path}...")
        video_with_audio.write_videofile(
            str(output_path),
            fps=FPS,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None  # Suppress moviepy logs
        )
        
        # Close
        video.close()
        audio.close()
        video_with_audio.close()
        
        if progress_callback:
            progress_callback(95)
        
        logger.info(f"✅ Video generation complete: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Video generation failed: {e}", exc_info=True)
        return False


