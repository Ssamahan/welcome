# welcome

The website for **Alleviating Technologies** — tech tips and tricks, hacks, trending
tech news, video games, top 10 lists, and Android and iOS customisation.

- **Live:** <https://ssamahan.github.io/welcome/>
- **YouTube:** <https://www.youtube.com/@alleviatingtechnologies>

## How this repository works

It is a static site, served straight from this repository by GitHub Pages
(`main`, root folder, HTTPS enforced). There is no build step and no dependency.

| File | What it is |
| --- | --- |
| `index.html` | The whole site — markup, styles and one small script. |
| `README.md` | This file. |

Because Pages publishes the repository root, **`index.html` is the site** and this
README is the repository's front page. They are separate files on purpose.

## Editing

Everything is in `index.html`. The styles are in the `<style>` block at the top, and
the colours are CSS variables under `:root` (`--ink`, `--gold`, `--paper`), so
changing the palette is four lines.

To change the video, replace `aMXQ_DYYo2s` in the two YouTube links and in the
thumbnail URL (`https://i.ytimg.com/vi/<ID>/maxresdefault.jpg`).

## Why it looks the way it does

This page began life as a complete HTML document pasted into `README.md`. That
mostly worked in a browser, but on GitHub it did not: Markdown sanitises HTML, so
every `style="…"` attribute was stripped, the YouTube `<iframe>` was escaped into
visible source code, and custom tags such as `<p1>` were discarded — leaving the
"p9 Copyright" line visible on the public page.

It now lives in `index.html` where that markup is valid, with three deliberate
changes:

- **A click-to-load video**, not an embedded player. An embed costs a request to
  YouTube and sets cookies before the visitor has asked for anything; the thumbnail
  costs one image and no cookie, and still links to the video.
- **Real HTML**, not invented tags. `<p1>`–`<p9>` and `</hr>` are not elements; a
  `<style>` block with classes gives the same look and actually renders.
- **A viewport meta tag**, so the page is readable on a phone instead of rendering
  zoomed-out at desktop width.

## Deploying

Push to `main`. Pages rebuilds within a minute or two. There is nothing to install.

## Licence

The text and images in this repository are © Alleviating Technologies. The
YouTube video and thumbnail belong to the channel.
