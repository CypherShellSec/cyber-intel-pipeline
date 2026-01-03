#!/usr/bin/env python3

import argparse
import json
import sys
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from readability import Document
import time

def clean_text(text):
    """Clean up whitespace while preserving paragraph breaks."""
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def extract_article_body(url, timeout=10):
    """Fetch URL and extract clean article body using readability-lxml."""
    try:
        response = requests.get(url, timeout=timeout, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; RSSArticleExtractor/1.0)'
        })
        response.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to fetch: {str(e)}"}

    doc = Document(response.text)
    summary_html = doc.summary()

    soup = BeautifulSoup(summary_html, 'html.parser')
    article_text = soup.get_text(separator='\n')

    cleaned_text = clean_text(article_text)

    if not cleaned_text.strip():
        return {"error": "No readable content extracted"}

    return {"body": cleaned_text}

def main():
    parser = argparse.ArgumentParser(
        description="Extract article bodies from a list of URLs and save as JSON"
    )
    parser.add_argument(
        'input_file',
        help="Text file with one URL per line"
    )
    parser.add_argument(
        '-o', '--output',
        default='articles.json',
        help="Output JSON file (default: articles.json)"
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help="Delay in seconds between requests (default: 1.0, to be polite)"
    )
    args = parser.parse_args()

    # Read URLs
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)

    if not urls:
        print("No URLs found in input file.", file=sys.stderr)
        sys.exit(1)

    results = {}

    print(f"Processing {len(urls)} URLs...")
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Extracting: {url}")
        body_data = extract_article_body(url)
        results[url] = body_data
        time.sleep(args.delay)  # Be respectful to servers

    # Write to JSON file
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nDone! Saved {len(results)} articles to '{args.output}'")
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Install required packages:
    # pip install requests beautifulsoup4 readability-lxml
    main()
