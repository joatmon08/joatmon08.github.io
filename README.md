# Rosemary Wang — Personal Website

Single-page portfolio built with [Jekyll](https://jekyllrb.com/) and hosted on [GitHub Pages](https://pages.github.com/) at [joatmon08.com](https://joatmon08.com).

## Publishing changes

Edit markdown content, commit, and push to `main`. GitHub Pages builds the site automatically — no local build step required.

```bash
git add _includes/content/talks.md
git commit -m "Add new talk"
git push
```

## Editing content

All content lives in markdown files under `_includes/content/`:

| File | Section |
|------|---------|
| `about.md` | About bio and speaker info |
| `writing.md` | Books, articles, podcasts, interviews, hosted shows |
| `talks.md` | Upcoming and past speaking engagements |

### Add an article

Open `_includes/content/writing.md` and add a line under `### Articles`:

```markdown
- [Article Title](https://example.com/article)
```

### Add an upcoming talk

In `_includes/content/talks.md`, find the **Upcoming** block wrapped in `<!-- ... -->`. Remove the comment markers, add your row(s), and save:

```markdown
### Upcoming

| Date | Event | Location |
|------|-------|----------|
| 06.03.2026 | Women Who Code Summit — My Talk | [New York, NY](https://events.example.com) |
```

When you have no upcoming talks, wrap that section in `<!--` and `-->` again so it stays hidden.

### Add a past talk

Open `_includes/content/talks.md` and add a row at the top of the **Past Talks** table (newest first):

```markdown
| 01.15.2026 | Conference Name — Talk Title | [Slides](https://speakerdeck.com/...) |
```

The table has three columns: **Date**, **Event** (conference and talk title), and **Links**.

Link labels: `Slides` for slide decks, `Demo` for GitHub links, `Recording` for YouTube or HashiCorp links. Separate multiple links with ` · `:

```markdown
| 01.15.2026 | Meetup — My Talk | [Slides](url) · [Demo](https://github.com/...) · [Recording](https://www.youtube.com/...) |
```

If a title contains a pipe character, escape it: `Episode 32 \| Part 2`.

### Site settings and social links

Edit `_config.yml` for site title, tagline, and social profile URLs.

## Local preview

Native `bundle install` may fail on macOS if C++ build tools cannot compile Jekyll's dependencies. Use Docker instead (Docker Desktop must be running):

```bash
./preview.sh
```

Open [http://localhost:4000](http://localhost:4000). Press `Ctrl+C` to stop.

The preview uses LiveReload and file polling so edits should rebuild automatically. **Restart preview after changing `preview.sh` or `_config.yml`.**

**If the browser does not update after you save:**

1. Watch the terminal for `Regenerating:` after you save a file (may take a few seconds on macOS).
2. Hard-refresh the browser (`Cmd+Shift+R`).
3. Restart preview: `Ctrl+C`, then `./preview.sh` again.

The preview uses the same `github-pages` gem that GitHub Pages runs in production.

### Alternative: Homebrew Ruby (if gems install successfully)

If you have Homebrew Ruby 3+ and a working native toolchain:

```bash
export PATH="/usr/local/opt/ruby/bin:$PATH"
bundle install
bundle exec jekyll serve
```

## License

See [LICENSE.md](LICENSE.md).
