# AI Content Scraper and Summarizer API

## Overview

The **AI Content Scraper API** is a Flask-based web application that scrapes content from a given URL, converts it to Markdown, and generates a summary using either rule-based or AI-driven methods. It leverages libraries like BeautifulSoup for web scraping, Hugging Face Transformers for AI-based summarization, and Sumy for rule-based summarization.

### The AI Content Scraper and Summarizer allows users to

- **Scrape Any Website**: Fetch HTML content from any public URL.
- **Convert to Markdown**: Automatically convert the scraped content into Markdown format for easy integration into LLM training pipelines.
- **Generate Summaries**: Generate summaries of the extracted content using either a rule-based approach (Luhn algorithm) or an AI-based approach (Hugging Face's BART model).
- **Rate Limiting**: Prevent abuse with a limit of 100 requests per day per IP address.
- **API Key Authentication**: Secure your API by requiring valid API keys for access.
- **Error Handling**: Provides clear and informative error messages for invalid inputs, missing content, or network issues.

---

## Features

- Web scraping using requests and BeautifulSoup. Fetch HTML content from any public URL.
- Conversion of HTML to Markdown using markdownify.
- **Generate Summaries**: Generate summaries of the extracted content using either a rule-based approach (Luhn algorithm) or an AI-based approach (Hugging Face's BART model).
- Two summarization methods:
    - Rule-based summarization using the Luhn algorithm from the sumy   library.
    - AI-based summarization using Hugging Face's transformers library and the "facebook/bart-large-cnn" model.
- Rate limiting to control API usage.
- RESTful API endpoint (/scrape) that accepts POST requests with a URL and optional parameters.

## Requirements

To run this project locally, you need the following:

- Python 3.7 or higher
- Pip (Python package manager)
- Virtual environment (optional but recommended)

Install the required dependencies using `pip`:

```bash
pip install flask requests beautifulsoup4 markdownify flask_limiter
