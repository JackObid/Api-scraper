from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Initialize the rate limiter with the correct parameter name
limiter = Limiter(app, key_func=get_remote_address)  # Corrected 'key_function' to 'key_func'

@app.route('/scrape', methods=['POST'])
@limiter.limit("100/day")  # Allow 100 requests per day per IP
def scrape_to_markdown():
    # Get the API key from the headers
    api_key = request.headers.get('X-RapidAPI-Key')
    if not api_key:
        return jsonify({"error": "Missing API key"}), 401

    # Validate the API key (you can store valid keys in a database or environment variable)
    valid_keys = ["your_valid_api_key_here"]  # Replace with your actual keys
    if api_key not in valid_keys:
        return jsonify({"error": "Invalid API key"}), 403

    # Get the URL from the JSON payload (POST request)
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' parameter in JSON payload"}), 400

    url = data['url']

    try:
        # Fetch the HTML content of the website
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract main content (for Wikipedia, we target the <div> with class 'mw-parser-output')
        main_div = soup.find('div', class_='mw-parser-output')
        if not main_div:
            # Fallback: If 'mw-parser-output' is not found, extract all relevant tags
            main_content = ""
            for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li']:
                elements = soup.find_all(tag)
                for element in elements:
                    main_content += str(element)
            if not main_content.strip():  # Ensure there is some content
                return jsonify({"error": "Could not find any parsable content on the page."}), 400
        else:
            main_content = str(main_div)

        # Convert the extracted content to Markdown
        markdown_content = md(main_content)

        # Return the Markdown content as JSON
        return jsonify({"markdown": markdown_content})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch content from {url}. Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)