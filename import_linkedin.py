import asyncio
import json
import os
import re
from playwright.async_api import async_playwright

# Data extracted from the screenshot to be used as a template/fallback
SCREENSHOT_DATA = [
  {
    "name": "Maksym Lakhman",
    "role": "AQA Software Engineer",
    "date": "March 15, 2024",
    "connection": "worked with Maksym on the same team",
    "text": "Maxym is an excellent specialist with strong communication skills and technical expertise. experienced Magento/Adobe Commerce developer, capable of investigating deep issues and a good teammate.",
    "avatar": "https://media.licdn.com/dms/image/v2/D4E03AQG_Q9yQW6v_Sg/profile-displayphoto-shrink_100_100/0/1710188647087?e=1724889600&v=beta&t=example1",
    "linkedin": "https://www.linkedin.com/in/maksym-lakhman"
  },
  {
    "name": "J Flacks",
    "role": "Technical Lead at Innox Trading Ltd t/a chemist-4-u.com",
    "date": "February 22, 2024",
    "connection": "managed Maksym directly",
    "text": "Max worked with us to help improve the uncached performance of many of our key pages. identified inefficiencies and helped us implement fixes to serve pages much faster. Max is a fantastic developer with a great understanding of Magento 2.",
    "avatar": "https://media.licdn.com/dms/image/v2/D4D03AQE_E_example/profile-displayphoto-shrink_100_100/0/1700000000000?e=1724889600&v=beta&t=example2",
    "linkedin": "https://www.linkedin.com/in/jflacks"
  },
  {
    "name": "Matias Hidalgo",
    "role": "Magento Tech Lead and SRE at McFadyen / 7x Magento Certified",
    "date": "November 15, 2023",
    "connection": "worked with Maksym but on different teams",
    "text": "He is a kind guy to work with, always open to listen and help others, he really knows Adobe Commerce and undertand his complex architecture.",
    "avatar": "https://media.licdn.com/dms/image/v2/D4E03AQG_example/profile-displayphoto-shrink_100_100/0/1700000000000?e=1724889600&v=beta&t=example3",
    "linkedin": "https://www.linkedin.com/in/matiashidalgo"
  },
  {
    "name": "Martin Arrua",
    "role": "eCommerce Specialist",
    "date": "November 4, 2023",
    "connection": "worked with Maksym on the same team",
    "text": "Max is a highly talented and dedicated software engineer. I had the pleasure of working with with Max a couple of years ago, and I am continually impressed by his technical expertise, ethic, and professionalism. Max is a brilliant software engineer with a deep understanding of programming languages, algorithms, and software design principles. His ability to solve complex problems and write clean code is truly commendable.",
    "avatar": "https://media.licdn.com/dms/image/v2/C4E03AQF_example/profile-displayphoto-shrink_100_100/0/1700000000000?e=1724889600&v=beta&t=example4",
    "linkedin": "https://www.linkedin.com/in/martinarrua"
  }
]

def parse_recommendations_html(html_content):
    """
    Parses LinkedIn recommendations from HTML content using BeautifulSoup.
    """
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'lxml')
    items = soup.select(".artdeco-list__item")

    scraped_data = []
    for item in items:
        name_elem = item.select_one(".t-bold span[aria-hidden='true']")
        role_elem = item.select_one(".t-14.t-black--light.t-normal")
        date_elem = item.select_one(".t-12.t-black--light.t-normal")
        text_elem = item.select_one(".inline-show-more-text")
        link_elem = item.select_one("a[data-field='recommendation_author_origin_url']")
        img_elem = item.select_one("img")

        if name_elem:
            name = name_elem.get_text().strip()
            role = role_elem.get_text().strip() if role_elem else ""
            date = date_elem.get_text().strip() if date_elem else ""
            # Handle text content which might be inside multiple spans
            text = text_elem.get_text().strip() if text_elem else ""
            profile_link = link_elem.get("href") if link_elem else ""
            image_url = img_elem.get("src") if img_elem else ""

            scraped_data.append({
                "name": name,
                "role": role,
                "date": date,
                "text": text.replace("...see more", "").replace("\n", " ").strip(),
                "linkedin": profile_link if profile_link.startswith("http") else f"https://www.linkedin.com{profile_link}",
                "avatar": image_url
            })
    return scraped_data

