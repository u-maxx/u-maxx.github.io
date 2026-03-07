# Copilot Agent Instructions — maxuroda.pro

## Project Overview

Personal portfolio / landing page for **Maksym Uroda** (Senior AI Engineer).
Hosted on **GitHub Pages** at `https://maxuroda.pro`.
Single-page static site with a retro terminal / neon-green-on-dark aesthetic.

---

## Tech Stack

| Layer        | Technology                                        |
| ------------ | ------------------------------------------------- |
| CSS          | **Tailwind CSS v4** (`@tailwindcss/cli`)           |
| Fonts        | Self-hosted **Orbitron** + **Space Grotesk** (woff2) |
| Build        | `node build.js` (Tailwind compile → inline CSS)   |
| Pre-commit   | **Husky** runs `npm run build` automatically       |
| Hosting      | GitHub Pages (static `index.html`)                |

There is **no JavaScript framework** — the site is plain HTML + Tailwind CSS.

---

## File Map

```
├── index.html        ← The one and only page. Contains ALL markup + inline <style> block.
├── input.css         ← ⭐ SOURCE OF TRUTH for all CSS. Edit styles HERE, never in index.html.
├── build.js          ← Build script: compiles input.css → dist/styles.css, then inlines it into index.html.
├── package.json      ← npm scripts: build, build:css, watch:css.
├── dist/
│   ├── styles.css    ← Compiled Tailwind output (auto-generated, committed).
│   └── fonts/        ← Self-hosted .woff2 font files.
├── .husky/pre-commit ← Runs `npm run build && git add dist/styles.css index.html` before every commit.
├── CNAME             ← Custom domain: maxuroda.pro
└── COPILOT.md        ← This file.
```

---

## ⚠️ Critical Rules

### 1. All styles go in `input.css`

**Never** edit the `<style id="inline-css">` block inside `index.html` directly.
That block is **auto-generated** by `build.js` and will be overwritten on the next build.

- Custom classes (`.text-neon`, `.btn-neon`, `.glass-panel`, etc.) → define in `input.css`
- Tailwind utility classes (`px-4`, `sm:text-2xl`, etc.) → just use them in `index.html` markup; Tailwind scans the HTML and generates them automatically
- If a Tailwind utility class is missing from the compiled output after build, **do not** manually add it to `input.css` as a hand-written rule. Instead, ensure the class name is present in `index.html` markup so Tailwind's scanner picks it up, then re-run the build.

### 2. Always run the build after changes

```bash
npm run build
```

This does two things:
1. `npx @tailwindcss/cli -i input.css -o dist/styles.css --minify` — compiles Tailwind
2. Inlines the compiled CSS into `index.html`'s `<style id="inline-css">` block

The Husky pre-commit hook runs this automatically, but you should still build manually to verify changes before committing.

### 3. Use Tailwind CSS utility classes first

Prefer Tailwind utility classes in HTML markup over writing custom CSS in `input.css`.
Only create custom classes in `input.css` when:
- The style is complex (multi-property) and reused across multiple elements
- The style involves `@keyframes` animations
- The style can't be expressed as a Tailwind utility (e.g., custom background patterns)

### 4. Mobile-first responsive design

The site **must** look great on phones, tablets, and desktops. Follow Tailwind's mobile-first breakpoint system:

| Prefix | Min-width | Target              |
| ------ | --------- | ------------------- |
| (none) | 0         | Mobile (default)    |
| `sm:`  | 40rem     | Large phones / small tablets |
| `md:`  | 48rem     | Tablets             |
| `lg:`  | 64rem     | Desktops            |

Always write the **mobile style first** (unprefixed), then layer on `sm:`, `md:`, `lg:` overrides.

Example: `class="text-2xl sm:text-3xl md:text-5xl lg:text-6xl"`

### 5. No inline styles unless absolutely necessary

Avoid `style="..."` attributes on HTML elements. If an inline style exists, it's likely a workaround — prefer moving it to a proper class in `input.css` or using a Tailwind utility.

---

## Design System

### Color Palette

