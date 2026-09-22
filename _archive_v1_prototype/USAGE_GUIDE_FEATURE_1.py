"""
USAGE GUIDE: Feature 1 - Cartoon Character System
Quick reference for using all classes.
"""

from pathlib import Path
from backend.cartoon_character_generator import CartoonCharacterGenerator, CharacterStyle
from backend.character_manager import CharacterManager
from backend.lip_sync_engine import LipSyncEngine

# ============================================================================
# 1. GENERATE NEW CHARACTERS
# ============================================================================

generator = CartoonCharacterGenerator(Path("backend/assets/characters"))

# Custom colors
style = CharacterStyle(
    skin_color=(255, 200, 140),
    hair_color=(50, 30, 20),
    shirt_color=(30, 100, 200),
    eye_color=(50, 100, 200),
    mouth_color=(200, 100, 100)
)
generator.generate_character('my_hero', style)

# Random style
hero_style = CartoonCharacterGenerator.get_random_style('hero')
generator.generate_character('random_hero', hero_style)

villain_style = CartoonCharacterGenerator.get_random_style('villain')
generator.generate_character('random_villain', villain_style)

# ============================================================================
# 2. LOAD CHARACTERS
# ============================================================================

manager = CharacterManager(Path("backend/assets/characters"))

# Load single character
hero = manager.load_character('hero_001')

# Load all characters
all_chars = manager.load_all_characters()

# Get available characters
available = manager.get_available_characters()

# ============================================================================
# 3. RENDER FRAMES
# ============================================================================

# Get available options
expressions = hero.get_available_expressions()  # ['neutral', 'happy', 'sad', 'angry']
mouths = hero.get_available_mouths()  # ['A', 'E', 'I', 'O', 'U', 'MBP', 'X']

# Render expression
neutral = hero.get_expression_frame('neutral')
neutral.save('output/neutral.png')

# Render mouth shape
mouth_a = hero.get_mouth_shape('A')
mouth_a.save('output/mouth_a.png')

# Render complete frame
frame = hero.render_frame(expression='happy', mouth_shape='A')
frame.save('output/frame.png')

# ============================================================================
# 4. LIP-SYNC ENGINE
# ============================================================================

engine = LipSyncEngine()

# Extract mouth shapes
events = engine.extract_mouth_shapes()

# Get mouth at specific time
mouth = engine.get_mouth_at_time(1.5)  # Returns 'A', 'E', etc.

# Get events in time range
range_events = engine.get_events_in_range(0.0, 2.0)

# Export to JSON
engine.export_to_json(Path("output/lip_sync.json"))

# ============================================================================
# 5. BATCH RENDER ALL EXPRESSIONS
# ============================================================================

output_dir = Path("output/expressions")
output_dir.mkdir(parents=True, exist_ok=True)

for expr in hero.get_available_expressions():
    frame = hero.render_frame(expression=expr, mouth_shape='X')
    frame.save(output_dir / f"{expr}.png")

# ============================================================================
# 6. CREATE ANIMATION SEQUENCE
# ============================================================================

def create_animation(character, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    sequence = [
        ('neutral', 'X', 2),
        ('happy', 'A', 2),
        ('happy', 'E', 2),
        ('neutral', 'X', 2),
    ]
    
    frame_num = 0
    for expr, mouth, count in sequence:
        frame = character.render_frame(expression=expr, mouth_shape=mouth)
        for i in range(count):
            frame.save(output_dir / f"frame_{frame_num:04d}.png")
            frame_num += 1
    return frame_num

num_frames = create_animation(hero, Path("output/animation"))
print(f"Created {num_frames} frames ({num_frames/24:.2f}s at 24 FPS)")

# ============================================================================
# 7. RENDER DIALOGUE WITH LIP-SYNC
# ============================================================================

def render_dialogue(char_name, expr='neutral'):
    output_dir = Path(f"output/{char_name}_dialogue")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    mgr = CharacterManager(Path("backend/assets/characters"))
    char = mgr.load_character(char_name)
    if not char:
        return False
    
    eng = LipSyncEngine()
    eng.extract_mouth_shapes()
    
    # 60 frames = 2.5 seconds at 24 FPS
    for frame_num in range(60):
        time = frame_num / 24.0
        mouth = eng.get_mouth_at_time(time)
        frame = char.render_frame(expression=expr, mouth_shape=mouth)
        frame.save(output_dir / f"frame_{frame_num:04d}.png")
    
    return True

# render_dialogue('hero_001', 'happy')
