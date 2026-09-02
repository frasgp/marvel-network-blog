# Marvel Graph Lab

A weekly Quarto blog for course 02805 (Social Graphs and Interactions) assignment 1.8, "Go nuts
with your LLM." Each week's post mines that week's release of the shared Marvel Comics character
network.

## Prerequisites

- [Quarto CLI](https://quarto.org/docs/get-started/) (`brew install --cask quarto`, or the
  official installer). If `brew install --cask` fails asking for a sudo password in a
  non-interactive shell, grab the no-install tarball instead:
  ```sh
  curl -sL -o quarto.tar.gz "https://github.com/quarto-dev/quarto-cli/releases/download/v1.10.18/quarto-1.10.18-macos.tar.gz"
  mkdir -p ~/.local/opt ~/.local/bin
  tar xzf quarto.tar.gz -C ~/.local/opt
  ln -sf ~/.local/opt/bin/quarto ~/.local/bin/quarto
  export PATH="$HOME/.local/bin:$PATH"   # add to ~/.zshrc to make permanent
  ```
- Python 3.10+

## Setup

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Preview locally

```sh
quarto preview
```

Live-reloads in your browser as you edit.

## Full build

```sh
quarto render
```

Outputs the static site to `_site/` (gitignored). In production this is built and published
automatically by `.github/workflows/publish.yml` on every push to `main`.

## Repo layout

```
_quarto.yml       site/navbar config, theme
styles.scss       visual identity
index.qmd         homepage — auto-lists every post in posts/
about.qmd         about page + credits
posts/<slug>/     one folder per weekly post
  index.qmd       the post itself
  data/           that week's dataset release (TSVs, etc.)
```

## Adding next week's post

1. Copy `posts/_template/` to `posts/2026-weekNN-<slug>/` (drop the leading underscore — that's
   what tells Quarto to render it and the homepage to list it).
2. Drop that week's dataset files into its own `data/` subfolder.
3. Update the front matter (`title`, `date`, `categories`) and write the post.

The homepage listing picks up new posts automatically — no other file needs editing. Pushing to
`main` publishes it live within a few minutes.

## Credits

See [`about.qmd`](about.qmd) — fill in the `[Your names here]` placeholder.

## License

MIT — see [`LICENSE`](LICENSE).
