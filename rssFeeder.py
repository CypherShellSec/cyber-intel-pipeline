#!/usr/bin/env python3

import argparse
import sys
from datetime import datetime, timedelta, timezone
from feedparser import parse as feedparse

def read_urls_from_file(filename):
    """Read RSS/Atom URLs from a text file, one per line. Ignore empty lines and comments."""
    urls = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)
    return urls

def parse_entry_date(entry):
    """Parse the entry's published or updated date using feedparser's struct_time."""
    time_struct = entry.get('published_parsed') or entry.get('updated_parsed')
    if time_struct:
        return datetime(*time_struct[:6], tzinfo=timezone.utc)
    return None

def fetch_and_print_links(url, cutoff_dt, num=None):
    feed = feedparse(url)
    
    if feed.bozo:
        print(f"Warning: Malformed feed ({url})", file=sys.stderr)
    
    entries = feed.entries
    count = 0
    for entry in entries:
        if num is not None and count >= num:
            break
        
        pub_date = parse_entry_date(entry)
        if pub_date is None or pub_date < cutoff_dt:
            continue  # Skip if no date or older than 24h
        
        link = entry.get('link', '').strip()
        if link:
            print(link)
            count += 1

def main():
    parser = argparse.ArgumentParser(description="Ultra-minimal RSS reader: only new links (last 24h), one URL per line")
    parser.add_argument('file', nargs='?', default='feeds.txt',
                        help="Text file with RSS/Atom URLs, one per line (default: feeds.txt)")
    parser.add_argument('-n', '--num', type=int, default=None,
                        help="Max new links per feed (default: all from last 24h)")
    args = parser.parse_args()

    # Cutoff: last 24 hours in UTC
    cutoff_dt = datetime.now(timezone.utc) - timedelta(hours=24)

    try:
        urls = read_urls_from_file(args.file)
    except FileNotFoundError:
        print(f"Error: '{args.file}' not found.", file=sys.stderr)
        sys.exit(1)

    if not urls:
        print("No URLs found in file.", file=sys.stderr)
        sys.exit(1)

    for url in urls:
        try:
            fetch_and_print_links(url, cutoff_dt, args.num)
        except Exception as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
