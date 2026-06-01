# Self-Hosted Blog

> A personal blog built with Hugo + PaperMod, deployed to GitHub Pages via GitHub Actions.

## Stack

- **Generator**: Hugo v0.162.1 (extended)
- **Theme**: [PaperMod](https://github.com/adityatelange/hugo-PaperMod) (git submodule at `themes/PaperMod`)
- **Hosting**: GitHub Pages
- **CI**: GitHub Actions (`.github/workflows/gh-pages.yml`)
- **Content**: Markdown + TOML front matter, LaTeX (KaTeX) via Goldmark passthrough

## Where to Look

- [`README.md`](README.md) — setup, content workflow, troubleshooting
- [`hugo.toml`](hugo.toml) — site config
- [`content/posts/`](content/posts/) — blog posts
- [`archetypes/default.md`](archetypes/default.md) — front-matter template
- [`layouts/`](layouts/) — local theme overrides (wins over `themes/PaperMod/`)
- [`themes/PaperMod/`](themes/PaperMod/) — git submodule; **do not edit directly**

## Conventions

- Front matter is **TOML** (`+++` blocks). Use `draft = true` while iterating.
- Add `math = true` to a post's front matter to enable KaTeX rendering.
- Override theme files by copying into `layouts/` — never edit `themes/PaperMod/` (submodule, edits are lost on update).
- `public/` and `resources/_gen/` are gitignored; never commit them.
- Match the Hugo version in `.github/workflows/gh-pages.yml` locally so previews match CI.

## Common Commands

- `hugo server --buildDrafts` — local preview with drafts visible
- `hugo new posts/<slug>.md` — scaffold a new post from the archetype
- `hugo --gc --minify` — production build (matches what CI runs)

## Deployment

Pushing to `main` runs `.github/workflows/gh-pages.yml`, which builds and deploys to GitHub Pages. **Source** in repo Settings → Pages must be set to *GitHub Actions* (not a branch).

## Parent

Part of the [parent project](../CLAUDE.md).