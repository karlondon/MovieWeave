"""Fast MP4 video generation using FFmpeg directly instead of MoviePy"""
import logging
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import shutil
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

# Thread pool for CPU-intensive frame generation
frame_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="frame_gen_")

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
        arm_angle = 20 + (frame % 12) * 2 if state == 'talking' else 15
        arm_left_x = cx - arm_length * (arm_angle / 90)
        arm_right_x = cx + arm_length * (arm_angle / 90)
        arm_y = body_top + 18
        draw.line([cx, arm_y, arm_left_x, arm_y - 12], fill=(220, 190, 160), width=2)
        draw.line([cx, arm_y, arm_right_x, arm_y - 12], fill=(220, 190, 160), width=2)
        draw.line([cx, body_bottom, cx - 12, body_bottom + 45], fill=(100, 80, 150), width=2)
        draw.line([cx, body_bottom, cx + 12, body_bottom + 45], fill=(100, 80, 150), width=2)
    
    def _draw_animal(self, draw, cx, cy, frame, state):
        """Draw animal character"""
        head_x, head_y = cx, cy - 20
        body_x1, body_y1 = cx - 40, cy + 20
        body_x2, body_y2 = cx + 40, cy + 20
        draw.ellipse([head_x - 35, head_y - 35, head_x + 35, head_y + 35], 
                    fill=(200, 120, 60), outline=(150, 80, 20), width=2)
        draw.ellipse([head_x - 25, head_y - 20, head_x - 5, head_y], fill=(150, 80, 20))
        draw.ellipse([head_x + 5, head_y - 20, head_x + 25, head_y], fill=(150, 80, 20))
        draw.ellipse([head_x - 10, head_y - 5, head_x - 2, head_y + 3], fill=(0, 0, 0))
        draw.ellipse([head_x + 2, head_y - 5, head_x + 10, head_y + 3], fill=(0, 0, 0))
        draw.rectangle([body_x1, body_y1, body_x2, body_y2], 
                      fill=(200, 120, 60), outline=(150, 80, 20), width=2)
        tail_wag = 20 + (frame % 8) * 5 if state == 'talking' else 15
        draw.line([body_x2, body_y2 - 10, body_x2 + 30, body_y2 - 10 + tail_wag], 
                 fill=(200, 120, 60), width=4)



def create_frame_ffmpeg(text, frame_idx, character):
    """Create a single frame for video"""
    frame = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), BG_COLOR)
    
    # Draw animated character
    character.draw(frame, frame_idx, animation_state='talking')
    
    # Draw text subtitle at bottom
    draw = ImageDraw.Draw(frame)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    text_y = VIDEO_HEIGHT - 80
    text_color = (220, 220, 240)
    
    # Word wrap text
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        test_text = ' '.join(current_line)
        bbox = draw.textbbox((0, 0), test_text, font=font)
        text_width = bbox[2] - bbox[0]
        
        if text_width > VIDEO_WIDTH - 100:
            if len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(test_text)
                current_line = []
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw lines
    start_y = text_y - (len(lines) - 1) * 35 // 2
    for i, line in enumerate(lines):
        y = start_y + i * 35
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (VIDEO_WIDTH - line_width) // 2
        draw.text((x, y), line, fill=text_color, font=font)
    
    return frame


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
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks if chunks else [""]


def get_audio_duration(audio_path):
    """Get audio duration in seconds using ffprobe"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            duration = float(result.stdout.strip())
            logger.info(f"⏱️ Audio duration: {duration:.1f} seconds")
            return duration
        else:
            logger.error(f"ffprobe failed or no output")
            return None
    except Exception as e:
        logger.error(f"Failed to get audio duration: {e}")
        return None


def generate_frames_batch(batch_start, batch_end, temp_path, text_chunks, 
                          chunk_duration_frames, character):
    """Generate a batch of frames (runs in thread pool)"""
    try:
        for frame_idx in range(batch_start, batch_end):
            chunk_idx = min(int(frame_idx / chunk_duration_frames), len(text_chunks) - 1)
            current_text = text_chunks[chunk_idx]
            frame = create_frame_ffmpeg(current_text, frame_idx, character)
            frame_path = temp_path / f"frame_{frame_idx:06d}.png"
            frame.save(frame_path, 'PNG')
        return batch_end - batch_start
    except Exception as e:
        logger.error(f"Error generating batch frames {batch_start}-{batch_end}: {e}")
        raise



async def generate_mp4_ffmpeg(audio_path, text_content, output_path, character_type='male', progress_callback=None):
    """Generate MP4 using FFmpeg - properly async with thread pool for CPU work"""
    temp_dir = None
    loop = asyncio.get_event_loop()
    
    try:
        logger.info(f"🎬 Starting FFmpeg video generation with {character_type} character")
        if progress_callback:
            progress_callback(5)
        
        # Get audio duration (synchronous call - quick)
        duration = get_audio_duration(str(audio_path))
        if duration is None:
            logger.error("❌ Could not determine audio duration")
            return False
        
        logger.info(f"⏱️ Audio duration: {duration:.1f} seconds")
        if progress_callback:
            progress_callback(10)
        
        # Prepare for frame generation
        character = StickFigureFFmpeg(character_type)
        text_chunks = split_text_into_chunks(text_content, words_per_chunk=15)
        logger.info(f"📝 Split text into {len(text_chunks)} subtitle chunks")
        
        temp_dir = tempfile.mkdtemp(prefix="movieweave_")
        temp_path = Path(temp_dir)
        
        num_frames = int(duration * FPS)
        chunk_duration_frames = num_frames / len(text_chunks) if text_chunks else 1
        
        logger.info(f"🖼️ Generating {num_frames} frames at {FPS} FPS (async with thread pool)...")
        
        # Generate frames in batches using thread pool
        batch_size = 100
        for batch_start in range(0, num_frames, batch_size):
            batch_end = min(batch_start + batch_size, num_frames)
            
            # Run batch frame generation in thread pool to avoid blocking event loop
            await loop.run_in_executor(
                frame_executor,
                generate_frames_batch,
                batch_start, batch_end, temp_path, text_chunks,
                chunk_duration_frames, character
            )
            
            # Update progress after each batch
            if progress_callback:
                progress = 10 + (batch_end / num_frames) * 35
                progress_callback(int(progress))
                logger.info(f"📊 Frame generation progress: {int(progress)}%")
            
            # Yield to event loop to allow other tasks to run
            await asyncio.sleep(0)
        
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
        
        # Run FFmpeg encoding in thread pool to not block event loop
        result = await loop.run_in_executor(
            None,
            subprocess.run,
            ffmpeg_cmd
        )
        
        if result.returncode != 0:
            logger.error(f"❌ FFmpeg encoding failed with code {result.returncode}")
            return False
        
        if progress_callback:
            progress_callback(95)
        
        logger.info(f"✅ Video generation complete: {output_path}")
        if output_path.exists():
            logger.info(f"📹 MP4 file size: {output_path.stat().st_size / (1024*1024):.1f} MB")
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
                logger.warning(f"⚠️ Could not cleanup temp: {e}")
