# Blog

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

## Micro-posts

A second content type for short, tweet-style notes — distinct from long-form `posts/`.

- Location: `content/micros/<slug>.md`
- Scaffold: `hugo new micros/<slug>.md` (uses `archetypes/micro.md`)
- URL: `/micros/<slug>/`
- Listing: `/micros/`
- Front matter is auto-set to suppress cover, reading time, word count, and author — only the date is shown. Author may add `tags = [...]` and override any field.
- Micro-posts share the same `tags` taxonomy as long posts (no separate taxonomy).
- Micro-posts ARE included in the main `/index.xml` RSS feed. To exclude one, set `hiddenInRss: true` in its front matter.
- The home page surfaces the latest 5 micros in a sidebar widget (`layouts/_partials/micro-sidebar.html`).
- The top nav has a "Micros" entry declared in `hugo.toml` under `[[menu.main]]`.

## Images

Two patterns supported. Pick by scope.

- **One post only → page bundle.** Convert the post to a directory + `index.md` and place images next to it. Reference with a **relative path** (e.g. `![Figure](figure.png)`). Hugo can process these via `.Resources.GetMatch`.
- **Shared across posts → `static/`.** Drop the file under `static/images/...`. Reference with a **site-root path** (e.g. `![Logo](/images/site-logo.png)`). No image processing.
- Cover image in front matter accepts either: `image = "cover.jpg"` (page bundle, relative) or `image = "/images/cover.jpg"` (static, root-relative).
- Micros have `cover.hidden = true` by default, so the `cover.image` field is a no-op for them — use a page bundle and reference the image inline with a relative path if needed.
- `public/` and `resources/_gen/` (image-processing cache) are gitignored; safe to delete.

## Parent

Part of the [parent project](../CLAUDE.md).