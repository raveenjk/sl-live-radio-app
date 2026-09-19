# Island Radio: Project Spec

A fast, mobile-first web player for live Sri Lankan radio stations. One page, one player, a searchable list of stations.

Reference prototype: `reference/prototype.html` (behavior and visual direction). Treat it as the source of truth for look and feel; split it into modules but do not redesign it.

## 1. Goals

- Start listening in one tap.
- Work well on a phone first, then tablet and desktop.
- Load fast: no framework, no build step required, under 100 KB before fonts.
- Keep the station list in data, not in code.

## 2. Non-goals

- No user accounts, no ads, no analytics in v1.
- No copying of another site's branding, logo or artwork.
- No scraping of stream URLs from other sites.

## 3. Tech stack

- Plain HTML, CSS and JavaScript (ES modules). No framework.
- Data: `data/stations.json`, loaded with `fetch`. Optional later: `api/stations.php`.
- Hosting: any static host.

## 4. File structure

```
island-radio/
  index.html
  css/
    base.css        tokens, reset, typography
    player.css      header, carousel, controls
    browse.css      search, filters, grid, empty state
  js/
    main.js         boot, wiring
    player.js       audio state machine
    carousel.js     snap scroll, drag, active sync
    browse.js       search, filters, grid render
    store.js        localStorage wrapper (try/catch, safe fallback)
  data/
    stations.json
  scripts/
    check-streams.js
  pages/
    privacy.html
    download.html
  reference/
    prototype.html
  SPEC.md
```

## 5. Data model

`data/stations.json`:

```json
[
  {
    "id": "example",
    "name": "Example FM",
    "lang": "Sinhala",
    "freq": "00.0",
    "url": "https://example.com/stream",
    "logo": null
  }
]
```

Rules:
- `id`: unique, lowercase, no spaces.
- `lang`: one of `Sinhala`, `Tamil`, `English`.
- `freq`: optional string. Leave empty if unknown. Never guess.
- `url`: `https` stream (MP3, AAC or HLS). Empty string means "not configured".
- `logo`: optional path. If null, show generated initials on a colored tile.

## 6. Layout

1. **Header:** brand, "Live now" badge (pulses only while playing), app download button.
2. **Player:**
   - Horizontal carousel of station tiles with a fixed center needle.
   - Hint text: "Drag or swipe to browse stations".
   - Status line, station name (H1), meta line (Live • Language • Frequency), HD badge.
   - Controls: previous, play/pause, next. Volume slider.
3. **Browse:**
   - Search input with `Ctrl/⌘ K` hint.
   - Filter buttons: All, Sinhala, Tamil, English.
   - Heading "All radio stations", station count, responsive grid of cards.
   - Empty state: "No stations found" with a "Show all stations" button.
4. **Footer:** copyright, privacy link, tagline.

## 7. Behavior

### Player states
`idle` → `connecting` → `playing` ↔ `buffering`, with `error` reachable from any state.

| State | Status text | UI |
|---|---|---|
| idle | Ready to play | play icon |
| connecting | Connecting… | play icon |
| playing | Now playing | pause icon, live badge pulses |
| buffering | Buffering… | pause icon |
| error | Stream unavailable right now | play icon, error color |
| no stream | No stream URL set for this station yet | play icon, error color |

- Pausing must release the stream (clear `src`) so live audio does not keep buffering.
- On error, retry once automatically after 2 seconds, then stay in `error`.
- Changing station while playing switches stream immediately.
- Changing station while paused only updates the UI.

### Carousel
- Scroll-snap, centered active tile. Active tile is full size and opacity; others are scaled down and dimmed.
- Active station is determined by the tile closest to center after scrolling settles.
- Mouse drag works on desktop; touch swipe works natively.
- Clicking a tile selects it and centers it.
- Page glow color follows the active station's hue.

### Browse
- Search matches name, language and frequency, case-insensitive.
- Search and language filter combine.
- Selecting a card selects the station, starts playback if it has a URL, and scrolls to the player.
- Count reads "1 station" / "N stations".

### Persistence
- Save last station id and volume in `localStorage`. Every read and write is wrapped in try/catch. The app must work when storage is empty or blocked.

### Keyboard
- `Ctrl/⌘ K`: focus search.
- `Space`: play/pause (ignored while typing).
- `←` / `→`: previous / next station.

### Media Session
- Set title, artist ("Live radio"), and handlers for play, pause, previous, next.

## 8. Visual design

- Dark theme. Background `#03070d`, surface `#0b131d`, raised surface `#111c29`, line `#1c2a3a`.
- Accent amber `#ffb02e` for the play button, focus ring, active card border and needle.
- Live indicator red `#ff4d5e`.
- Fonts: Bricolage Grotesque (headings), Figtree (body), each with a system fallback stack.
- Station tiles: rounded squares, gradient from the station hue.
- Motion: only the live pulse and tile scale on selection. Respect `prefers-reduced-motion`.

## 9. Accessibility

- All controls are real buttons with accessible names.
- Visible focus ring on every interactive element.
- Status line uses `aria-live="polite"`.
- Text contrast at least 4.5:1.
- Everything reachable and usable by keyboard.

## 10. Performance

- No blocking scripts; use `type="module"`.
- Font loading with `display=swap`.
- Audio `preload="none"`.
- No layout shift when the station list loads (reserve space for the grid).

## 11. Acceptance checklist

The browser agent should verify each item and attach screenshots or a recording.

- [ ] Layout is correct at 375px, 768px and 1280px, with no horizontal page scroll.
- [ ] Selecting a station updates title, meta line, active tile and active card.
- [ ] Play, pause, next and previous work; state text matches the table in section 7.
- [ ] A station with no URL shows the "No stream URL" message and does not crash.
- [ ] Search "hiru" returns matching stations only; nonsense text shows the empty state; the reset button restores everything.
- [ ] Filters and search combine correctly.
- [ ] `Ctrl/⌘ K`, Space and arrow keys work.
- [ ] Reload restores the last station and volume.
- [ ] The page works with `localStorage` disabled.
- [ ] Lighthouse: Accessibility ≥ 95, Performance ≥ 90 on mobile.

## 12. Stream handling notes

- Browsers block `http://` audio on an `https` page (mixed content). Prefer `https` streams; if a station only offers `http`, note it in `stations.json` rather than adding a workaround silently.
- Audio starts only after a user gesture. Never try to autoplay.
- `scripts/check-streams.js` reads `stations.json`, requests each `url`, and prints status, content type and response time. It must never modify the data file.

## 13. Build order

1. Scaffold structure and load stations from JSON.
2. Player core (`player.js`) and controls.
3. Carousel and browse (can run in parallel).
4. Polish: persistence, Media Session, accessibility.
5. Stream checker script, privacy and download pages.
6. Deploy.
