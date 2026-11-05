from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio

async def main():
    async with async_playwright() as p:
        # Launch a browser
        browser = await p.chromium.launch(headless=True)
        print("Browser launched!")

        # Open Hacker News homepage
        page = await browser.new_page()
        await page.goto("https://news.ycombinator.com/")
        await page.wait_for_load_state("networkidle")
        print("Page loaded successfully:", await page.title())

        # Scrape top headlines
        await page.wait_for_selector(".titleline")
        headlines = await page.locator(".titleline").all_inner_texts()
        print("Top Headlines:")
        for headline in headlines:
            print("-", headline)

        # Search for "AI"
        search_box = page.locator("input[type='text']")
        await search_box.fill("AI")
        await search_box.press("Enter")
        await page.wait_for_load_state("networkidle")

        # Parse search results with BeautifulSoup
        page_content = await page.content()
        soup = BeautifulSoup(page_content, "html.parser")
        first_headline = soup.select_one(".titleline a")
        if first_headline:
            print("First search result headline:", first_headline.text)
        else:
            print("No search results found.")

        # Close the browser
        await browser.close()
        print("Browser closed.")

if __name__ == "__main__":
    asyncio.run(main())