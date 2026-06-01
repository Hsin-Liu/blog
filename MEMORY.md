# MEMORY — Self-Hosted Blog

## Metadata

- **Project**: self-hosted-blog
- **Parent**: Ai Note Code & Docs / Develop
- **Type**: static site / blog
- **Status**: scaffolded
- **Stack**: Hugo + PaperMod theme

## Hugo Setup

- Hugo binary: `v0.162.1+extended` (Homebrew)
- Theme: [PaperMod](https://github.com/adityatelange/hugo-PaperMod) (git submodule)
- Content: `content/posts/`
- Output: `public/` (gitignored, served by GitHub Pages)

## Next Steps

- [ ] Create GitHub repo and connect remote
- [ ] Configure GitHub Actions for auto-deploy
- [ ] Customize `hugo.toml` (title, description, author)
- [ ] Write first posts

## Sub-Projects

### video-batch-processor

- **Type**: Python CLI batch processing tool
- **Purpose**: Process teaching videos → timeline-aligned notes (PPT frames + Whisper transcription)
- **Stack**: Python 3.10+, Faster-Whisper, extract-video-ppt, FFmpeg
- **Status**: Initial scaffold complete
- **Files**: config.py, video_summarizer.py, batch_processor.py, run_batch.bat, README.md, requirements.txt
- **Parent**: self-hosted-blog (this project)
- **Windows**: Compatible via run_batch.bat + Task Scheduler
