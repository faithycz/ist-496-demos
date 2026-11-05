from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def main():
    with sync_playwright() as p:
        # Launch a browser
        browser = p.chromium.launch(headless=True)
        print("Browser launched!")

        # Open Hacker News homepage
        page = browser.new_page()
        page.goto("https://news.ycombinator.com/")
        page.wait_for_load_state("networkidle")
        print("Page loaded successfully:", page.title())

        # Scrape top headlines
        page.wait_for_selector(".athing.submission")
        headlines = page.locator(".athing.submission .titleline a").all_inner_texts()
        print("Top Headlines:")
        for headline in headlines:
            print("-", headline)

        # Search for "AI"
        page.goto("https://hn.algolia.com/?query=AI")
        page.wait_for_load_state("networkidle")

        # Parse search results with BeautifulSoup
        page_content = page.content()
        soup = BeautifulSoup(page_content, "html.parser")
        first_headline = soup.select_one("a[href*='/item?id=']")

        if first_headline:
            print("First search result headline:", first_headline.text)
        else:
            print("No search results found.")

        # Close the browser
        browser.close()
        print("Browser closed.")

if __name__ == "__main__":
    main()