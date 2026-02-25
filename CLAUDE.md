# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Academic personal website for Shengyao Zhuang, built with Jekyll using the Minimal Mistakes theme (forked from academicpages). Hosted on GitHub Pages at https://arvinzhuang.github.io.

## Build & Development Commands

```bash
# Install Ruby dependencies
bundle install

# Local development with live reload
bundle exec jekyll liveserve

# Minify JavaScript (requires Node.js)
npm run build:js

# Watch JS for changes during development
npm run watch:js
```

Note: `_config.yml` is NOT reloaded by `jekyll serve` — restart the server after config changes. Dev overrides live in `_config.dev.yml`.

## Architecture

**Jekyll static site** with these collections (each in its own `_` directory):

- **`_publications/`** — Academic papers (primary content, 35+ entries). Displayed on the homepage grouped by year.
- **`_talks/`** — Conference presentations
- **`_teaching/`** — Course information
- **`_portfolio/`** — Project showcases
- **`_posts/`** — Blog posts (mostly template examples)

**Key directories:**
- `_pages/` — Top-level site pages (`about.md` is the homepage via `permalink: /`)
- `_layouts/` — Liquid HTML templates
- `_includes/` — Reusable Liquid components
- `_sass/` — SCSS stylesheets (Minimal Mistakes theme)
- `_data/navigation.yml` — Site navigation menu
- `files/` — Downloadable PDFs
- `images/` — Image assets
- `markdown_generator/` — Python scripts/Jupyter notebooks to generate collection markdown from TSV or BibTeX

## Publication Front Matter Format

Files in `_publications/` follow the naming pattern `YYYY-VENUE-SHORTNAME.md`:

```yaml
---
title: "Paper Title"
collection: publications
permalink: /publication/venue2024shortname
year: 2024
venue: 'Full Venue Name'
authors: First Author, <strong>Shengyao Zhuang</strong>, and Last Author.
track: Short paper
---
```

The `<strong>` tag around the site author's name is a convention used across all publication entries. The homepage (`_pages/about.md`) renders publications sorted by year in reverse chronological order using Liquid.

## Markdown Generators

`markdown_generator/` contains Python scripts and Jupyter notebooks for batch-creating collection entries:
- `publications.py` / `publications.ipynb` — Generate from `publications.tsv`
- `talks.py` / `talks.ipynb` — Generate from `talks.tsv`
- `pubsFromBib.py` / `PubsFromBib.ipynb` — Generate from BibTeX files

## Deployment

Push to `master` branch — GitHub Pages builds and deploys automatically.
