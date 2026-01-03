#!/usr/bin/env python3

import argparse
import json
import sys
import time
import requests

def summarize_with_ollama(body_text, host="http://localhost:11434"):
    """
    Send article body to local Ollama (Mistral 7B) and get a 4-sentence summary.
    """
    url = f"{host}/api/generate"
    
    # Truncate if too long — Mistral 7B has ~8k context, but keep safe
    truncated_text = body_text[:15000]
    
    prompt = (
        "Summarize the following article in exactly 4 sentences. "
        "Focus only on the main points, key events, and conclusions. "
        "Act as a cyber analyst when analyzing and presenting information. "
        "Do not add opinions, introductions, or extra commentary.\n\n"
        f"{truncated_text}"
    )
    
    payload = {
        "model": "mistral",          # change if you use a different tag, e.g., "mistral:7b-instruct-q5_K_M"
        "prompt": prompt,
        "stream": False,             # we want full response at once
        "options": {
            "temperature": 0.3,
            "num_ctx": 8192,
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=600)  # longer timeout for local model
        response.raise_for_status()
        result = response.json()
        return result["response"].strip()
    except requests.exceptions.ConnectionError:
        return "[Error: Could not connect to Ollama. Is it running?[](http://localhost:11434)]"
    except requests.exceptions.Timeout:
        return "[Error: Request timed out. Try a smaller article or increase timeout.]"
    except Exception as e:
        return f"[Error generating summary: {str(e)}]"

def main():
    parser = argparse.ArgumentParser(
        description="Generate 4-sentence summaries using local Ollama (Mistral 7B) from article JSON"
    )
    parser.add_argument(
        'input_json',
        help="Input JSON file from extract_articles.py (e.g., articles.json)"
    )
    parser.add_argument(
        '-o', '--output',
        default='summaries.txt',
        help="Output text file (default: summaries.txt)"
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=0.5,
        help="Delay in seconds between summaries (default: 0.5 — fast for local)"
    )
    parser.add_argument(
        '--host',
        default='http://localhost:11434',
        help="Ollama server URL (default: http://localhost:11434)"
    )
    args = parser.parse_args()

    # Load JSON
    try:
        with open(args.input_json, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except FileNotFoundError:
        print(f"Error: '{args.input_json}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{args.input_json}'.", file=sys.stderr)
        sys.exit(1)

    # Filter successful extractions
    valid_articles = {url: data for url, data in articles.items() if 'body' in data}
    skipped = len(articles) - len(valid_articles)

    if skipped > 0:
        print(f"Skipping {skipped} URLs with errors or no content.")

    if not valid_articles:
        print("No articles with body text found.", file=sys.stderr)
        sys.exit(1)

    print(f"Generating summaries for {len(valid_articles)} articles using local Ollama (Mistral 7B)...")

    with open(args.output, 'w', encoding='utf-8') as out_f:
        for i, (url, data) in enumerate(valid_articles.items(), 1):
            body = data['body']
            print(f"[{i}/{len(valid_articles)}] Summarizing: {url}")

            summary = summarize_with_ollama(body, args.host)

            out_f.write(f"URL: {url}\n")
            out_f.write(f"SUMMARY:\n{summary}\n")
            out_f.write("\n\n")

            if args.delay > 0:
                time.sleep(args.delay)

    print(f"\nDone! Summaries saved to '{args.output}'")

if __name__ == "__main__":
    main()
