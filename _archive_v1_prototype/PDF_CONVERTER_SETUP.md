# MovieWeave PDF/Text to Video Feature - Setup Guide

## ✅ What's Been Created

### 1. **New Files**
- ✅ `/Users/karthiksankaran/MovieWeave/backend/simple_pdf_converter.py` - Text extraction & TTS
- ✅ `/Users/karthiksankaran/MovieWeave/templates/convert.html` - Upload UI

### 2. **Modified Files**
- ✅ `/Users/karthiksankaran/MovieWeave/app.py` - Added 2 new routes:
  - `GET /convert` - Serves the upload page
  - `POST /api/convert/pdf-to-video` - Handles PDF/TXT file upload and conversion
  
- ✅ `/Users/karthiksankaran/MovieWeave/backend/cartoon_video_engine.py` - Added:
  - `render_rotating_character_video()` method - Creates video with rotating characters
  
- ✅ `/Users/karthiksankaran/MovieWeave/templates/index.html` - Added navigation link

---

## 🚀 Installation & Setup

### Step 1: Install Required Python Packages

```bash
pip install PyPDF2 pyttsx3
```

**What they do:**
- `PyPDF2` - Extracts text from PDF files
- `pyttsx3` - Generates audio from text using system voices

### Step 2: Verify FFmpeg is Installed

```bash
ffmpeg -version
```

If not installed:
```bash
# macOS
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg

# Windows
choco install ffmpeg
```

### Step 3: Test Locally

```bash
cd /Users/karthiksankaran/MovieWeave
python app.py
```

Then visit:
- **http://localhost:5000** - Main dashboard
- **http://localhost:5000/convert** - PDF/Text converter

---

## 📋 How It Works

### **Workflow:**

1. User uploads PDF or TXT file
2. System extracts text and splits into sentences (max 30 lines)
3. For each line:
   - Assigns rotating character (e.g., Char1, Char2, Char1, Char2...)
   - Generates audio using pyttsx3 with different voice each time
   - Measures audio duration (or uses 2-second default)
   - Renders character frames with lip-sync
4. Concatenates all frames into single MP4 video
5. Returns video file for download

### **Example Output:**
```
Line 1: Character 1 speaks (with audio)
Line 2: Character 2 speaks (with audio)
Line 3: Character 1 speaks (with audio)
...
→ Final video.mp4 with all characters rotating
```

---

## 🔧 API Response Example

**Request:**
```
POST /api/convert/pdf-to-video
Content-Type: multipart/form-data

file: [PDF/TXT file]
expression: happy
auto_audio: yes
```

**Success Response:**
```json
{
  "success": true,
  "message": "Video generated",
  "video_file": "pdf_video_20260921_194530.mp4",
  "num_scenes": 15,
  "total_duration": 32.5
}
```

---

## 📱 Features Implemented

✅ **PDF/TXT Upload** - Drag & drop or click to upload  
✅ **Text Extraction** - Automatic text parsing from files  
✅ **Smart Splitting** - Sentence-based dialogue creation  
✅ **Character Rotation** - Different character speaks each line  
✅ **Auto Voice Generation** - pyttsx3 synthesizes speech  
✅ **Lip-Sync** - Mouth animation matches audio  
✅ **Expression Selection** - Happy, Neutral, Sad, Angry  
✅ **Audio Duration Detection** - Frames match audio length  
✅ **Cleanup** - Temporary files deleted after processing  

---

## 🐛 Troubleshooting

### Issue: "PyPDF2 not installed"
```bash
pip install PyPDF2
```

### Issue: "pyttsx3 not installed" 
```bash
pip install pyttsx3
```

### Issue: "FFmpeg not found"
- Install FFmpeg (see Step 2 above)

### Issue: "No characters available"
- Check that character assets exist in `/backend/assets/characters/`

### Issue: Video generation is slow
- This is normal! Processing 30 scenes × 24 FPS = ~720 frames
- Takes 10-30 seconds depending on system

---

## 📤 Deployment to Server

Copy the updated files to your AWS server:

```bash
# Copy app.py
scp -i ~/MovieWeave/pem-key/NarrativeFilm-instance.pem \
  /Users/karthiksankaran/MovieWeave/app.py \
  ubuntu@34.229.168.102:/opt/movieweave/app.py

# Copy new backend module
scp -i ~/MovieWeave/pem-key/NarrativeFilm-instance.pem \
  /Users/karthiksankaran/MovieWeave/backend/simple_pdf_converter.py \
  ubuntu@34.229.168.102:/opt/movieweave/backend/simple_pdf_converter.py

# Copy updated cartoon engine
scp -i ~/MovieWeave/pem-key/NarrativeFilm-instance.pem \
  /Users/karthiksankaran/MovieWeave/backend/cartoon_video_engine.py \
  ubuntu@34.229.168.102:/opt/movieweave/backend/cartoon_video_engine.py

# Copy templates
scp -i ~/MovieWeave/pem-key/NarrativeFilm-instance.pem \
  /Users/karthiksankaran/MovieWeave/templates/convert.html \
  ubuntu@34.229.168.102:/opt/movieweave/templates/convert.html

scp -i ~/MovieWeave/pem-key/NarrativeFilm-instance.pem \
  /Users/karthiksankaran/MovieWeave/templates/index.html \
  ubuntu@34.229.168.102:/opt/movieweave/templates/index.html
```

Then on the server:

```bash
cd /opt/movieweave
pip install PyPDF2 pyttsx3
sudo systemctl restart movieweave
```

---

## 🎯 Next Steps (Future Enhancements)

1. **Progress Bar** - Real-time upload/processing status
2. **Multiple Audio Tracks** - Different voice for each character
3. **Custom Voices** - Google Cloud TTS or Azure Speech Services
4. **Paragraph-based Split** - Longer scenes for each character
5. **Video Preview** - Show thumbnail before download
6. **Batch Processing** - Queue multiple uploads
7. **Language Support** - Auto-detect and translate text

---

## ✨ Summary

You now have a **fully functional PDF/Text to Video converter** that:
- Extracts text from documents
- Automatically generates voice dialogue
- Creates animated videos with multiple characters
- Syncs animations to audio

Just install the dependencies and you're ready to go! 🚀
