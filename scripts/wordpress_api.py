#!/usr/bin/env python3
"""
WordPress REST API connector for SEO analysis.

Connects to any WordPress site via Application Password authentication
and retrieves posts, pages, categories, tags, media, and site metadata
for comprehensive SEO auditing.

Usage:
    python wordpress_api.py https://example.com --user admin --password xxxx xxxx xxxx xxxx
    python wordpress_api.py https://example.com --user admin --password xxxx --command posts --json
    python wordpress_api.py https://example.com --user admin --password xxxx --command seo-audit
    python wordpress_api.py https://example.com --check

Commands:
    info        Site metadata and WordPress detection
    posts       Retrieve all published posts with SEO data
    pages       Retrieve all published pages with SEO data
    categories  Retrieve all categories with post counts
    tags        Retrieve all tags with post counts
    media       Retrieve media library metadata
    users       Retrieve authors/users
    plugins     Retrieve active plugins (requires admin)
    seo-audit   Full SEO audit of all content
    seo-meta    Retrieve Yoast/RankMath SEO meta for all posts
    create-post Create a new post (--title, --content, --status, --categories, --tags)
    update-post Update an existing post (--post-id, --title, --content, --status)
"""

import argparse
import base64
import ipaddress
import json
import mimetypes
import os
import re
import socket
import sys
from typing import Optional
from urllib.parse import urlparse, urljoin

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

