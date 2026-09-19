# Workspace Rules: Island Radio

Follow these rules on every task in this workspace.

## Source of truth
- Read `SPEC.md` before planning any task. If the spec and a request conflict, ask before changing the spec.
- `reference/prototype.html` defines the look and behavior. Do not redesign it.

## Stack limits
- Plain HTML, CSS and JavaScript (ES modules). Do not add a framework, bundler or package dependency without asking first.
- Keep the total page weight small. Do not add libraries for things the browser already does.

## Data integrity
- Never invent or guess stream URLs, frequencies or station details. If a value is unknown, leave it empty.
- Never scrape stream URLs from other websites.
- Do not edit `data/stations.json` except when I ask for a specific change.
- Do not copy another site's name, logo, artwork or text.

## Code style
- Small modules with one job each, matching the structure in `SPEC.md` section 4.
- Wrap every `localStorage` read and write in try/catch. The app must work without storage.
- No inline event handlers in HTML. No global variables outside `main.js`.
- Comment only where the reason is not obvious.

## Quality bar
- Mobile first. Test at 375px before wider sizes.
- Every interactive element is a real button or link with an accessible name and a visible focus style.
- Respect `prefers-reduced-motion`.
- Audio never autoplays. Playback starts only from a user action.

## Process
- Start each task with an implementation plan and wait for approval before large changes.
- Finish each task by running the relevant items from `SPEC.md` section 11 in the browser and attaching screenshots or a recording.
- Report anything you could not verify. Do not claim a stream works unless you actually tested it.
- Keep changes scoped to the task. Do not refactor unrelated files.
