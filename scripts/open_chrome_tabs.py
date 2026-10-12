#!/usr/bin/env python3
"""Open one or more URLs as tabs in Google Chrome.

Usage:
    python3 open_chrome_tabs.py https://example.com https://github.com
    python3 open_chrome_tabs.py --file urls.txt
    python3 open_chrome_tabs.py --new-window https://example.com

With no URLs, the DEFAULT_URLS list below is opened.
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys

DEFAULT_URLS = [
    "https://www.google.com",
    "https://developer.mozilla.org",
    "https://github.com",
]


def find_chrome():
    """Return the path to the Chrome executable, or None if not found."""
    system = platform.system()
    if system == "Darwin":
        candidates = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    elif system == "Windows":
        candidates = [
            os.path.join(os.environ.get(var, ""), r"Google\Chrome\Application\chrome.exe")
            for var in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")
        ]
    else:
        candidates = [
            shutil.which(name)
            for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
        ]
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return None


def read_urls(path):
    """Read URLs from a file, one per line; blank lines and # comments are skipped."""
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.lstrip().startswith("#")]


def normalize(url):
    """Add https:// if the URL has no scheme."""
    return url if "://" in url else "https://" + url


def main():
    parser = argparse.ArgumentParser(description="Open URLs as tabs in Google Chrome.")
    parser.add_argument("urls", nargs="*", help="URLs to open")
    parser.add_argument("-f", "--file", help="text file with one URL per line")
    parser.add_argument("-n", "--new-window", action="store_true", help="open the tabs in a new window")
    args = parser.parse_args()

    urls = list(args.urls)
    if args.file:
        urls += read_urls(args.file)
    if not urls:
        urls = DEFAULT_URLS
    urls = [normalize(u) for u in urls]

    chrome = find_chrome()
    if chrome is None:
        sys.exit("Google Chrome was not found. Install it or edit find_chrome() with its path.")

    cmd = [chrome]
    if args.new_window:
        cmd.append("--new-window")
    cmd += urls

    # Chrome hands the URLs to an already-running instance if there is one,
    # so this returns right away instead of waiting for the browser to close.
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Opened {len(urls)} tab(s) in Chrome.")


if __name__ == "__main__":
    main()
