# Selenium Automation Code — Google Autocomplete Keyword Extractor

A production-ready Python CLI automation tool built with **Selenium** and **OpenPyXL** that reads seed keywords from an Excel workbook, queries Google Search autocomplete suggestions using explicit waits and fallback selectors, and exports the shortest and longest suggestions to a structured Excel output file.

## Features
- **Explicit Waits & Fallback Selectors:** Uses `WebDriverWait` instead of brittle hardcoded sleeps and supports modern Google autocomplete DOM selectors.
- **Headless by Default:** Runs cleanly in headless Chrome (`--headless=new`) with an optional `--headed` flag for visual debugging.
- **Safe Resource Cleanup:** Always closes the WebDriver and saves partial/full Excel results inside a `finally` block.
- **Configurable CLI:** Supports custom input/output workbook paths and per-query rate-limit delays.

## Tech Stack
- **Python 3.9+**
- **Selenium** (browser automation)
- **OpenPyXL** (Excel `.xlsx` read/write)

## Setup & Usage

```bash
pip install -r requirements.txt
python selenium_automation.py --input keywords.xlsx --output result.xlsx --delay 1.5
```

### CLI Options
| Flag | Default | Description |
| :--- | :--- | :--- |
| `--input` | `keywords.xlsx` | Path to the input Excel workbook (keywords in column A) |
| `--output` | `result.xlsx` | Path to save the enriched Excel workbook (shortest in column B, longest in column C) |
| `--headed` | `False` | Run Chrome with a visible browser window |
| `--delay` | `1.5` | Delay in seconds between keyword queries |
