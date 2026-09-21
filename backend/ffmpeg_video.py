"""Fast MP4 video generation using FFmpeg directly instead of MoviePy"""
import logging
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import shutil

logger = logging.getLogger(__name__)

VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
FPS = 24
BG_COLOR = (30, 30, 50)


class StickFigureFFmpeg:
    """Draw stick figure characters"""
    
    def __init__(self, character_type='male'):
        self.character_type = character_type
        self.x = VIDEO_WIDTH // 2
        self.y = VIDEO_HEIGHT // 2
    
    def draw(self, image, frame, animation_state='idle'):
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
        head_radius, body_length, arm_length = 30, 50, 40
        draw.ellipse([cx - head_radius, cy - head_radius, cx + head_radius, cy + head_radius],
                    outline=(200, 180, 150), width=3)
        eye_offset = 12
        draw.ellipse([cx - eye_offset - 5, cy - 10, cx - eye_offset + 5, cy], fill=(0, 0, 0))
        draw.ellipse([cx + eye_offset - 5, cy - 10, cx + eye_offset + 5, cy], fill=(0, 0, 0))
        draw.arc([cx - 10, cy + 5, cx + 10, cy + 20], 0, 180, fill=(0, 0, 0), width=2)
        body_top = cy + head_radius
        body_bottom = body_top + body_length
        draw.line([cx, body_top, cx, body_bottom], fill=(100, 150, 255), width=3)
        arm_angle = 25 + (frame % 10) * 3 if state == 'talking' else 20
        arm_left_x = cx - arm_length * (arm_angle / 90)
        arm_right_x = cx + arm_length * (arm_angle / 90)
        arm_y = body_top + 15
        draw.line([cx, arm_y, arm_left_x, arm_y - 10], fill=(200, 180, 150), width=2)
        draw.line([cx, arm_y, arm_right_x, arm_y - 10], fill=(200, 180, 150), width=2)
        draw.line([cx, body_bottom, cx - 15, body_bottom + 40], fill=(50, 50, 100), width=2)
        draw.line([cx, body_bottom, cx + 15, body_bottom + 40], fill=(50, 50, 100), width=2)
    
    def _draw_female(self, draw, cx, cy, frame, state):
        """Draw female stick figure"""
        head_radius, body_length, arm_length = 30, 55, 38
        draw.ellipse([cx - head_radius, cy - head_radius, cx + head_radius, cy + head_radius],
                    outline=(220, 190, 160), width=3)
        draw.arc([cx - head_radius, cy - head_radius - 10, cx + head_radius, cy - head_radius + 10],
                0, 180, fill=(150, 100, 80), width=4)
        eye_offset = 12
        draw.ellipse([cx - eye_offset - 5, cy - 10, cx - eye_offset + 5, cy], fill=(0, 0, 0))
        draw.ellipse([cx + eye_offset - 5, cy - 10, cx + eye_offset + 5, cy], fill=(0, 0, 0))
        draw.arc([cx - 10, cy + 5, cx + 10, cy + 20], 0, 180, fill=(0, 0, 0), width=2)
        body_top = cy + head_radius
        body_bottom = body_top + body_length
        draw.line([cx, body_top, cx, body_bottom], fill=(255, 100, 150), width=3)
        arm_angle = 25 + (frame % 10) * 3 if state == 'talking' else 20
        arm_left_x = cx - arm_length * (arm_angle / 90)
        arm_right_x = cx + arm_length * (arm_angle / 90)
        arm_y = body_top + 15
        draw.line([cx, arm_y, arm_left_x, arm_y - 10], fill=(220, 190, 160), width=2)
        draw.line([cx, arm_y, arm_right_x, arm_y - 10], fill=(220, 190, 160), width=2)
        draw.line([cx - 10, body_bottom, cx - 15, body_bottom + 40], fill=(150, 100, 80), width=2)
        draw.line([cx + 10, body_bottom, cx + 15, body_bottom + 40], fill=(150, 100, 80), width=2)
    
    def _draw_animal(self, draw, cx, cy, frame, state):
        """Draw animal character"""
        body_radius = 35
        draw.ellipse([cx - body_radius, cy - 20, cx + body_radius, cy + 40],
                    outline=(200, 150, 100), width=3, fill=(255, 200, 100))
        draw.polygon([cx - 25, cy - 25, cx - 15, cy - 50, cx - 10, cy - 20], fill=(200, 150, 100))
        draw.polygon([cx + 25, cy - 25, cx + 15, cy - 50, cx + 10, cy - 20], fill=(200, 150, 100))
        draw.ellipse([cx - 15, cy, cx - 5, cy + 10], fill=(0, 0, 0))
        draw.ellipse([cx + 5, cy, cx + 15, cy + 10], fill=(0, 0, 0))
        draw.ellipse([cx - 5, cy + 15, cx + 5, cy + 25], fill=(100, 50, 0))
        tail_angle = (frame % 20) * 18
        tail_x = cx + body_radius
        tail_y = cy + 20
        tail_end_x = tail_x + 30 * ((tail_angle % 360) / 180 - 1)
        tail_end_y = tail_y - 30 * abs((tail_angle % 360) / 180 - 0.5)
        draw.line([tail_x, tail_y, tail_end_x, tail_end_y], fill=(200, 150, 100), width=3)
        for x_offset in [-20, -5, 5, 20]:
            leg_x = cx + x_offset
            leg_y = cy + 40
            draw.line([leg_x, leg_y, leg_x, leg_y + 25], fill=(150, 100, 50), width=2)