async def scrape_linkedin_recommendations(profile_url):
    print(f"🚀 Attempting to scrape live data from {profile_url}...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        )
        page = await context.new_page()

        try:
            target_url = profile_url.rstrip('/') + "/details/recommendations/"
            await page.goto(target_url, wait_until="networkidle", timeout=15000)

            if "login" in page.url or "signup" in page.url:
                print("⚠️ LinkedIn Auth Wall encountered. Scraper blocked.")
                return None

            await page.wait_for_selector(".artdeco-list__item", timeout=5000)
            content = await page.content()
            return parse_recommendations_html(content)
        except Exception as e:
            print(f"❌ Scraper error: {e}")
            return None
        finally:
            await browser.close()

def update_html_with_reviews(reviews):
    """
    Updates index.html with the latest reviews data.
    """
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Generate the HTML for the reviews
    reviews_html = ""
    for r in reviews:
        reviews_html += f"""
                <!-- Review: {r['name']} -->
                <div class="glass-panel p-6 rounded-xl review-card flex flex-col h-full">
                    <div class="flex items-center gap-4 mb-4">
                        <div class="w-12 h-12 rounded-full overflow-hidden border border-neon/30 flex-shrink-0">
                            <img src="{r['avatar']}" alt="{r['name']}" class="w-full h-full object-cover review-avatar">
                        </div>
                        <div>
                            <h3 class="text-neon font-retro text-sm uppercase tracking-wider">{r['name']}</h3>
                            <p class="text-xs text-gray-300">{r['role']}</p>
                        </div>
                    </div>
                    <p class="text-xs sm:text-sm text-gray-100 leading-relaxed italic mb-4 flex-grow">
                        "{r['text']}"
                    </p>
                    <div class="mt-auto pt-4 border-t border-gray-700/50 flex justify-between items-center">
                        <span class="text-[10px] uppercase font-mono text-gray-300">{r['date']}</span>
                        <a href="{r['linkedin']}" target="_blank" class="text-neon hover:underline text-[10px] font-mono tracking-tighter">View Profile ↗</a>
                    </div>
                </div>"""

    # Replace the existing grid content
    # Look for the grid container
    pattern = re.compile(r'(<div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-left">).*?(</div>\s+</div>\s+<div class="flex flex-col sm:flex-row)', re.DOTALL)

    if pattern.search(html):
        new_html = pattern.sub(rf'\1{reviews_html}\n            \2', html)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_html)
        print("✅ index.html updated with latest reviews.")
    else:
        print("❌ Could not find the reviews grid in index.html to update.")

async def main():
    profile_url = "https://www.linkedin.com/in/max-uroda"
    local_file = "recommendations.html"
    final_data = None

    # Check for local file first (most reliable for user running locally)
    if os.path.exists(local_file):
        print(f"📄 Found local file '{local_file}'. Parsing...")
        with open(local_file, "r", encoding="utf-8") as f:
            content = f.read()
            final_data = parse_recommendations_html(content)
            if final_data:
                print(f"✅ Successfully parsed {len(final_data)} items from local file.")
            else:
                print("⚠️ Local file found but no recommendations were parsed.")

    # Try live scraping if no local data
    if not final_data:
        final_data = await scrape_linkedin_recommendations(profile_url)

    # Fallback to hardcoded template
    if not final_data:
        print("💡 Falling back to template data (from screenshot).")
        final_data = SCREENSHOT_DATA

    # Save to reviews.json
    with open("reviews.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2)
    print(f"✅ reviews.json updated with {len(final_data)} items.")

    # Update index.html
    update_html_with_reviews(final_data)

if __name__ == "__main__":
    asyncio.run(main())