class WordPressClient:
    """WordPress REST API client with Application Password auth."""

    def __init__(self, site_url: str, username: str = None, password: str = None):
        self.site_url = site_url.rstrip("/")
        self.api_base = f"{self.site_url}/wp-json/wp/v2"
        self.username = username
        self.password = password
        self.session = requests.Session()

        # Set auth header if credentials provided
        if username and password:
            credentials = base64.b64encode(
                f"{username}:{password}".encode()
            ).decode()
            self.session.headers.update({
                "Authorization": f"Basic {credentials}"
            })

        self.session.headers.update({
            "User-Agent": "ClaudeSEO-WordPress/1.0",
            "Accept": "application/json",
        })

    def _get(self, endpoint: str, params: dict = None) -> dict | list:
        """Make GET request to WP REST API."""
        url = f"{self.api_base}/{endpoint}"
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def _get_all(self, endpoint: str, params: dict = None) -> list:
        """Paginate through all results from WP REST API."""
        if params is None:
            params = {}
        params["per_page"] = 100
        params["page"] = 1

        all_items = []
        while True:
            url = f"{self.api_base}/{endpoint}"
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 400:
                break
            response.raise_for_status()

            items = response.json()
            if not items:
                break

            all_items.extend(items)

            total_pages = int(response.headers.get("X-WP-TotalPages", 1))
            if params["page"] >= total_pages:
                break
            params["page"] += 1

        return all_items

    # ─── Detection ───────────────────────────────────────────────────────

    def check_wordpress(self) -> dict:
        """Detect if site is WordPress and get basic info."""
        result = {
            "is_wordpress": False,
            "version": None,
            "api_available": False,
            "seo_plugin": None,
            "theme": None,
            "permalink_structure": None,
            "error": None,
        }

        # Check wp-json endpoint
        try:
            response = self.session.get(
                f"{self.site_url}/wp-json/", timeout=15
            )
            if response.status_code == 200:
                data = response.json()
                result["is_wordpress"] = True
                result["api_available"] = True
                result["name"] = data.get("name", "")
                result["description"] = data.get("description", "")
                result["url"] = data.get("url", "")
                result["home"] = data.get("home", "")
                result["gmt_offset"] = data.get("gmt_offset", "")
                result["timezone_string"] = data.get("timezone_string", "")

                # Check available namespaces for SEO plugins
                namespaces = data.get("namespaces", [])
                if "yoast/v1" in namespaces:
                    result["seo_plugin"] = "yoast"
                elif "rankmath/v1" in namespaces:
                    result["seo_plugin"] = "rankmath"
                elif "aioseo/v1" in namespaces:
                    result["seo_plugin"] = "aioseo"

        except requests.exceptions.RequestException as e:
            result["error"] = str(e)

        # Fallback: check homepage for WP signals
        if not result["is_wordpress"]:
            try:
                response = self.session.get(self.site_url, timeout=15)
                html = response.text
                if any(signal in html for signal in [
                    "wp-content", "wp-includes", "wp-json",
                    "wordpress", "generator\" content=\"WordPress"
                ]):
                    result["is_wordpress"] = True
                    # Extract version from generator meta
                    match = re.search(
                        r'content="WordPress\s+([\d.]+)"', html
                    )
                    if match:
                        result["version"] = match.group(1)
            except requests.exceptions.RequestException:
                pass

        return result

    # ─── Content Retrieval ───────────────────────────────────────────────

    def get_posts(self, status: str = "publish") -> list:
        """Retrieve all posts with SEO-relevant fields."""
        posts = self._get_all("posts", {
            "status": status,
            "_fields": "id,date,modified,slug,status,title,content,excerpt,"
                       "author,categories,tags,featured_media,link,meta,"
                       "yoast_head_json,rank_math_title,rank_math_description"
        })
        return [self._enrich_post(p) for p in posts]

    def get_pages(self, status: str = "publish") -> list:
        """Retrieve all pages with SEO-relevant fields."""
        pages = self._get_all("pages", {
            "status": status,
            "_fields": "id,date,modified,slug,status,title,content,excerpt,"
                       "author,parent,featured_media,link,meta,"
                       "yoast_head_json,rank_math_title,rank_math_description"
        })
        return [self._enrich_post(p) for p in pages]

    def get_categories(self) -> list:
        """Retrieve all categories with post counts."""
        return self._get_all("categories", {
            "_fields": "id,count,name,slug,description,parent,link"
        })

    def get_tags(self) -> list:
        """Retrieve all tags with post counts."""
        return self._get_all("tags", {
            "_fields": "id,count,name,slug,description,link"
        })

    def get_media(self) -> list:
        """Retrieve media library items."""
        return self._get_all("media", {
            "_fields": "id,date,slug,title,alt_text,media_details,source_url,"
                       "mime_type,link"
        })

    def get_users(self) -> list:
        """Retrieve authors/users (public info only)."""
        return self._get_all("users", {
            "_fields": "id,name,slug,description,link,avatar_urls"
        })

    # ─── SEO Plugin Data ─────────────────────────────────────────────────

    def get_yoast_meta(self) -> list:
        """Retrieve Yoast SEO metadata for all posts."""
        posts = self._get_all("posts", {
            "_fields": "id,title,link,slug,yoast_head_json"
        })
        results = []
        for post in posts:
            yoast = post.get("yoast_head_json", {}) or {}
            results.append({
                "id": post["id"],
                "title": post.get("title", {}).get("rendered", ""),
                "link": post.get("link", ""),
                "slug": post.get("slug", ""),
                "seo_title": yoast.get("title", ""),
                "seo_description": yoast.get("description", ""),
                "canonical": yoast.get("canonical", ""),
                "og_title": yoast.get("og_title", ""),
                "og_description": yoast.get("og_description", ""),
                "og_image": (yoast.get("og_image", [{}]) or [{}])[0].get("url", ""),
                "schema": yoast.get("schema", {}),
                "robots": yoast.get("robots", {}),
            })
        return results

    def get_rankmath_meta(self) -> list:
        """Retrieve RankMath SEO metadata via REST API."""
        try:
            posts = self._get_all("posts", {
                "_fields": "id,title,link,slug,meta"
            })
            results = []
            for post in posts:
                meta = post.get("meta", {}) or {}
                results.append({
                    "id": post["id"],
                    "title": post.get("title", {}).get("rendered", ""),
                    "link": post.get("link", ""),
                    "slug": post.get("slug", ""),
                    "seo_title": meta.get("rank_math_title", ""),
                    "seo_description": meta.get("rank_math_description", ""),
                    "focus_keyword": meta.get("rank_math_focus_keyword", ""),
                    "seo_score": meta.get("rank_math_seo_score", ""),
                    "robots": meta.get("rank_math_robots", []),
                    "canonical": meta.get("rank_math_canonical_url", ""),
                })
            return results
        except Exception:
            return []

    # ─── Content Analysis Helpers ────────────────────────────────────────

    def _enrich_post(self, post: dict) -> dict:
        """Add SEO analysis fields to a post."""
        content_html = post.get("content", {}).get("rendered", "")
        title = post.get("title", {}).get("rendered", "")
        excerpt = post.get("excerpt", {}).get("rendered", "")

        # Strip HTML for word count and text analysis
        if BeautifulSoup:
            soup = BeautifulSoup(content_html, "html.parser")
            text = soup.get_text(separator=" ", strip=True)

            # Extract headings
            headings = {}
            for tag in ["h1", "h2", "h3", "h4"]:
                found = soup.find_all(tag)
                headings[tag] = [h.get_text(strip=True) for h in found]

            # Extract images
            images = []
            for img in soup.find_all("img"):
                images.append({
                    "src": img.get("src", ""),
                    "alt": img.get("alt", ""),
                    "width": img.get("width"),
                    "height": img.get("height"),
                })

            # Extract internal/external links
            links_internal = []
            links_external = []
            base_domain = urlparse(self.site_url).netloc
            for a in soup.find_all("a", href=True):
                href = a.get("href", "")
                if not href or href.startswith("#"):
                    continue
                full_url = urljoin(self.site_url, href)
                parsed = urlparse(full_url)
                link_data = {
                    "href": full_url,
                    "text": a.get_text(strip=True)[:100],
                    "rel": a.get("rel", []),
                }
                if parsed.netloc == base_domain:
                    links_internal.append(link_data)
                else:
                    links_external.append(link_data)
        else:
            text = re.sub(r"<[^>]+>", " ", content_html)
            headings = {}
            images = []
            links_internal = []
            links_external = []

        words = re.findall(r"\b\w+\b", text)
        word_count = len(words)

        # Yoast data if present
        yoast = post.get("yoast_head_json", {}) or {}

        post["_seo"] = {
            "word_count": word_count,
            "title_length": len(title),
            "excerpt_length": len(re.sub(r"<[^>]+>", "", excerpt).strip()),
            "has_excerpt": bool(excerpt.strip()),
            "headings": headings,
            "images_count": len(images),
            "images": images,
            "images_without_alt": sum(1 for img in images if not img.get("alt")),
            "internal_links": len(links_internal),
            "external_links": len(links_external),
            "links_internal": links_internal,
            "links_external": links_external,
            "seo_title": yoast.get("title", ""),
            "seo_description": yoast.get("description", ""),
            "canonical": yoast.get("canonical", ""),
            "schema_types": [
                s.get("@type", "")
                for s in yoast.get("schema", {}).get("@graph", [])
            ] if yoast.get("schema") else [],
        }

        return post

    # ─── Full SEO Audit ──────────────────────────────────────────────────

    def seo_audit(self) -> dict:
        """Run a comprehensive SEO audit of all WordPress content."""
        audit = {
            "site_info": self.check_wordpress(),
            "summary": {},
            "posts": [],
            "pages": [],
            "categories": [],
            "tags": [],
            "media_issues": [],
            "issues": {
                "critical": [],
                "high": [],
                "medium": [],
                "low": [],
            },
            "scores": {},
        }

        # Fetch all content
        try:
            posts = self.get_posts()
            pages = self.get_pages()
            categories = self.get_categories()
            tags = self.get_tags()
            media = self.get_media()
            users = self.get_users()
        except requests.exceptions.HTTPError as e:
            audit["error"] = f"API error: {e}"
            return audit

        audit["posts"] = posts
        audit["pages"] = pages
        audit["categories"] = categories
        audit["tags"] = tags

        # ─── Summary Stats ───────────────────────────────────────────
        audit["summary"] = {
            "total_posts": len(posts),
            "total_pages": len(pages),
            "total_categories": len(categories),
            "total_tags": len(tags),
            "total_media": len(media),
            "total_authors": len(users),
            "seo_plugin": audit["site_info"].get("seo_plugin", "none"),
        }

        # ─── Content Issues ──────────────────────────────────────────
        for post in posts:
            seo = post.get("_seo", {})

            # Thin content
            if seo.get("word_count", 0) < 300:
                audit["issues"]["critical"].append({
                    "type": "thin_content",
                    "post_id": post["id"],
                    "title": post.get("title", {}).get("rendered", ""),
                    "link": post.get("link", ""),
                    "word_count": seo.get("word_count", 0),
                    "message": f"Article trop court ({seo.get('word_count', 0)} mots, minimum 1500 recommande)",
                })
            elif seo.get("word_count", 0) < 1500:
                audit["issues"]["high"].append({
                    "type": "short_content",
                    "post_id": post["id"],
                    "title": post.get("title", {}).get("rendered", ""),
                    "link": post.get("link", ""),
                    "word_count": seo.get("word_count", 0),
                    "message": f"Article court ({seo.get('word_count', 0)} mots, minimum 1500 recommande)",
                })

            # Missing meta description
            if not seo.get("seo_description"):
                audit["issues"]["high"].append({
                    "type": "missing_meta_description",
                    "post_id": post["id"],
                    "title": post.get("title", {}).get("rendered", ""),
                    "link": post.get("link", ""),
                    "message": "Meta description manquante",
                })

            # Missing excerpt
            if not seo.get("has_excerpt"):
                audit["issues"]["medium"].append({
                    "type": "missing_excerpt",
                    "post_id": post["id"],
                    "title": post.get("title", {}).get("rendered", ""),
                    "link": post.get("link", ""),
                    "message": "Extrait (excerpt) non renseigne",
                })

            # Images without alt text
            if seo.get("images_without_alt", 0) > 0:
                audit["issues"]["medium"].append({
                    "type": "images_missing_alt",
                    "post_id": post["id"],
                    "title": post.get("title", {}).get("rendered", ""),
                    "link": post.get("link", ""),
                    "count": seo.get("images_without_alt", 0),
                    "message": f"{seo.get('images_without_alt', 0)} image(s) sans attribut alt",
                })

            # No internal links
            if seo.get("internal_links", 0) == 0:
                audit["issues"]["high"].append({
                    "type": "no_internal_links",
                    "post_id": post["id"],
                    "title": post.get("title", {}).get("rendered", ""),
                    "link": post.get("link", ""),
                    "message": "Aucun lien interne (article orphelin)",
                })

            # Poor heading structure
            headings = seo.get("headings", {})
            if not headings.get("h2"):
                audit["issues"]["medium"].append({
                    "type": "no_h2_headings",
                    "post_id": post["id"],
                    "title": post.get("title", {}).get("rendered", ""),
                    "link": post.get("link", ""),
                    "message": "Aucun sous-titre H2 (structure pauvre)",
                })

            # Title too long or too short
            title_len = seo.get("title_length", 0)
            if title_len > 60:
                audit["issues"]["medium"].append({
                    "type": "title_too_long",
                    "post_id": post["id"],
                    "title": post.get("title", {}).get("rendered", ""),
                    "link": post.get("link", ""),
                    "message": f"Titre trop long ({title_len} chars, max 60 recommande)",
                })
            elif title_len < 20:
                audit["issues"]["medium"].append({
                    "type": "title_too_short",
                    "post_id": post["id"],
                    "title": post.get("title", {}).get("rendered", ""),
                    "link": post.get("link", ""),
                    "message": f"Titre trop court ({title_len} chars, min 20 recommande)",
                })

            # No featured image
            if not post.get("featured_media"):
                audit["issues"]["low"].append({
                    "type": "no_featured_image",
                    "post_id": post["id"],
                    "title": post.get("title", {}).get("rendered", ""),
                    "link": post.get("link", ""),
                    "message": "Pas d'image mise en avant (important pour OG/social)",
                })

        # ─── Category/Tag Issues ─────────────────────────────────────
        for cat in categories:
            if not cat.get("description"):
                audit["issues"]["low"].append({
                    "type": "category_no_description",
                    "name": cat.get("name", ""),
                    "slug": cat.get("slug", ""),
                    "message": f"Categorie '{cat.get('name', '')}' sans description",
                })
            if cat.get("count", 0) == 0:
                audit["issues"]["medium"].append({
                    "type": "empty_category",
                    "name": cat.get("name", ""),
                    "slug": cat.get("slug", ""),
                    "message": f"Categorie '{cat.get('name', '')}' vide (0 articles)",
                })

        # Unused tags
        for tag in tags:
            if tag.get("count", 0) <= 1:
                audit["issues"]["low"].append({
                    "type": "underused_tag",
                    "name": tag.get("name", ""),
                    "slug": tag.get("slug", ""),
                    "count": tag.get("count", 0),
                    "message": f"Tag '{tag.get('name', '')}' sous-utilise ({tag.get('count', 0)} article(s))",
                })

        # ─── Media Issues ────────────────────────────────────────────
        for item in media:
            details = item.get("media_details", {})
            file_size = details.get("filesize", 0)
            if file_size and int(file_size) > 500_000:
                audit["media_issues"].append({
                    "type": "large_image",
                    "id": item["id"],
                    "url": item.get("source_url", ""),
                    "size_kb": round(int(file_size) / 1024),
                    "message": f"Image trop lourde ({round(int(file_size) / 1024)} KB)",
                })
            if not item.get("alt_text"):
                audit["media_issues"].append({
                    "type": "missing_alt_media",
                    "id": item["id"],
                    "url": item.get("source_url", ""),
                    "title": item.get("title", {}).get("rendered", ""),
                    "message": "Image sans texte alternatif dans la mediatheque",
                })

        # ─── Scoring ─────────────────────────────────────────────────
        total_content = len(posts) + len(pages)
        if total_content > 0:
            issues_count = (
                len(audit["issues"]["critical"]) * 4
                + len(audit["issues"]["high"]) * 2
                + len(audit["issues"]["medium"])
                + len(audit["issues"]["low"]) * 0.5
            )
            raw_score = max(0, 100 - (issues_count / total_content * 10))
            audit["scores"]["overall"] = round(min(100, raw_score))

            # Sub-scores
            posts_with_good_wc = sum(
                1 for p in posts if p.get("_seo", {}).get("word_count", 0) >= 1500
            )
            audit["scores"]["content_depth"] = round(
                (posts_with_good_wc / len(posts) * 100) if posts else 0
            )

            posts_with_meta = sum(
                1 for p in posts if p.get("_seo", {}).get("seo_description")
            )
            audit["scores"]["meta_optimization"] = round(
                (posts_with_meta / len(posts) * 100) if posts else 0
            )

            posts_with_links = sum(
                1 for p in posts if p.get("_seo", {}).get("internal_links", 0) > 0
            )
            audit["scores"]["internal_linking"] = round(
                (posts_with_links / len(posts) * 100) if posts else 0
            )

            posts_with_images_ok = sum(
                1 for p in posts
                if p.get("_seo", {}).get("images_without_alt", 0) == 0
                and p.get("_seo", {}).get("images_count", 0) > 0
            )
            audit["scores"]["image_optimization"] = round(
                (posts_with_images_ok / len(posts) * 100) if posts else 0
            )

        return audit

    # ─── Post Creation & Publishing ────────────────────────────────────────

    def _post(self, endpoint: str, data: dict = None, files: dict = None,
              headers: dict = None) -> dict:
        """Make POST request to WP REST API."""
        url = f"{self.api_base}/{endpoint}"
        if files:
            response = self.session.post(
                url, data=data, files=files, headers=headers, timeout=60
            )
        else:
            response = self.session.post(url, json=data, timeout=30)
        response.raise_for_status()
        return response.json()

    def create_post(self, title: str, content: str, status: str = 'draft',
                    categories: list = None, tags: list = None,
                    meta: dict = None) -> dict:
        """Create a new WordPress post via POST /wp/v2/posts.

        Args:
            title: Post title.
            content: Post HTML content.
            status: 'draft', 'publish', or 'future'.
            categories: List of category IDs.
            tags: List of tag IDs.
            meta: Dict of post meta fields (for SEO plugins, etc.).

        Returns:
            Created post data dict with id, link, status.
        """
        data = {
            "title": title,
            "content": content,
            "status": status,
        }
        if categories:
            data["categories"] = categories
        if tags:
            data["tags"] = tags
        if meta:
            data["meta"] = meta
        return self._post("posts", data)

    def update_post(self, post_id: int, data: dict) -> dict:
        """Update an existing post via POST /wp/v2/posts/{id}.

        Args:
            post_id: The WordPress post ID to update.
            data: Dict of fields to update (title, content, status, meta, etc.).

        Returns:
            Updated post data dict.
        """
        url = f"{self.api_base}/posts/{post_id}"
        response = self.session.post(url, json=data, timeout=30)
        response.raise_for_status()
        return response.json()

    def upload_media(self, file_path: str, alt_text: str = '') -> dict:
        """Upload an image to the WordPress media library via POST /wp/v2/media.

        Args:
            file_path: Local path to the image file.
            alt_text: Alt text for the image (SEO).

        Returns:
            Media object dict with id, source_url, etc.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Media file not found: {file_path}")

        filename = os.path.basename(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "application/octet-stream"

        with open(file_path, "rb") as f:
            file_data = f.read()

        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": mime_type,
        }
        url = f"{self.api_base}/media"
        response = self.session.post(url, data=file_data, headers=headers, timeout=60)
        response.raise_for_status()
        media = response.json()

        # Set alt text if provided
        if alt_text and media.get("id"):
            self.update_media_alt(media["id"], alt_text)

        return media

    def update_media_alt(self, media_id: int, alt_text: str) -> dict:
        """Update alt text on an existing media item."""
        url = f"{self.api_base}/media/{media_id}"
        response = self.session.post(url, json={"alt_text": alt_text}, timeout=15)
        response.raise_for_status()
        return response.json()

    def set_seo_meta(self, post_id: int, seo_title: str,
                     seo_description: str, focus_keyword: str = '') -> dict:
        """Set Yoast or RankMath SEO meta on a post.

        Auto-detects which SEO plugin is active and sets meta accordingly.

        Args:
            post_id: The WordPress post ID.
            seo_title: SEO title (title tag).
            seo_description: Meta description.
            focus_keyword: Primary focus keyword.

        Returns:
            Updated post data dict.
        """
        info = self.check_wordpress()
        seo_plugin = info.get("seo_plugin")

        meta = {}
        if seo_plugin == "yoast":
            meta = {
                "_yoast_wpseo_title": seo_title,
                "_yoast_wpseo_metadesc": seo_description,
            }
            if focus_keyword:
                meta["_yoast_wpseo_focuskw"] = focus_keyword
        elif seo_plugin == "rankmath":
            meta = {
                "rank_math_title": seo_title,
                "rank_math_description": seo_description,
            }
            if focus_keyword:
                meta["rank_math_focus_keyword"] = focus_keyword
        else:
            # Fallback: set standard WP meta (may not render without plugin)
            meta = {
                "_seo_title": seo_title,
                "_seo_description": seo_description,
            }

        return self.update_post(post_id, {"meta": meta})

    def get_or_create_category(self, name: str) -> int:
        """Get a category ID by name, or create it if it doesn't exist.

        Args:
            name: Category name to find or create.

        Returns:
            Category ID (int).
        """
        # Search for existing category
        categories = self._get("categories", {"search": name, "per_page": 100})
        for cat in categories:
            if cat.get("name", "").lower() == name.lower():
                return cat["id"]

        # Create new category
        result = self._post("categories", {"name": name})
        return result["id"]

    def get_or_create_tag(self, name: str) -> int:
        """Get a tag ID by name, or create it if it doesn't exist.

        Args:
            name: Tag name to find or create.

        Returns:
            Tag ID (int).
        """
        # Search for existing tag
        tags = self._get("tags", {"search": name, "per_page": 100})
        for tag in tags:
            if tag.get("name", "").lower() == name.lower():
                return tag["id"]

        # Create new tag
        result = self._post("tags", {"name": name})
        return result["id"]

    # ─── Internal Linking Matrix ─────────────────────────────────────────

    def internal_linking_matrix(self) -> dict:
        """Build internal linking matrix to find orphan pages and link gaps."""
        posts = self.get_posts()
        pages = self.get_pages()
        all_content = posts + pages

        url_to_title = {}
        url_links_to = {}
        url_linked_from = {}

        for item in all_content:
            link = item.get("link", "")
            title = item.get("title", {}).get("rendered", "")
            url_to_title[link] = title
            internal = item.get("_seo", {}).get("links_internal", [])
            outgoing = [l["href"] for l in internal]
            url_links_to[link] = outgoing

            for target in outgoing:
                if target not in url_linked_from:
                    url_linked_from[target] = []
                url_linked_from[target].append(link)

        # Find orphans (no incoming links)
        orphans = []
        for link, title in url_to_title.items():
            if link not in url_linked_from or len(url_linked_from[link]) == 0:
                orphans.append({"url": link, "title": title})

        # Find pages with no outgoing links
        no_outgoing = []
        for link, targets in url_links_to.items():
            if len(targets) == 0:
                no_outgoing.append({
                    "url": link,
                    "title": url_to_title.get(link, ""),
                })

        return {
            "total_content": len(all_content),
            "orphan_pages": orphans,
            "no_outgoing_links": no_outgoing,
            "link_matrix": {
                url: {
                    "title": url_to_title.get(url, ""),
                    "outgoing": len(targets),
                    "incoming": len(url_linked_from.get(url, [])),
                }
                for url, targets in url_links_to.items()
            },
        }


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="WordPress REST API connector for SEO analysis"
    )
    parser.add_argument("url", help="WordPress site URL")
    parser.add_argument("--user", "-u", help="WordPress username")
    parser.add_argument("--password", "-p", help="Application password")
    parser.add_argument(
        "--command", "-c",
        default="info",
        choices=[
            "info", "check", "posts", "pages", "categories", "tags",
            "media", "users", "seo-audit", "seo-meta", "linking-matrix",
            "create-post", "update-post"
        ],
        help="Command to execute (default: info)"
    )
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--check", action="store_true", help="Just check if site is WordPress")
    parser.add_argument("--post-id", type=int, help="Post ID (for update-post command)")
    parser.add_argument("--title", help="Post title (for create-post)")
    parser.add_argument("--content", help="Post HTML content or path to .html file (for create-post)")
    parser.add_argument("--status", default="draft", choices=["draft", "publish", "future"],
                        help="Post status (default: draft)")
    parser.add_argument("--categories", nargs="*", help="Category names (for create-post)")
    parser.add_argument("--tags", nargs="*", help="Tag names (for create-post)")

    args = parser.parse_args()

    # Validate URL
    try:
        url = validate_url(args.url)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    client = WordPressClient(url, args.user, args.password)

    if args.check or args.command == "check":
        result = client.check_wordpress()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["is_wordpress"]:
                print(f"WordPress detected: {url}")
                print(f"  API available: {result['api_available']}")
                print(f"  SEO plugin: {result.get('seo_plugin', 'none')}")
                print(f"  Site name: {result.get('name', 'N/A')}")
            else:
                print(f"Not a WordPress site: {url}")
        sys.exit(0 if result["is_wordpress"] else 1)

    command = args.command

    if command == "info":
        result = client.check_wordpress()
    elif command == "posts":
        result = client.get_posts()
    elif command == "pages":
        result = client.get_pages()
    elif command == "categories":
        result = client.get_categories()
    elif command == "tags":
        result = client.get_tags()
    elif command == "media":
        result = client.get_media()
    elif command == "users":
        result = client.get_users()
    elif command == "seo-audit":
        result = client.seo_audit()
    elif command == "seo-meta":
        info = client.check_wordpress()
        if info.get("seo_plugin") == "yoast":
            result = client.get_yoast_meta()
        elif info.get("seo_plugin") == "rankmath":
            result = client.get_rankmath_meta()
        else:
            result = {"error": "No supported SEO plugin detected (Yoast or RankMath required)"}
    elif command == "linking-matrix":
        result = client.internal_linking_matrix()
    elif command == "create-post":
        if not args.title:
            print("Error: --title is required for create-post", file=sys.stderr)
            sys.exit(1)
        content = args.content or ""
        # If content is a file path, read it
        if content and os.path.isfile(content):
            with open(content, "r", encoding="utf-8") as f:
                content = f.read()
        # Resolve category and tag names to IDs
        cat_ids = []
        if args.categories:
            for name in args.categories:
                cat_ids.append(client.get_or_create_category(name))
        tag_ids = []
        if args.tags:
            for name in args.tags:
                tag_ids.append(client.get_or_create_tag(name))
        result = client.create_post(
            title=args.title,
            content=content,
            status=args.status,
            categories=cat_ids,
            tags=tag_ids,
        )
        # Print summary for non-JSON output
        if not args.json:
            print(f"Post created successfully!")
            print(f"  ID:     {result.get('id')}")
            print(f"  Status: {result.get('status')}")
            print(f"  Link:   {result.get('link', 'N/A')}")
            sys.exit(0)
    elif command == "update-post":
        if not args.post_id:
            print("Error: --post-id is required for update-post", file=sys.stderr)
            sys.exit(1)
        data = {}
        if args.title:
            data["title"] = args.title
        if args.content:
            content = args.content
            if os.path.isfile(content):
                with open(content, "r", encoding="utf-8") as f:
                    content = f.read()
            data["content"] = content
        if args.status:
            data["status"] = args.status
        if args.categories:
            data["categories"] = [client.get_or_create_category(n) for n in args.categories]
        if args.tags:
            data["tags"] = [client.get_or_create_tag(n) for n in args.tags]
        if not data:
            print("Error: provide at least one field to update (--title, --content, --status, --categories, --tags)",
                  file=sys.stderr)
            sys.exit(1)
        result = client.update_post(args.post_id, data)
        if not args.json:
            print(f"Post updated successfully!")
            print(f"  ID:     {result.get('id')}")
            print(f"  Status: {result.get('status')}")
            print(f"  Link:   {result.get('link', 'N/A')}")
            sys.exit(0)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        # Remove heavy HTML content for JSON output
        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    if "content" in item:
                        item.pop("content", None)
        print(json.dumps(result, indent=2, default=str))
    else:
        if isinstance(result, dict) and "error" in result and result["error"]:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)

        if command == "seo-audit":
            _print_audit_report(result)
        elif isinstance(result, list):
            print(f"Total: {len(result)} items")
            for item in result[:10]:
                title = item.get("title", {})
                if isinstance(title, dict):
                    title = title.get("rendered", "")
                print(f"  - {title}")
            if len(result) > 10:
                print(f"  ... and {len(result) - 10} more")
        else:
            print(json.dumps(result, indent=2, default=str))


def _print_audit_report(audit: dict):
    """Print a formatted SEO audit report."""
    info = audit.get("site_info", {})
    summary = audit.get("summary", {})
    scores = audit.get("scores", {})
    issues = audit.get("issues", {})

    print("=" * 60)
    print(f"  SEO AUDIT: {info.get('name', info.get('url', 'Unknown'))}")
    print("=" * 60)
    print()

    print(f"  Plugin SEO: {summary.get('seo_plugin', 'aucun')}")
    print(f"  Articles:   {summary.get('total_posts', 0)}")
    print(f"  Pages:      {summary.get('total_pages', 0)}")
    print(f"  Categories: {summary.get('total_categories', 0)}")
    print(f"  Tags:       {summary.get('total_tags', 0)}")
    print(f"  Medias:     {summary.get('total_media', 0)}")
    print(f"  Auteurs:    {summary.get('total_authors', 0)}")
    print()

    print("  SCORES")
    print(f"  Score global:       {scores.get('overall', 'N/A')}/100")
    print(f"  Profondeur contenu: {scores.get('content_depth', 'N/A')}%")
    print(f"  Meta optimisation:  {scores.get('meta_optimization', 'N/A')}%")
    print(f"  Maillage interne:   {scores.get('internal_linking', 'N/A')}%")
    print(f"  Images:             {scores.get('image_optimization', 'N/A')}%")
    print()

    for level in ["critical", "high", "medium", "low"]:
        items = issues.get(level, [])
        if items:
            label = {"critical": "CRITIQUE", "high": "IMPORTANT",
                     "medium": "MOYEN", "low": "MINEUR"}[level]
            print(f"  [{label}] ({len(items)} problemes)")
            for item in items[:5]:
                print(f"    - {item.get('message', '')}")
                if item.get("title"):
                    print(f"      Article: {item['title']}")
            if len(items) > 5:
                print(f"    ... et {len(items) - 5} autres")
            print()


if __name__ == "__main__":
    main()
