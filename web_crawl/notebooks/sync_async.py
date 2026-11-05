import asyncio
from playwright.async_api import async_playwright


async def background_task():
    """A separate task to prove the event loop is not blocked."""

    for i in range(3):
        print(f"[Another task] Background task heartbeat {i}")
        await asyncio.sleep(2)


async def run_playwright():
    """
        Every time you call await, this function is paused/blocked/stopped until the await is complete.
        This is the so-called local blocking or local pause. It blocks this function, but not the event loop.
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("[Playwright] Navigating to page...")
        await page.goto("https://example.com")

        # This pauses this specific function but does NOT block the event loop
        print("[Playwright] Pausing here for 3 seconds...")
        await asyncio.sleep(3)

        print("[Playwright] Resuming and closing browser.")
        await browser.close()


async def main():
    # Run both the playwright script and the background task together
    await asyncio.gather(
        run_playwright(),
        background_task()
    )


if __name__ == "__main__":
    asyncio.run(main())