def split_text_into_chunks(text, words_per_chunk=15):
    """Split text into display chunks"""
    words = text.split()
    chunks = []
    current_chunk = []
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= words_per_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(' '.join(current_chunk))


def create_frame_ffmpeg(text, frame, character, font_size=20):
    """Create single frame with character and subtitle"""
    image = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), BG_COLOR)
    character.draw(image, frame, 'talking')
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', font_size)
    except:
        font = ImageFont.load_default()
    
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        test_line = ' '.join(current_line)
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]
        if line_width > VIDEO_WIDTH - 100:
            if len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(test_line)
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    
    subtitle_y = VIDEO_HEIGHT - 120
    if lines:
        draw.rectangle([20, subtitle_y - 10, VIDEO_WIDTH - 20, VIDEO_HEIGHT - 20],
                      fill=(0, 0, 0), outline=(100, 100, 150), width=2)
        y = subtitle_y
        for line in lines[:3]:
            draw.text((40, y), line, fill=(200, 200, 255), font=font)
            y += 30
    return image


def split_text_into_chunks(text, words_per_chunk=15):
    """Split text into chunks of approximately N words for subtitle display"""
    if not text or not text.strip():
        return [""]
    
    words = text.split()
    chunks = []
    current_chunk = []
    
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= words_per_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
    
    # Add remaining words as final chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks if chunks else [""]


def generate_mp4_ffmpeg(audio_path, text_content, output_path, character_type='male', progress_callback=None):
    """Generate MP4 using FFmpeg - 10x faster than MoviePy"""
    temp_dir = None
    try:
        logger.info(f"🎬 Starting FFmpeg video generation with {character_type} character")
        if progress_callback:
            progress_callback(5)
        
        # Get audio duration
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
             '-of', 'default=noprint_wrappers=1:nokey=1:nokey=1', str(audio_path)],
            capture_output=True, text=True, timeout=10
        )
        try:
            duration = float(result.stdout.strip())
        except (ValueError, AttributeError):
            logger.error("Could not determine audio duration")
            return False
        
        logger.info(f"⏱️ Audio duration: {duration:.1f} seconds")
        if progress_callback:
            progress_callback(10)
        
        character = StickFigureFFmpeg(character_type)
        text_chunks = split_text_into_chunks(text_content, words_per_chunk=15)
        logger.info(f"📝 Split text into {len(text_chunks)} subtitle chunks")
        
        temp_dir = tempfile.mkdtemp(prefix="movieweave_")
        temp_path = Path(temp_dir)
        
        num_frames = int(duration * FPS)
        chunk_duration_frames = num_frames / len(text_chunks) if text_chunks else 1
        
        logger.info(f"🖼️ Generating {num_frames} frames at {FPS} FPS...")
        for frame_idx in range(num_frames):
            chunk_idx = min(int(frame_idx / chunk_duration_frames), len(text_chunks) - 1)
            current_text = text_chunks[chunk_idx]
            frame = create_frame_ffmpeg(current_text, frame_idx, character)
            frame_path = temp_path / f"frame_{frame_idx:06d}.png"
            frame.save(frame_path, 'PNG')
            if progress_callback and frame_idx % 50 == 0:
                progress = 10 + (frame_idx / num_frames) * 35
                progress_callback(int(progress))
        
        logger.info(f"✅ Generated {num_frames} frames")
        if progress_callback:
            progress_callback(50)
        
        logger.info("🎥 Encoding video with FFmpeg (fast preset)...")
        ffmpeg_cmd = [
            'ffmpeg', '-y', '-framerate', str(FPS),
            '-pattern_type', 'glob', '-i', str(temp_path / 'frame_*.png'),
            '-i', str(audio_path),
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-c:a', 'aac', '-shortest', '-pix_fmt', 'yuv420p',
            str(output_path)
        ]
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=600)
        if result.returncode != 0:
            logger.error(f"FFmpeg error: {result.stderr}")
            return False
        
        if progress_callback:
            progress_callback(95)
        
        logger.info(f"✅ Video generation complete: {output_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Video generation failed: {e}", exc_info=True)
        return False
    finally:
        if temp_dir and Path(temp_dir).exists():
            try:
                shutil.rmtree(temp_dir)
                logger.info("🧹 Cleaned up temporary directory")
            except Exception as e:
                logger.warning(f"Could not cleanup temp: {e}")

