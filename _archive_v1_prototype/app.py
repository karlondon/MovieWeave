"""app.py - MovieWeave Flask Web Application"""
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from pathlib import Path
import logging
from datetime import datetime
from backend.cartoon_video_engine import CartoonVideoEngine
from backend.character_manager import CharacterManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = Path('uploads')
app.config['OUTPUT_FOLDER'] = Path('output/videos')

app.config['UPLOAD_FOLDER'].mkdir(parents=True, exist_ok=True)
app.config['OUTPUT_FOLDER'].mkdir(parents=True, exist_ok=True)

# Initialize components
video_engine = CartoonVideoEngine(Path('backend/assets/characters'), app.config['OUTPUT_FOLDER'])
character_manager = CharacterManager(Path('backend/assets/characters'))

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '3.0.0'}), 200

@app.route('/api/characters', methods=['GET'])
def get_characters():
    """Get available characters"""
    try:
        characters = character_manager.get_available_characters()
        return jsonify({'success': True, 'count': len(characters), 'characters': characters}), 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/characters/<char_name>', methods=['GET'])
def get_character_info(char_name):
    """Get character details"""
    try:
        character = character_manager.load_character(char_name)
        if not character:
            return jsonify({'success': False, 'error': 'Not found'}), 404
        
        return jsonify({
            'success': True,
            'name': char_name,
            'expressions': character.get_available_expressions(),
            'mouths': character.get_available_mouths()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/video/generate', methods=['POST'])
def generate_video():
    """Generate video"""
    try:
        data = request.get_json()
        char_name = data.get('character_name')
        expression = data.get('expression', 'neutral')
        duration = float(data.get('duration', 3.0))
        
        if not char_name:
            return jsonify({'success': False, 'error': 'character_name required'}), 400
        
        if char_name not in character_manager.get_available_characters():
            return jsonify({'success': False, 'error': 'Character not found'}), 404
        
        if expression not in ['neutral', 'happy', 'sad', 'angry']:
            return jsonify({'success': False, 'error': 'Invalid expression'}), 400
        
        if duration < 0.5 or duration > 60:
            return jsonify({'success': False, 'error': 'Duration 0.5-60 seconds'}), 400
        
        audio_file = None
        if 'audio' in request.files:
            audio = request.files['audio']
            audio_path = app.config['UPLOAD_FOLDER'] / audio.filename
            audio.save(audio_path)
            audio_file = audio_path
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = app.config['OUTPUT_FOLDER'] / f"{char_name}_{expression}_{timestamp}.mp4"
        
        success = video_engine.render_dialogue_video(
            character_name=char_name,
            expression=expression,
            duration_seconds=duration,
            audio_file=audio_file,
            output_file=output_file
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Video generated',
                'video_file': output_file.name,
                'duration': duration
            }), 200
        else:
            return jsonify({'success': False, 'error': 'Generation failed'}), 500
            
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/video/<filename>', methods=['GET'])
def download_video(filename):
    """Download video"""
    try:
        file_path = app.config['OUTPUT_FOLDER'] / filename
        if not file_path.exists():
            return jsonify({'success': False, 'error': 'Not found'}), 404
        return send_file(file_path, mimetype='video/mp4', as_attachment=True)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Dashboard"""
    from flask import make_response
    response = make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/generate', methods=['GET'])
def generate_page():
    """Video generator"""
    from flask import make_response
    response = make_response(render_template('generate.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/gallery', methods=['GET'])
def gallery_page():
    """Gallery"""
    from flask import make_response
    response = make_response(render_template('gallery.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/convert', methods=['GET'])
def convert_page():
    """PDF/Text to Video converter page"""
    from flask import make_response
    response = make_response(render_template('convert.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/api/convert/pdf-to-video', methods=['POST'])
def convert_pdf_to_video():
    """Convert PDF or TXT file to video with rotating characters"""
    try:
        from backend.simple_pdf_converter import SimplePDFConverter
        
        # Validate file
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Validate file type
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ['.pdf', '.txt', '.text']:
            return jsonify({'success': False, 'error': 'Only PDF and TXT files supported'}), 400
        
        # Save uploaded file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        upload_path = app.config['UPLOAD_FOLDER'] / f"upload_{timestamp}{file_ext}"
        file.save(upload_path)
        
        logger.info(f"Processing file: {upload_path}")
        
        # Extract text
        converter = SimplePDFConverter(app.config['UPLOAD_FOLDER'])
        text = converter.extract_text(upload_path)
        
        if not text or len(text.strip()) < 10:
            return jsonify({'success': False, 'error': 'File is empty or too small'}), 400
        
        # Split text into lines
        dialogue_lines = converter.split_text_into_lines(text)
        logger.info(f"Extracted {len(dialogue_lines)} dialogue lines")
        
        # Get parameters
        expression = request.form.get('expression', 'happy')
        auto_audio = request.form.get('auto_audio', 'yes') == 'yes'
        
        # Get available characters
        characters = character_manager.get_available_characters()
        if not characters:
            return jsonify({'success': False, 'error': 'No characters available'}), 500
        
        logger.info(f"Using {len(characters)} available characters: {characters}")
        
        # Generate audio and collect durations
        audio_files = []
        durations = []
        
        if auto_audio:
            for idx, line in enumerate(dialogue_lines):
                audio_path = app.config['UPLOAD_FOLDER'] / f"audio_{timestamp}_{idx}.wav"
                char_idx = idx % len(characters)
                
                success = converter.generate_audio(line, audio_path, voice_id=char_idx % 2)
                
                if success:
                    duration = converter.get_audio_duration(audio_path)
                    audio_files.append(audio_path)
                    durations.append(duration)
                    logger.info(f"Generated audio for line {idx}: {duration:.2f}s")
                else:
                    audio_files.append(None)
                    durations.append(2.0)  # Default 2 seconds
        else:
            # No audio, use default durations
            audio_files = [None] * len(dialogue_lines)
            durations = [2.0] * len(dialogue_lines)
        
        # Generate video with rotating characters
        output_file = app.config['OUTPUT_FOLDER'] / f"pdf_video_{timestamp}.mp4"
        
        success = video_engine.render_rotating_character_video(
            dialogue_lines=dialogue_lines,
            characters=characters,
            expression=expression,
            audio_files=audio_files,
            durations=durations,
            output_file=output_file
        )
        
        # Cleanup uploaded file
        try:
            upload_path.unlink()
        except:
            pass
        
        # Cleanup audio files
        for audio_file in audio_files:
            if audio_file:
                try:
                    audio_file.unlink()
                except:
                    pass
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Video generated',
                'video_file': output_file.name,
                'num_scenes': len(dialogue_lines),
                'total_duration': sum(durations)
            }), 200
        else:
            return jsonify({'success': False, 'error': 'Video generation failed'}), 500
            
    except Exception as e:
        logger.error(f"Error in pdf-to-video: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500



@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Error: {error}")
    return jsonify({'success': False, 'error': 'Internal error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
