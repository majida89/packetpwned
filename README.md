# packetpwned.com

Personal security blog and TryHackMe writeups by Majid Ahmed (CCIE #55880 | CISSP).

## Stack
- **Hugo** — static site generator
- **GitHub Pages** — free hosting
- **Namecheap** — domain registrar

## Local Development

```bash
# Install Hugo (Windows)
winget install Hugo.Hugo.Extended

# Run local dev server
hugo server -D

# Visit http://localhost:1313
```

## Creating a New Writeup

```bash
hugo new writeups/room-name.md
```

Edit the file in `content/writeups/room-name.md`, set `draft: false` when ready to publish.

## Deploy

Push to `main` branch → GitHub Actions auto-builds and deploys to GitHub Pages.

## Folder Structure

```
packetpwned/
├── content/
│   ├── writeups/     ← TryHackMe writeups
│   ├── projects/     ← Engineering projects
│   ├── blog/         ← General posts
│   └── about.md      ← About page
├── layouts/          ← HTML templates
├── static/css/       ← Stylesheet
├── archetypes/       ← Post templates
└── hugo.toml         ← Site config
```
