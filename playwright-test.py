import asyncio
import psutil
from threading import Event, Thread
from playwright.async_api import async_playwright
from system_logger import monitor_system  # Import the logger


async def run_test(test_name, test_function, interval=2):
    """
    Runs a given test function with system monitoring.

    :param test_name: Name of the test (used for logging and CSV file naming).
    :param test_function: The coroutine to execute the test logic.
    :param interval: Interval (in seconds) for logging CPU and RAM usage.
    """
    # Create a threading Event to signal the monitor to stop
    stop_event = Event()

    # Start the monitor in a separate thread
    monitor_thread = Thread(
        target=monitor_system, 
        kwargs={"test_name": test_name, "interval": interval, "stop_event": stop_event}
    )
    monitor_thread.start()

    # Run the test function
    try:
        print(f"Starting test: {test_name}")
        await test_function()
    finally:
        # Signal the monitor to stop and wait for it to finish
        stop_event.set()
        monitor_thread.join()
        print(f"Test {test_name} has completed.")


async def scrolling_test():
    """
    Simulates infinite scrolling on a webpage using Playwright.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://x.com/elonmusk")
        for _ in range(10):
            await page.evaluate("window.scrollBy(0, 500);")
            await asyncio.sleep(1)
        await browser.close()
        print("Playwright infinite scroll test complete.")

async def video_test():
    """
    open and play a video.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.youtube.com/watch?v=ZgkbnZeRkuY")
        await page.wait_for_selector("ytd-player[id='ytd-player']")
        player = await page.query_selector("ytd-player[id='ytd-player']")
        await asyncio.sleep(5)
        await browser.close()
        print("Playwright infinite scroll test complete.")


async def pages_test():
    """
    Opens multiple pages in new tabs using Playwright.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://x.com/elonmusk")
        for pages in range(1000):
            await context.new_page()
            print(f"Pages open: {pages + 1}")
        await browser.close()
        print("Playwright pages test complete.")


async def instances_test():
    """
    Opens multiple browser instances using Playwright.
    """
    instances = []
    try:
        async with async_playwright() as p:
            while psutil.cpu_percent(interval=None) <= 95 and psutil.virtual_memory().percent <= 95:
                browser = await p.chromium.launch()
                instances.append(browser)
                print(f"Browser instances: {len(instances)}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print(f"Max browser instances reached: {len(instances)}")
        print("Closing all browser instances.")
        for browser in instances:
            await browser.close()
        print("Playwright instances test complete.")


async def main():
    """
    Orchestrates the execution of all tests sequentially.
    """
    tests = [
        {"name": "scrolling", "function": scrolling_test},
        {"name": "pages", "function": pages_test},
        {"name": "instances", "function": instances_test},
        {"name": "videos", "function": video_test}
    ]

    for test in tests:
        await run_test(test_name=test["name"], test_function=test["function"])


if __name__ == "__main__":
    asyncio.run(main())
