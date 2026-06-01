# MEMORY — Self-Hosted Blog

## Metadata

- **Project**: self-hosted-blog
- **Parent**: Develop
- **Type**: static site / blog
- **Status**: live
- **Stack**: Hugo + PaperMod theme

## Stack

- **Framework**: Hugo v0.162.1 (extended)
- **Theme**: [PaperMod](https://github.com/adityatelange/hugo-PaperMod) (git submodule)
- **Deploy**: GitHub Pages via GitHub Actions

## Repository

- **URL**: https://github.com/Hsin-Liu/self-hosted-blog
- **Branch**: main
- **Workflow**: `.github/workflows/gh-pages.yml`

## GitHub Pages Setup (Manual)

1. Go to repo **Settings → Pages**
2. Source: **GitHub Actions** (not Branch)
3. Workflow will auto-run on every push to `main`

## Content

- Posts: `content/posts/*.md`
- Drafts: `hugo server --buildDrafts`
- Build: `hugo --gc --minify`

## Notes

- `public/` is gitignored — built by GitHub Actions
- `themes/PaperMod` is a git submodule
