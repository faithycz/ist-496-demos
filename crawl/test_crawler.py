import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from fake_useragent import UserAgent
from markdownify import markdownify as md

PAGE_TO_BE_CRAWLED = (
    "https://pennstate.service-now.com/kb?id=kb_article_view&sys_kb_id=98b80bc7c3eabd5062ca32cf050131bd")
MARKDOWN_FOLDER = Path("crawled_markdown")


async def get_links():
    async with async_playwright() as p:
        # launching the browser
        browser = await p.chromium.launch(headless=False)
        print("Browser launched!")

        # open PSU knowledge base website with filtered search results
        page = await browser.new_page()
        await page.goto(
            "https://pennstate.service-now.com/kb?id=kb_search&kb_knowledge_base=a007226c4fe9030409d02ae6f110c753&spa=1&kb_category=01c1befc4fa18700d0f9e3414210c795")
        await page.wait_for_load_state("networkidle")

        # Click the body first to focus the page so it receives keyboard inputs
        await page.click("body")

        scroll_height = await page.evaluate("document.body.scrollHeight")

        # try converting to while true
        for _ in range(16):
            # Simulate pressing the "PageDown" key
            await page.keyboard.press("PageDown")

            # Alternatively, use "End" to jump straight to the bottom of the current view
            # page.keyboard.press("End")

            # Wait for lazy loading to trigger and elements to render
            await asyncio.sleep(1)

            scroll_top = await page.evaluate("document.body.scrollTop")
            client_height = await page.evaluate("document.body.clientHeight")
            # print(f"Scroll height: {scroll_height} | Client height: {client_height} | Scroll top: {scroll_top}")
            # if we are at the bottom, then we do one more scroll and break
            # if scroll_height - scroll_top - client_height <= 1:
            #     # Press it one more time just to be sure
            #     # await page.keyboard.press("PageDown")
            #     # await asyncio.sleep(1)
            #     break  # Break if the page height is completely stuck

        print("Page loaded successfully:", await page.title())

        # Locate all anchor (<a>) tags on the page
        links_locator = page.locator("a.kb-title")

        # Extract the 'href' attribute from all matching elements
        # evaluate_all runs a JavaScript function across all elements in the DOM
        links = await links_locator.evaluate_all("elements => elements.map(e => e.href)")

        print("Number of links found:", len(links))

        # for link in links:
            # print(link)

        # close the browser
        await browser.close()
        print("Browser closed.")


async def crawl_page(page_url: str):
    ua = UserAgent()
    random_user_agent = ua.random

    async with async_playwright() as p:
        browser = p.chromium.launch(headless=True)
        print("Browser launched!")

        context = browser.new_context(
            user_agent=random_user_agent
        )

        page = context.new_page()

        page.goto(page_url)
        page.wait_for_load_state("networkidle")

        print("Page loaded successfully:", page.title())

        # get page HTML
        page_content = page.content()

        # parse the HTML
        soup = BeautifulSoup(page_content, "html.parser")

        # extract all text from the page
        content = md(str(soup))

        # only keep content that comes after first #
        first_heading = content.find("#")

        if first_heading != -1:
            content = content[first_heading:]

        # get sys_kb_id from the URL
        parsed_url = urlparse(page_url)
        sys_kb_id = parse_qs(parsed_url.query)["sys_kb_id"][0]

        # create the markdown folder if it doesn't exist
        MARKDOWN_FOLDER.mkdir(exist_ok=True)

        # create the markdown file
        markdown_file = MARKDOWN_FOLDER / f"{sys_kb_id}.md"

        # write to the file and save the content
        markdown_file.write_text(content, encoding="utf-8")

        print("Saved file:", markdown_file)

        # close the context and browser
        context.close()
        browser.close()

        print("Browser closed.")


async def main():
    await get_links()
    # crawl_page(PAGE_TO_BE_CRAWLED)


if __name__ == "__main__":
    asyncio.run(main())
