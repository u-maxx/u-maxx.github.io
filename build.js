#!/usr/bin/env node
/**
 * build.js — Production build script
 *
 * 1. Runs Tailwind CSS to compile input.css → dist/styles.css
 * 2. Inlines the compiled CSS into index.html as a <style> block
 *    (eliminates the render-blocking CSS request from the critical path)
 *
 * Font URLs in input.css already use dist/fonts/ paths so they resolve
 * correctly when inlined into index.html at the project root.
 *
 * This reduces the critical request chain from 3 hops (HTML→CSS→Fonts)
 * to 1 hop (HTML→Fonts via preload), cutting ~330ms off LCP.
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const root = __dirname;
const htmlPath = path.join(root, 'index.html');
const cssPath = path.join(root, 'dist', 'styles.css');

// Step 1: Build Tailwind CSS
console.log('⚙️  Building CSS with Tailwind…');
execSync('npx @tailwindcss/cli -i input.css -o dist/styles.css --minify', {
  cwd: root,
  stdio: 'inherit',
});

// Step 2: Read files
let html = fs.readFileSync(htmlPath, 'utf8');
const css = fs.readFileSync(cssPath, 'utf8');

// Step 3: Inline CSS — replace either an existing <style id="inline-css"> block
//         or the external <link> tag
const existingStyle = /<style id="inline-css">[\s\S]*?<\/style>/;
const linkTag = /<link\s+href=["']dist\/styles\.css["']\s+rel=["']stylesheet["']\s*\/?>/;

const inlineBlock = `<style id="inline-css">${css}</style>`;

if (existingStyle.test(html)) {
  html = html.replace(existingStyle, inlineBlock);
} else if (linkTag.test(html)) {
  html = html.replace(linkTag, inlineBlock);
} else {
  console.error('ERROR: Could not find CSS link or inline style block in index.html');
  process.exit(1);
}

fs.writeFileSync(htmlPath, html, 'utf8');
console.log('✅ CSS inlined into index.html');

