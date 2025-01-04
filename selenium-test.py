from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Event, Thread
from time import sleep
import psutil
from system_logger import monitor_system  # Import the logger

OPTIONS = webdriver.ChromeOptions()

def run_test(test_name, test_function, interval=2):
    """
    Runs a given test function with system monitoring.

    :param test_name: Name of the test (used for logging and CSV file naming).
    :param test_function: The function to execute the test logic.
    :param interval: Interval (in seconds) for logging CPU and RAM usage.
    """
    # Create a threading Event to signal the monitor to stop
    stop_event = Event()

    # Start the monitor in a separate thread
    monitor_thread = Thread(target=monitor_system, kwargs={"test_name": test_name, "interval": interval, "stop_event": stop_event})
    monitor_thread.start()

    # Run the test function
    try:
        print(f"Starting test: {test_name}")
        test_function()
    finally:
        # Signal the monitor to stop and wait for it to finish
        stop_event.set()
        monitor_thread.join()
        print(f"Test {test_name} has completed.")

def scrolling_test():
    """
    Simulates infinite scrolling on a webpage.
    """
    driver = webdriver.Chrome(options=OPTIONS)
    driver.get("https://x.com/elonmusk")
    scrolls = 0
    while scrolls < 10:
        driver.execute_script("window.scrollBy(0, 500);")
        sleep(1)
        scrolls += 1
    driver.quit()
    print("Selenium infinite scroll test complete.")

def video_test():
    """
    open a page and attempt to autoplay a video
    """
    driver = webdriver.Chrome(options=OPTIONS)
    driver.get("https://www.youtube.com/watch?v=ZgkbnZeRkuY")

    sleep(5)
    driver.quit()

def pages_test():
    """
    Opens multiple pages in new tabs.
    """
    driver = webdriver.Chrome(options=OPTIONS)
    driver.get("https://x.com/elonmusk")
    pages = 0
    while pages < 1000:
        driver.execute_script("window.open('');")
        pages += 1
        print("Pages open:", pages)
    driver.quit()
    print("Selenium pages test complete.")

def instances_test():
    """
    Opens multiple browser instances.
    """
    open_instances = []
    while psutil.cpu_percent(interval=None) <= 95 and psutil.virtual_memory().percent <= 95:
        try:
            driver = webdriver.Chrome(options=OPTIONS)
            open_instances.append(driver)
            print("Browser instances:", len(open_instances))
        except:
            print("Failed to open more browsers, total:", len(open_instances))
            break

    print("Max browser instances:", len(open_instances))
    print("Closing all browsers.")
    for instance in open_instances:
        instance.quit()
    print("Selenium instances test complete.")

if __name__ == "__main__":
    # Define tests to run
    tests = [
        {"name": "scrolling", "function": scrolling_test},
        {"name": "pages", "function": pages_test},
        {"name": "instances", "function": instances_test},
        {"name": "video", "function": video_test}
    ]

    # Run each test sequentially
    for test in tests:
        run_test(test_name=test["name"], test_function=test["function"])
