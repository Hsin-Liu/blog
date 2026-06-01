"""
Batch Processor - Process multiple videos sequentially.

Since Whisper model uses ~6GB VRAM on 16GB card, sequential processing
ensures stable memory usage. The model stays loaded in memory for
faster subsequent processing.

For true parallel processing on multiple GPUs, run multiple instances.
"""

import sys
import logging
from pathlib import Path
from typing import Optional

from video_summarizer import VideoSummarizer
import config

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)


class BatchProcessor:
    """Process multiple videos sequentially with one Whisper model instance."""

    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        recursive: bool = False,
        video_extensions: tuple[str, ...] = (".mp4", ".avi", ".mov", ".mkv", ".wmv")
    ):
        """
        Initialize BatchProcessor.

        Args:
            input_dir: Directory containing input videos
            output_dir: Base output directory
            recursive: Search subdirectories for videos
            video_extensions: Supported video file extensions
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.recursive = recursive
        self.video_extensions = video_extensions

        if not self.input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")

        # Find all video files
        self.videos = self._find_videos()
        logger.info(f"Found {len(self.videos)} video(s) to process")

    def _find_videos(self) -> list[Path]:
        """Find all video files in input directory."""
        videos = []

        if self.recursive:
            pattern = "**/*"
        else:
            pattern = "*"

        for ext in self.video_extensions:
            videos.extend(self.input_dir.glob(f"{pattern}{ext}"))
            videos.extend(self.input_dir.glob(f"{pattern}{ext.upper()}"))

        return sorted(videos)

    def run(self, output_formats: list[str] = None) -> dict:
        """
        Process all videos sequentially.

        Args:
            output_formats: List of output formats

        Returns:
            Dict with per-video results and summary
        """
        if output_formats is None:
            output_formats = config.DEFAULT_OUTPUT_FORMATS

        results = {
            "total": len(self.videos),
            "successful": 0,
            "failed": 0,
            "videos": []
        }

        logger.info(f"🚀 Starting batch processing: {results['total']} video(s)")

        for i, video_path in enumerate(self.videos, 1):
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing video {i}/{results['total']}: {video_path.name}")
            logger.info(f"{'='*60}")

            # Create output subdirectory for this video
            video_output = self.output_dir / video_path.stem

            try:
                summarizer = VideoSummarizer(
                    video_path=str(video_path),
                    output_dir=str(video_output),
                    whisper_model=config.WHISPER_MODEL,
                    compute_type=config.COMPUTE_TYPE,
                    language=config.LANGUAGE,
                    batch_size=config.BATCH_SIZE
                )

                output_paths = summarizer.run(output_formats=output_formats)

                results["videos"].append({
                    "video": str(video_path),
                    "status": "success",
                    "outputs": {k: str(v) for k, v in output_paths.items() if k != "timeline"}
                })
                results["successful"] += 1

            except Exception as e:
                logger.error(f"❌ Failed to process {video_path.name}: {e}")
                results["videos"].append({
                    "video": str(video_path),
                    "status": "failed",
                    "error": str(e)
                })
                results["failed"] += 1

        # Print summary
        self._print_summary(results)

        return results

    def _print_summary(self, results: dict) -> None:
        """Print batch processing summary."""
        logger.info(f"\n{'='*60}")
        logger.info("BATCH PROCESSING COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"Total: {results['total']}")
        logger.info(f"Successful: {results['successful']}")
        logger.info(f"Failed: {results['failed']}")

        if results["failed"] > 0:
            logger.info("\nFailed videos:")
            for v in results["videos"]:
                if v["status"] == "failed":
                    logger.info(f"  - {v['video']}: {v['error']}")


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Video Batch Processor")
    parser.add_argument("--input-dir", "-i", required=True, help="Input directory with videos")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory")
    parser.add_argument(
        "--formats", "-f",
        nargs="+",
        default=["markdown", "html"],
        choices=["markdown", "html", "word"],
        help="Output formats"
    )
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="Search subdirectories recursively"
    )
    parser.add_argument(
        "--extensions", "-e",
        nargs="+",
        default=[".mp4", ".avi", ".mov", ".mkv", ".wmv"],
        help="Video file extensions"
    )

    args = parser.parse_args()

    try:
        processor = BatchProcessor(
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            recursive=args.recursive,
            video_extensions=tuple(args.extensions)
        )
        results = processor.run(output_formats=args.formats)

        if results["failed"] > 0:
            sys.exit(1)

    except Exception as e:
        logger.error(f"Batch processing failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
