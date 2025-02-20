from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
from transformers import pipeline
from flask_limiter import Limiter  # Added for rate-limiting
from flask_limiter.util import get_remote_address  # Added for rate-limiting

app = Flask(__name__)

# Initialize rate-limiter (100 requests per day, 10 requests per minute)
limiter = Limiter(get_remote_address, app=app, default_limits=["100 per day", "10 per minute"])  

# Initialize the summarization pipeline (Hugging Face Transformers)
try:
    summarizer_pipeline = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
except Exception as e:
    print(f"Error loading summarization pipeline: {str(e)}")
    summarizer_pipeline = None # Fallback or handle this case
    
@app.route('/scrape', methods=['POST'])
@limiter.limit("100/day")  # Allow 100 requests per day per IP
def scrape_to_markdown():
    # Get the URL and optional parameters from the request body
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    url = data['url']
    summarization_method = data.get('summarization_method', 'rule_based')  # Default to rule-based
    max_summary_length = int(data.get('max_summary_length', 100))  # Default to 100 words
    min_summary_length = int(data.get('min_summary_length', 30))   # Default to 30 words

    try:
        # Fetch the HTML content of the website
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract main content (you may need to customize this based on the website)
        main_content = ""
        for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li']:
            elements = soup.find_all(tag)
            for element in elements:
                main_content += str(element)

        # Convert the extracted content to Markdown
        markdown_content = md(main_content)

        # Extract plain text for summarization
        plain_text = " ".join(soup.stripped_strings)

        # Generate summary based on the selected method
        if summarization_method == 'rule_based':
            summary = rule_based_summarize(plain_text, num_sentences=3)
        elif summarization_method == 'ai':
            summary = ai_summarize(plain_text, max_summary_length, min_summary_length)
        else:
            return jsonify({"error": "Invalid summarization_method. Use 'rule_based' or 'ai'."}), 400

        # Return the Markdown content and summary as JSON
        return jsonify({
            "markdown": markdown_content,
            "summary": summary
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch content from {url}. Error: {str(e)}"}), 500


def rule_based_summarize(text, num_sentences=3):
    """Generate a summary using a rule-based approach (Luhn algorithm)."""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LuhnSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join([str(sentence) for sentence in summary])


def ai_summarize(text, max_length=100, min_length=30):
    """
    Generate a summary using Hugging Face's Transformer models.

    Args:
        text (str): Input text to summarize.
        max_length (int): Maximum length of the summary in words.
        min_length (int): Minimum length of the summary in words.

    Returns:
        str: Generated summary.
    """
    # Ensure the input text is not too long to avoid memory issues
    if len(text.split()) > 1000:
        text = " ".join(text.split()[:1000])  # Truncate to first 1000 words

    try:
        # Generate the summary
        summary = summarizer_pipeline(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False  # Disable sampling for deterministic results
        )
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error generating summary: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)