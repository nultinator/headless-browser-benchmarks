import psutil
import time
import datetime
import logging
import csv
from dataclasses import dataclass, field
from threading import Thread, Event

@dataclass
class PerformanceSnapshot:
    cpu: float = 0.0
    ram: float = 0.0
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)


def monitor_system(test_name, interval=1, stop_event=None):
    """
    Monitor CPU and RAM usage at regular intervals until the stop event is set.
    
    :param test_name: Name of the test (used for logging and CSV file naming).
    :param interval: Time interval in seconds between readings.
    :param stop_event: Threading Event to signal when to stop monitoring.
    """
    # Create a logger specifically for this test
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)

    # Create a file handler for the test
    file_handler = logging.FileHandler(f"{test_name}.log", mode="w", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # Add the handler to the logger (avoid duplicate handlers)
    if not logger.handlers:
        logger.addHandler(file_handler)

    logger.info("Monitoring CPU and RAM usage...")
    logger.info(f"{'Time':<20} {'CPU (%)':<10} {'RAM (%)':<10}")

    with open(f"{test_name}.csv", mode="w", newline="") as csv_file:
        fieldnames = ["timestamp", "cpu", "ram"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        try:
            while not stop_event.is_set():
                snapshot = PerformanceSnapshot(
                    cpu=psutil.cpu_percent(interval=None),
                    ram=psutil.virtual_memory().percent
                )
                writer.writerow({
                    "timestamp": snapshot.timestamp,
                    "cpu": snapshot.cpu,
                    "ram": snapshot.ram
                })
                logger.info(f"Logged: {snapshot.timestamp}, CPU: {snapshot.cpu}, RAM: {snapshot.ram}")
                time.sleep(interval)
        except Exception as e:
            logger.error(f"Error in monitor_system: {e}")
        finally:
            logger.info("Monitoring stopped.")
