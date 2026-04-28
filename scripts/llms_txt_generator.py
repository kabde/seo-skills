#!/usr/bin/env python3
"""
llms.txt Generator for WordPress sites.

Connects to a WordPress site via REST API and generates an llms.txt file
following the standard format. Fetches site info, top posts by category,
and author information.

Usage:
    python llms_txt_generator.py https://example.com --user admin --password xxxx
    python llms_txt_generator.py https://example.com --user admin --password xxxx --output llms.txt
    python llms_txt_generator.py https://example.com --user admin --password xxxx --json
"""

import argparse
import base64
import ipaddress
import json
import re
import socket
import sys
from typing import Optional
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


# ─── SSRF Protection ────────────────────────────────────────────────────────

def validate_url(url: str) -> str:
    """Validate URL and block private/internal IPs (SSRF protection)."""
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}"
        parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Invalid URL scheme: {parsed.scheme}")

    try:
        resolved_ip = socket.gethostbyname(parsed.hostname)
        ip = ipaddress.ip_address(resolved_ip)
        if ip.is_private or ip.is_loopback or ip.is_reserved:
            raise ValueError(f"Blocked: URL resolves to private/internal IP ({resolved_ip})")
    except (socket.gaierror, ValueError) as e:
        if "Blocked" in str(e):
            raise
    return url


# ─── WordPress API Client ───────────────────────────────────────────────────

class WordPressLLMSClient:
    """Lightweight WordPress REST API client for llms.txt generation."""

    def __init__(self, site_url: str, username: str, password: str):
        self.site_url = validate_url(site_url.rstrip("/"))
        self.api_base = f"{self.site_url}/wp-json/wp/v2"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "ClaudeSEO/2.0 llms-txt-generator",
        })
        if username and password:
            credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
            self.session.headers["Authorization"] = f"Basic {credentials}"

    def _get(self, endpoint: str, params: dict = None) -> list | dict:
        """Make a GET request to the WP REST API."""
        url = f"{self.api_base}/{endpoint}"
        resp = self.session.get(url, params=params or {}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_site_info(self) -> dict:
        """Fetch site name and description."""
        url = f"{self.site_url}/wp-json"
        resp = self.session.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return {
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "url": data.get("url", self.site_url),
        }

    def get_categories(self) -> list:
        """Fetch all categories with post counts."""
        categories = []
        page = 1
        while True:
            batch = self._get("categories", {"per_page": 100, "page": page})
            if not batch:
                break
            categories.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        # Filter out uncategorized and empty categories
        return [c for c in categories if c.get("count", 0) > 0 and c.get("slug") != "uncategorized"]

    def get_posts_by_category(self, category_id: int, limit: int = 5) -> list:
        """Fetch top posts for a category, ordered by date descending."""
        posts = self._get("posts", {
            "categories": category_id,
            "per_page": limit,
            "orderby": "date",
            "order": "desc",
            "_fields": "id,title,link,excerpt,date",
        })
        return posts

    def get_all_top_posts(self, limit: int = 10) -> list:
        """Fetch most recent posts across all categories."""
        posts = self._get("posts", {
            "per_page": limit,
            "orderby": "date",
            "order": "desc",
            "_fields": "id,title,link,excerpt,date",
        })
        return posts

    def get_authors(self) -> list:
        """Fetch site authors."""
        users = self._get("users", {"per_page": 20, "_fields": "id,name,description,link,slug"})
        return users


# ─── Text Helpers ────────────────────────────────────────────────────────────

def strip_html(html_str: str) -> str:
    """Strip HTML tags from a string."""
    if BeautifulSoup:
        return BeautifulSoup(html_str, "html.parser").get_text(strip=True)
    return re.sub(r"<[^>]+>", "", html_str).strip()


def truncate(text: str, max_len: int = 120) -> str:
    """Truncate text to max length with ellipsis."""
    text = text.strip()
    if len(text) <= max_len:
        return text
    return text[:max_len - 3].rsplit(" ", 1)[0] + "..."


# ─── llms.txt Generation ────────────────────────────────────────────────────

def generate_llms_txt(site_url: str, username: str, password: str) -> dict:
    """Generate llms.txt content from WordPress data."""
    client = WordPressLLMSClient(site_url, username, password)

    # Fetch data
    site_info = client.get_site_info()
    categories = client.get_categories()
    authors = client.get_authors()

    # Build category -> posts mapping
    category_posts = {}
    for cat in categories:
        posts = client.get_posts_by_category(cat["id"], limit=5)
        if posts:
            category_posts[cat["name"]] = [
                {
                    "title": strip_html(p["title"]["rendered"]),
                    "url": p["link"],
                    "excerpt": truncate(strip_html(p["excerpt"]["rendered"])),
                }
                for p in posts
            ]

    # If no categories with posts, fetch recent posts
    if not category_posts:
        top_posts = client.get_all_top_posts(limit=10)
        if top_posts:
            category_posts["Recent Articles"] = [
                {
                    "title": strip_html(p["title"]["rendered"]),
                    "url": p["link"],
                    "excerpt": truncate(strip_html(p["excerpt"]["rendered"])),
                }
                for p in top_posts
            ]

    # Build llms.txt content
    lines = []
    lines.append(f"# {site_info['name']}")
    if site_info.get("description"):
        lines.append(f"> {site_info['description']}")
    lines.append("")

    # Topics / Categories
    for cat_name, posts in category_posts.items():
        lines.append(f"## {cat_name}")
        for post in posts:
            desc = f": {post['excerpt']}" if post["excerpt"] else ""
            lines.append(f"- [{post['title']}]({post['url']}){desc}")
        lines.append("")

    # Authors
    if authors:
        lines.append("## About")
        for author in authors:
            name = author.get("name", "")
            bio = strip_html(author.get("description", ""))
            author_url = author.get("link", "")
            if bio:
                lines.append(f"- **{name}**: {bio}")
            else:
                lines.append(f"- **{name}** ({author_url})")
        lines.append("")

    llms_txt_content = "\n".join(lines)

    return {
        "site": site_info,
        "categories_count": len(categories),
        "posts_count": sum(len(posts) for posts in category_posts.values()),
        "authors_count": len(authors),
        "llms_txt": llms_txt_content,
    }


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate llms.txt from WordPress blog data."
    )
    parser.add_argument("url", help="WordPress site URL")
    parser.add_argument("--user", required=True, help="WordPress username")
    parser.add_argument("--password", required=True, help="WordPress application password")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--json", action="store_true", help="Output full result as JSON")
    args = parser.parse_args()

    try:
        result = generate_llms_txt(args.url, args.user, args.password)
    except requests.exceptions.HTTPError as e:
        error = {"error": f"HTTP error: {e}", "url": args.url}
        if args.json:
            print(json.dumps(error, indent=2))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error = {"error": str(e), "url": args.url}
        if args.json:
            print(json.dumps(error, indent=2))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result["llms_txt"])
        print(f"Generated {args.output} ({result['posts_count']} posts, {result['categories_count']} categories)")
    else:
        print(result["llms_txt"])


if __name__ == "__main__":
    main()
