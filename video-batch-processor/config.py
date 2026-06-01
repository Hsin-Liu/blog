"""
Configuration for Video Batch Processor.
Optimized for RTX 5060 Ti (16GB) with CUDA 12.4+.
"""

from pathlib import Path

# =============================================================================
# Whisper Configuration (RTX 5060 Ti optimized)
# =============================================================================

# Model: large-v3-turbo for Chinese-English initial screening
# VRAM: ~6GB in FP16, leaves plenty of headroom on 16GB card
WHISPER_MODEL = "large-v3-turbo"

# Compute type: float16 for 40% less VRAM + 50%+ throughput
COMPUTE_TYPE = "float16"

# Language: explicit "zh" activates Chinese-specific decoding path
# Better recognition for mixed Chinese-English content
LANGUAGE = "zh"

# Decoding parameters optimized for speed (initial screening use case)
BEAM_SIZE = 1
BEST_OF = 1
TEMPERATURE = 0.0  # Deterministic decoding

# Disable word-level timestamps to save computation
WORD_TIMESTAMPS = False

# Voice Activity Detection: skip silent segments
VAD_FILTER = True

# Batch size: 8-16 videos can run in parallel on 16GB VRAM
BATCH_SIZE = 8

# =============================================================================
# PPT Extraction Configuration (CPU)
# =============================================================================

# Similarity threshold for slide detection
# 0.85 default; lower (0.75) for videos with frequent transitions
# higher (0.90) for videos with animations
PPT_THRESHOLD = 0.85

# CPU threads for extraction
PPT_THREADS = 4

# =============================================================================
# Output Configuration
# =============================================================================

# Supported output formats
OUTPUT_FORMATS = ["markdown", "html", "word"]

# Default format list
DEFAULT_OUTPUT_FORMATS = ["markdown", "html"]

# Image quality (JPEG)
IMAGE_QUALITY = 90

# Image max width (pixels)
IMAGE_MAX_WIDTH = 1200

# =============================================================================
# FFmpeg Configuration
# =============================================================================

# Audio extraction settings
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1  # Mono

# FFmpeg path (leave None for system PATH)
FFMPEG_PATH = None

# =============================================================================
# Path Configuration
# =============================================================================

def get_default_output_dir(video_path: str) -> Path:
    """Generate output directory from video path."""
    video_name = Path(video_path).stem
    return Path("output") / video_name

# =============================================================================
# Logging Configuration
# =============================================================================

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
