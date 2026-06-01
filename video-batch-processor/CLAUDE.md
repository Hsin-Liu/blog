# Video Batch Processor

> Sub-project of [self-hosted-blog](../self-hosted-blog/CLAUDE.md)

A batch processing tool for teaching videos that:
1. Extracts PPT/slides frames from videos (CPU)
2. Transcribes audio to text via Whisper (GPU)
3. Aligns timeline and generates Markdown/HTML/Word reports

## Project Overview

- **Type**: Batch processing CLI tool
- **Stack**: Python 3.10+, Faster-Whisper, extract-video-ppt, FFmpeg
- **Purpose**: Automatically process teaching videos → structured notes with timeline

## Architecture

```
Input Videos
     ↓
┌─────────────────────────────┐
│  Parallel Processing        │
│  ├─ CPU: extract-video-ppt  │→ PPT images + timestamps
│  └─ GPU: Whisper            │→ transcription + timestamps
└─────────────────────────────┘
     ↓
Timeline Alignment + Report Generation
     ↓
Output: Markdown / HTML / Word
```

## Hardware Configuration

### RTX 5060 Ti (16GB) Optimization

| Component | Requirement |
|-----------|-------------|
| GPU | NVIDIA RTX 5060 Ti (16GB VRAM) |
| Architecture | Blackwell (CUDA 12.4+ required) |
| Memory | ~6GB used by large-v3-turbo FP16 |

**Critical**: CUDA 12.4+ required for Blackwell architecture. CUDA 11.x causes 30-40% performance drop.

### CUDA Setup

```bash
# 1. Uninstall old PyTorch
pip uninstall torch torchvision -y

# 2. Install CUDA 12.x compatible PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124

# 3. Install Faster-Whisper
pip install faster-whisper
```

## Model Configuration

| Model | VRAM | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| large-v3-turbo | ~6GB | 7-8x faster than large-v3 | -0.3% vs large-v3 | **Recommended for initial screening** |
| large-v3 | ~10GB | Baseline | Best | High-precision needs |
| medium | ~5GB | Faster | Lower | Low-VRAM systems |

### Optimal Parameters for "中英文初筛" (Chinese-English Initial Screening)

```python
WHISPER_MODEL = "large-v3-turbo"
COMPUTE_TYPE = "float16"      # 40% less VRAM, 50%+ throughput
LANGUAGE = "zh"                # Explicit Chinese → better mixed zh/en
BEAM_SIZE = 1                  # Fastest decoding
BEST_OF = 1
TEMPERATURE = 0.0              # Deterministic decoding
WORD_TIMESTAMPS = False        # Skip word-level timestamps
VAD_FILTER = True              # Skip silent segments

# Batch processing (16GB has room)
BATCH_SIZE = 8-16             # Parallel video processing
```

## Usage

### Single Video

| File | Purpose |
|------|---------|
| `video_summarizer.py` | Main orchestrator class |
| `batch_processor.py` | Batch processing multiple videos |
| `report_generator.py` | Output generation (MD/HTML/Word) |
| `config.py` | Configuration and constants |

## Usage

### Single Video

```bash
python video_summarizer.py --input video.mp4 --output ./output
```

### Batch Mode

```bash
python batch_processor.py --input-dir ./videos --output-dir ./batch_output
```

### Output Structure

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

## Configuration

Edit `config.py` to adjust:
- `WHISPER_MODEL`: Model size (default: large-v3-turbo)
- `PPT_THRESHOLD`: Similarity threshold for slide detection
- `GPU_DEVICE`: CUDA device index
- `BATCH_SIZE`: Number of videos to process concurrently

## Windows Compatibility

- All paths use `pathlib` for cross-platform compatibility
- FFmpeg must be in PATH or set `FFMPEG_PATH` in config
- Batch script supports Windows Task Scheduler

## Status

- [x] Core `video_summarizer.py` implementation
- [x] `batch_processor.py` for multiple videos
- [x] Report generation integrated in `video_summarizer.py` (MD/HTML/Word)
- [x] `config.py` with adjustable parameters
- [x] `run_batch.bat` for Windows Task Scheduler
- [ ] Unit tests