# Selenium Automation Code — Google Autocomplete Keyword Extractor

A Python and Selenium automation script that reads a list of seed keywords from an Excel workbook (`keywords.xlsx`), queries Google Search autocomplete suggestions sequentially, and records the shortest and longest matching suggestions into an output Excel file (`result.xlsx`).

## How It Works
1. Loads input keywords from column A of `keywords.xlsx` using `openpyxl`.
2. Launches Chrome via Selenium WebDriver and enters each keyword into Google Search.
3. Captures live autocomplete suggestions and computes the shortest and longest suggestion by character length.
4. Writes the extracted results to columns B and C and saves the output to `result.xlsx`.

## Tech Stack
- **Python 3**
- **Selenium** (browser automation)
- **OpenPyXL** (Excel `.xlsx` read/write)

## Setup & Usage

```bash
pip install -r requirements.txt
python selenium_automation.py
```

Make sure Google Chrome and a compatible ChromeDriver are installed on your system, and place your input keywords in `keywords.xlsx`.
