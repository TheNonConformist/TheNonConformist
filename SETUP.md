# Setup — turn this into your GitHub profile

Everything here targets the repo **`TheNonConformist/TheNonConformist`** (a repo named exactly
like your username, public, with a `README.md` at the root — GitHub renders that on your profile).

## 1. Create the profile repo

1. Go to <https://github.com/new>.
2. Repository name: **`TheNonConformist`**.
3. Set it **Public**, tick **Add a README file**, create.
4. Delete the generated README and upload the files from this folder (`README.md`, `assets/`, `.github/`).

Using git instead:

```bash
cd github-profile
git init -b main
git remote add origin git@github.com:TheNonConformist/TheNonConformist.git
git add .
git commit -m "profile: init"
git push -u origin main
```

## 2. Enable the contribution snake

The workflow writes `github-snake.svg` and `github-snake-dark.svg` to an `output` branch.

1. Repo **Settings → Actions → General → Workflow permissions** → **Read and write permissions** → Save.
2. **Actions → Generate contribution snake → Run workflow** (or just push).
3. Wait ~1 minute. The `output` branch appears with the SVGs.
4. The `<picture>` block in `README.md` already points at those raw URLs.

If the images 404 at first, run the workflow once, then refresh.

## 3. Make the profile page itself look sharp

- **Bio**: short and concrete, e.g. `systems programmer · Rust / C · building small fast things`.
- **Status** (profile → Edit status): `reading rust-lang internals` — shows a speech bubble on your avatar.
- **Pinned repos**: pin 4–6, in this order: Multi-Container Runtime, EP-SAD, Console-Based Social Network, Traffic Collector, plus one active WIP.
- **Links**: add your site/blog if you have one; otherwise GitHub + email is enough.
- **Achievements**: optional, but the trophy case adds noise — the current README deliberately skips it.

## 4. Customize

| What | Where |
| --- | --- |
| Accent color | `39D353` → search/replace in `README.md` (stats URLs) and `assets/terminal.svg` |
| Terminal text | edit `assets/terminal.svg` (plain `<text>` elements) |
| Animation speed | `readme-typing-svg` → `pause=` and `size=` params |
| Hide private-repo counts | remove `count_private=true` (not currently set) if you don't want it |

## 5. Notes

- **Third-party cards** (`github-readme-stats`, `streak-stats`, `activity-graph`) are free public
  instances and occasionally rate-limit. If a card breaks, self-host the project or retry later.
- **Camo caching**: GitHub proxies images through Camo. After editing an SVG, changes can take a
  few minutes (sometimes a hard refresh) to show.
- **Relative asset path**: `./assets/terminal.svg` works because the asset lives in the same repo.
- The snake workflow runs twice a day; no secrets needed beyond the default `GITHUB_TOKEN`.

## Optional add-ons

Trophy case (if you want it anyway), paste under the stats section:

```html
<div align="center">
  <img src="https://github-profile-trophy.vercel.app/?username=TheNonConformist&theme=algolia&no-frame=true&no-bg=true&column=7&margin-w=8" alt="trophies" />
</div>
```

WakaTime coding stats (requires the WakaTime GitHub integration):

```html
<img src="https://github-readme-stats.vercel.app/api/wakatime?username=TheNonConformist&layout=compact&hide_border=true&bg_color=0D1117&title_color=39D353&text_color=C9D1D9" alt="wakatime" />
```
