# AI Content Scraper API

## Overview

The **AI Content Scraper API** is a powerful tool designed to scrape content from any website and convert it into Markdown format. This makes it ideal for preparing data for Large Language Model (LLM) training or other text-processing tasks. The API is built using Python with Flask, and it includes features such as rate limiting, API key authentication, and robust error handling.

---

## Features

- **Scrape Any Website**: Extract text content from any publicly accessible website.
- **Convert to Markdown**: Automatically convert the scraped content into Markdown format for easy integration into LLM training pipelines.
- **Rate Limiting**: Prevent abuse with a limit of 100 requests per day per IP address.
- **API Key Authentication**: Secure your API by requiring valid API keys for access.
- **Error Handling**: Provides clear and informative error messages for invalid inputs, missing content, or network issues.

---

## Requirements

To run this project locally, you need the following:

- Python 3.7 or higher
- Pip (Python package manager)
- Virtual environment (optional but recommended)

Install the required dependencies using `pip`:

```bash
pip install flask requests beautifulsoup4 markdownify flask_limiter
