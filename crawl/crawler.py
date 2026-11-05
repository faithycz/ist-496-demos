from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from fake_useragent import UserAgent
from markdownify import markdownify as md
import random
import asyncio

URL = ("https://pennstate.service-now.com/kb?id=kb_search&kb_knowledge_base=a007226c4fe9030409d02ae6f110c753&spa=1&kb_category=2757b1694fc6078031427bcd0210c790")
MARKDOWN_FOLDER = Path("crawled_markdown")

async def crawl_page(page, page_url: str):
    print("Crawl: ", page_url)

    await page.goto(page_url)
    await page.wait_for_load_state("networkidle")

    # get page HTML
    page_content = await page.content()

    # parse page HTML
    soup = BeautifulSoup(page_content, "html.parser")

    # convert HTML to markdown format
    content = md(str(soup), heading_style="ATX")

    # only keep content after first heading
    first_heading = content.find("#")

    if first_heading != -1:
        content = content[first_heading:]

    # get sys_kb_id from URL
    parsed_url = urlparse(page_url)
    sys_kb_id = parse_qs(parsed_url.query)["sys_kb_id"][0]

    # create markdown folder
    MARKDOWN_FOLDER.mkdir(exist_ok=True)

    # create the markdown file going into the markdown folder
    markdown_file = MARKDOWN_FOLDER / f"{sys_kb_id}.md"

    # save the page content to the file
    markdown_file.write_text(content, encoding="utf-8")

    print("Saved file:", markdown_file)

async def get_links(page):
    page_content = await page.content()
    soup = BeautifulSoup(page_content, "html.parser")

    # find all links on the page
    links = soup.find_all("a", href=lambda href: href and href.startswith("?id=kb_article_view"))

    return [urljoin(page.url, link["href"]) for link in links]

async def main():
    # create random user agent
    ua = UserAgent()
    random_user_agent = ua.random

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        print("Browser launched!")

        context = await browser.new_context(
            user_agent=random_user_agent
        )

        page = await context.new_page()

        # only get page links, do NOT download entire page
        await page.goto(URL)
        await page.wait_for_load_state("networkidle")

        links = await get_links(page)

        print("Number of links found:", len(links))

        # crawl each article on the page
        for link in links:
            # giving a random wait time from 1-3 seconds
            wait_time = random.randint(1, 3)

            print(f"Waiting {wait_time} seconds...")
            await asyncio.sleep(wait_time)

            await crawl_page(page, link)

        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())