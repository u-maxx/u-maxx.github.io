# GitHub Copilot Instructions

See [COPILOT.md](../COPILOT.md) for full project documentation.

## Quick Rules for Copilot Agent

1. **Edit styles only in `input.css`** — never touch the `<style id="inline-css">` block in `index.html`; it is auto-generated.
2. **Use Tailwind CSS utilities** in HTML markup. Only create custom classes in `input.css` for complex, reusable, or animation-based styles.
3. **Run `npm run build`** after any change to `input.css` or after adding new Tailwind classes to `index.html`. This compiles Tailwind and inlines the CSS.
4. **Mobile-first responsive design** — write mobile styles first (unprefixed), then add `sm:` (≥640px), `md:` (≥768px), `lg:` (≥1024px) overrides.
5. **No inline `style="..."` attributes** unless absolutely unavoidable. Prefer Tailwind utilities or custom classes in `input.css`.
6. **Design tokens**: background is `--color-bg-dark` (#090614), accent is `--color-neon-green` (#8eff7a). Fonts: Orbitron (`.font-retro`) for headings/buttons, Space Grotesk (default) for body.
7. The site is a **single static HTML page** with no JS framework. Keep it that way.
8. The Husky pre-commit hook auto-runs the build, but always build manually first to verify.

