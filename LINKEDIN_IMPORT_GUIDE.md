# LinkedIn Recommendations Import Guide

This guide explains how to update the portfolio's recommendations section with all your latest LinkedIn data.

## Option 1: Automated Local Import (Recommended)

Since the cloud environment is often blocked by LinkedIn's security walls, the best way to get **all** your recommendations is to run the script locally while you are logged in.

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Steps
1. **Save the Recommendations Page:**
   - Log in to LinkedIn.
   - Go to your recommendations page: [https://www.linkedin.com/in/max-uroda/details/recommendations/](https://www.linkedin.com/in/max-uroda/details/recommendations/)
   - Right-click anywhere and select **Save As...**
   - Save the file as `recommendations.html` in the root of this project.

2. **Run the Import Script:**
   ```bash
   # If using uv:
   uv venv
   source .venv/bin/activate # or .venv\Scripts\activate on Windows
   uv pip install playwright beautifulsoup4 lxml
   playwright install chromium
   python scripts/import_linkedin.py
   ```

3. **Rebuild the Site:**
   ```bash
   npm install
   npm run build
   ```

## Option 2: Fallback
If you cannot run the script locally, the project defaults to a set of 4 recommendations previously captured via screenshots.

## Files Updated
- `reviews.json`: The data store for all recommendations.
- `index.html`: The frontend UI is automatically updated with new entries.
