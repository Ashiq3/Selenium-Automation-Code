"""Automated Google Autocomplete Keyword Extractor.

Reads seed keywords from an input Excel workbook, queries Google Search
autocomplete suggestions using Selenium WebDriver with explicit waits, and
exports the shortest and longest suggestions to a structured Excel file.
"""

from __future__ import annotations

import argparse
import logging
import time
from pathlib import Path
from typing import List, Optional, Tuple

import openpyxl
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

AUTOCOMPLETE_SELECTORS = (
    "ul[role='listbox'] li[role='presentation'] span",
    "[role='listbox'] [role='option']",
    ".sbtc .sbl1",
)


def create_driver(headless: bool = True) -> webdriver.Chrome:
    """Initialize a configured Chrome WebDriver instance."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1280,800")
    return webdriver.Chrome(options=options)


def fetch_autocomplete_suggestions(
    driver: webdriver.Chrome,
    keyword: str,
    timeout: int = 8,
) -> List[str]:
    """Query Google Search and return non-empty autocomplete suggestions."""
    driver.get("https://www.google.com")
    wait = WebDriverWait(driver, timeout)

    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.clear()
    search_box.send_keys(keyword)

    for selector in AUTOCOMPLETE_SELECTORS:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            suggestions = [el.text.strip() for el in elements if el.text.strip()]
            if suggestions:
                return list(dict.fromkeys(suggestions))
        except TimeoutException:
            continue

    return []


def extract_shortest_and_longest(
    suggestions: List[str],
) -> Tuple[Optional[str], Optional[str]]:
    """Return the shortest and longest strings from a suggestion list."""
    if not suggestions:
        return None, None
    return min(suggestions, key=len), max(suggestions, key=len)


def process_keywords(
    input_path: Path,
    output_path: Path,
    headless: bool = True,
    delay: float = 1.5,
    timeout: int = 8,
) -> None:
    """Read keywords from Excel, fetch suggestions, and save results."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input workbook not found: {input_path}")

    workbook = openpyxl.load_workbook(input_path)
    sheet = workbook.active

    driver = create_driver(headless=headless)
    try:
        for row_idx in range(1, sheet.max_row + 1):
            raw_value = sheet.cell(row=row_idx, column=1).value
            if not raw_value or not str(raw_value).strip():
                continue

            keyword = str(raw_value).strip()
            logger.info("Processing row %d: '%s'", row_idx, keyword)

            try:
                suggestions = fetch_autocomplete_suggestions(
                    driver, keyword, timeout=timeout
                )
            except WebDriverException as exc:
                logger.warning("WebDriver error for '%s': %s", keyword, exc)
                continue

            shortest, longest = extract_shortest_and_longest(suggestions)
            if not shortest or not longest:
                logger.info("No suggestions found for '%s'", keyword)
                continue

            sheet.cell(row=row_idx, column=2).value = shortest
            sheet.cell(row=row_idx, column=3).value = longest
            logger.info("  Shortest: %s | Longest: %s", shortest, longest)

            if delay > 0:
                time.sleep(delay)
    finally:
        driver.quit()
        workbook.save(output_path)
        logger.info("Saved results to %s", output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract shortest and longest Google autocomplete suggestions into Excel."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("keywords.xlsx"),
        help="Path to the input Excel workbook (default: keywords.xlsx)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("result.xlsx"),
        help="Path to the output Excel workbook (default: result.xlsx)",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run Chrome with a visible browser window instead of headless mode",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.5,
        help="Delay in seconds between keyword queries (default: 1.5)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    process_keywords(
        input_path=args.input,
        output_path=args.output,
        headless=not args.headed,
        delay=args.delay,
    )
