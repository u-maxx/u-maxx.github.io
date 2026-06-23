# Agent Guide: Max Uroda Portfolio

Welcome. This guide explains how to work with this repository and use the built-in automation tools.

## Tech Stack
- **Frontend:** HTML5, Tailwind CSS v4 (Alpha/Beta).
- **Styles:** Custom `input.css` processed by a custom Node.js build script.
- **Automation:** Python (using Playwright and BeautifulSoup4) for data scraping and HTML injection.
- **Environment:** `npm` for Node.js, `uv` for Python.

## Core Rules
- **Design:** Follow the retro-terminal aesthetic. Use glass-morphism panels, neon-green accents, and grayscale-to-color transitions for interactive elements.
- **Build Artifacts:** Do **NOT** edit `dist/styles.css` directly. Always modify `input.css` and run `npm run build`.
- **Layout:** Follow the mobile-first grid layout and z-index layering defined in `COPILOT.md`.

## Automation Scripts
Located in the `scripts/` directory:
- `import_linkedin.py`: Fetches professional recommendations from LinkedIn.
  - It supports live scraping (Playwright).
  - It supports local HTML parsing if `recommendations.html` exists in the root.
  - It automatically updates `scripts/reviews.json` and injects HTML into `index.html`.

## Development Workflow
1. **Python Setup:**
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install playwright beautifulsoup4 lxml
   playwright install chromium
   ```
2. **Node.js Setup:**
   ```bash
   npm install
   ```
3. **Updating Content:**
   - Modify `index.html` for structural changes.
   - Run `python scripts/import_linkedin.py` to sync recommendations.
4. **Building Styles:**
   ```bash
   npm run build
   ```

## Verification
Use the Playwright script in `verification/` (if available) to capture screenshots of UI changes and ensure responsiveness.
