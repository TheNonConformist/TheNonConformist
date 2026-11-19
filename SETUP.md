# Profile setup

Live at <https://github.com/TheNonConformist/TheNonConformist>.

## What updates automatically

| Workflow | Schedule | Output |
| --- | --- | --- |
| `snake.yml` | every 12h | `output` branch → `github-snake.svg`, `github-snake-dark.svg` |
| `3d-contrib.yml` | daily 02:15 UTC | `profile-3d-contrib/*.svg` on `main` |
| `metrics.yml` | daily 02:30 UTC | `github-metrics.svg` on `main` |
| `activity.yml` | daily 02:45 UTC | recent activity block in `README.md` |

All four can be run manually:

```bash
gh workflow run snake.yml
gh workflow run 3d-contrib.yml
gh workflow run metrics.yml
gh workflow run activity.yml
```

## Secret

`METRICS_TOKEN` is a classic PAT with `repo`, `user`, `workflow` stored as an Actions secret.
Rotate it at <https://github.com/settings/tokens> and update:

```bash
gh secret set METRICS_TOKEN --repo TheNonConformist/TheNonConformist
```

## Manual checklist (UI-only)

- [ ] Pin 6 repos: profile → **Customize your pins** → Multi-Container Runtime, EP-SAD,
      Console-Based Social Network, Traffic Collector, plus two active repos.
- [ ] Profile → Edit profile → add **4 social links**, photo, location, pronouns.
- [ ] Profile → **Show Achievements** toggle on.
- [ ] Status is already set to `reading rust-lang internals`.

## Customize

- Accent color: replace `39D353` in `README.md` and `assets/terminal.svg`.
- Terminal copy: edit the `<text>` elements in `assets/terminal.svg`.
- Activity feed: `.github/recent-activity.config.yml` (`max_lines`, `disabled_events`, `ignored_repos`).
- Metrics plugins: `.github/workflows/metrics.yml`.

## Known issues

- `lowlighter/metrics`' achievements plugin currently errors because GitHub deprecated
  Projects (classic) in the GraphQL query it uses. Removed it; the static
  `native achievements — YOLO` badge links to the real Achievements tab instead.
- `github-profile-trophy` returns HTTP 402 on the public instance, so the trophy case
  was replaced with `github-profile-summary-cards`.
- Third-party cards are rate-limited by their hosts. If one breaks, retry or self-host.
