# Video Batch Processor

A batch processing tool for teaching videos that extracts PPT frames and transcribes audio to generate timeline-aligned notes.

## Features

- **PPT Extraction**: Extract slide frames from videos (CPU)
- **Whisper Transcription**: GPU-accelerated speech-to-text (NVIDIA RTX 5060 Ti optimized)
- **Timeline Alignment**: Automatic synchronization of slides and transcript
- **Multi-Format Output**: Markdown, HTML, Word reports
- **Batch Processing**: Process multiple videos sequentially
- **Windows Compatible**: Batch scripts for Task Scheduler

## Hardware Requirements

| Component | Specification |
|-----------|---------------|
| GPU | NVIDIA RTX 5060 Ti (16GB VRAM) |
| CUDA | 12.4+ (Blackwell architecture) |
| RAM | 16GB+ recommended |
| Storage | SSD for temp files |

## Installation

### 1. Install CUDA 12.4+

Download from: https://developer.nvidia.com/cuda-downloads

### 2. Install Python Dependencies

```powershell
# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\activate

# Install PyTorch with CUDA 12.4
pip uninstall torch torchvision -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124

# Install other dependencies
pip install extract-video-ppt faster-whisper opencv-python pillow pandas python-docx
```

### 3. Install FFmpeg

```powershell
# Windows: via Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

## Quick Start

### Single Video

```powershell
python video_summarizer.py --input video.mp4 --output .\output
```

### Batch Mode

```powershell
python batch_processor.py --input-dir .\videos --output-dir .\batch_output --recursive
```

### Using Windows Batch Script

```powershell
# Interactive mode
.\run_batch.bat

# Direct arguments
.\run_batch.bat "C:\Videos" "C:\Output"
```

## Configuration

Edit `config.py` to adjust:

```python
# Whisper model (large-v3-turbo for speed, large-v3 for accuracy)
WHISPER_MODEL = "large-v3-turbo"

# Compute type (float16 for RTX 5060 Ti)
COMPUTE_TYPE = "float16"

# Language for transcription
LANGUAGE = "zh"  # Chinese

# Batch size for parallel processing
BATCH_SIZE = 8   # Adjust based on VRAM

# PPT detection threshold (0.75-0.90)
PPT_THRESHOLD = 0.85
```

## Output Structure

```
output/
├── timeline_summary.md          # Markdown report
├── timeline_summary.html        # HTML report (with images)
├── timeline_summary.docx        # Word document
├── temp_audio.wav               # Extracted audio
└── ppt_images/
    ├── frame_0001_00-00-00.jpg
    ├── frame_0002_00-02-30.jpg
    └── ...
```

## Windows Task Scheduler Setup

1. Open Task Scheduler (`taskschd.msc`)
2. Create Basic Task
3. Set trigger (daily/weekly as needed)
4. Action: Start a program
   - Program: `cmd.exe`
   - Arguments: `/c "C:\path\to\video-batch-processor\run_batch.bat" "C:\InputVideos" "C:\OutputDir"`
5. Configure settings and finish

## Troubleshooting

### "CUDA out of memory"
- Reduce `BATCH_SIZE` in config.py
- Close other GPU applications

### "FFmpeg not found"
- Ensure FFmpeg is in PATH
- Or set `FFMPEG_PATH` in config.py

### "extract-video-ppt not found"
```powershell
pip install extract-video-ppt
```

### Slow transcription
- Verify CUDA 12.4+ is installed
- Check model is using GPU (not CPU)
- Reduce batch_size if memory constrained

## Project Structure

```
video-batch-processor/
├── CLAUDE.md           # This file
├── README.md           # Setup and usage guide
├── config.py           # Configuration
├── video_summarizer.py # Core processing class
├── batch_processor.py  # Multi-video processor
├── run_batch.bat       # Windows batch runner
└── requirements.txt    # Dependencies list
```