| Token               | Value      | Usage                           |
| -------------------- | ---------- | ------------------------------- |
| `--color-bg-dark`    | `#090614`  | Page background, footer bg      |
| `--color-neon-green` | `#8eff7a`  | Accent color, headings, borders |
| White / gray-100     | `#fff`     | Primary body text               |
| gray-300             | (Tailwind) | Secondary text (skill items)    |

### Fonts

| Font           | CSS variable   | Usage                        |
| -------------- | -------------- | ---------------------------- |
| Space Grotesk  | `--font-space` | Body text (default)          |
| Orbitron       | `--font-retro` | Headings, buttons, footer    |

Use `font-retro` class for Orbitron. Body text uses Space Grotesk by default.

### Custom CSS Classes (defined in `input.css`)

| Class               | Purpose                                            |
| -------------------- | -------------------------------------------------- |
| `.text-neon`         | Neon green text with glow `text-shadow`             |
| `.btn-neon`          | Button border + hover effect (green bg, lift, glow) |
| `.glass-panel`       | Frosted glass card (dark bg, blur, green border)    |
| `.bg-grid-wall`      | Fixed 2D grid background pattern                    |
| `.bg-grid-floor`     | Fixed 3D perspective floor grid                     |
| `.floor-fade`        | Gradient that fades floor grid into background      |
| `.scanlines`         | CRT scanline overlay (fixed, pointer-events: none)  |
| `.cursor-blink`      | Blinking terminal cursor animation (█)              |
| `.animate-grid-flow` | Continuously scrolling grid background              |
| `.animate-pulse-neon`| Pulsing neon text-shadow glow                       |
| `.skill-item`        | Hover effect for skill list items (slide + glow)    |

### Animations (defined in `input.css`)

| Keyframes      | Used by              | Effect                         |
| -------------- | -------------------- | ------------------------------ |
| `blink`        | `.cursor-blink`      | Terminal cursor on/off          |
| `grid-move`    | `.animate-grid-flow` | Floor grid scrolls vertically   |
| `neon-pulse`   | `.animate-pulse-neon`| Text shadow pulses brighter     |

---

## Page Structure

```
body
├── .bg-grid-wall          (fixed background: 2D grid)
├── .bg-grid-floor         (fixed background: 3D floor grid + animation)
├── .floor-fade            (fixed gradient overlay for floor)
├── .scanlines             (fixed CRT scanline overlay)
├── footer bar             (fixed bottom, dark bg, green text + top border)
└── main                   (z-10, centered content)
    ├── h1                 (name + title with blinking cursor)
    ├── .glass-panel       (bio paragraph + skills list)
    └── buttons            (GitHub, Book a Call, LinkedIn, Certifications, X.com, Get in Touch)
```

### Z-index Layers

| z-index | Element                |
| ------- | ---------------------- |
| 0       | Grid backgrounds       |
| 1       | Floor fade             |
| 10      | Main content           |
| 40      | Scanlines overlay      |
| 50      | Footer bar             |

---

## Button Hierarchy

- **Primary CTA**: "Book a Call" — has solid neon-green border (`border-color: var(--color-neon-green)`) and `font-bold`
- **Secondary**: All other buttons — standard `.btn-neon` styling with subtle border

All buttons use: `.btn-neon .border .border-solid .rounded-full .font-retro .uppercase .tracking-widest`

On hover, all buttons get the same green background + dark text treatment.

---

## Development Workflow

```bash
# Install dependencies
npm install

# Watch mode (auto-recompile CSS on changes, but does NOT inline)
npm run watch:css

# Full production build (compile + inline into index.html)
npm run build

# The pre-commit hook runs `npm run build` automatically
```

### When adding a new Tailwind class to HTML:
1. Add the class to the element in `index.html`
2. Run `npm run build`
3. The Tailwind CLI scans `index.html`, generates the needed utility, compiles it, and inlines it

### When adding a new custom class:
1. Define the class in `input.css`
2. Use it in `index.html`
3. Run `npm run build`

---

## Performance Notes

- CSS is **inlined** into `index.html` to eliminate a render-blocking request
- Fonts are **preloaded** via `<link rel="preload">` in the `<head>`
- Font files are **self-hosted** (no external Google Fonts requests)
- The critical rendering path is: HTML → Fonts (1 hop instead of HTML → CSS → Fonts)

