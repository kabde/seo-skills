#!/usr/bin/env python3
"""
GEO Readiness Analyzer - AI/LLM citation readiness checker.

Analyzes blog content for Generative Engine Optimization (GEO) readiness.
Checks passage citability, definition patterns, quotable facts, AI crawler
access, llms.txt presence, and author schema markup.

Usage:
    python georeadiness_analyzer.py https://example.com/blog-post
    python georeadiness_analyzer.py https://example.com/blog-post --json
    python georeadiness_analyzer.py page.html --json
"""

import argparse
import ipaddress
import json
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
    print("Error: beautifulsoup4 library required. Install with: pip install beautifulsoup4")
    sys.exit(1)


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


# ─── Constants ───────────────────────────────────────────────────────────────

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 ClaudeSEO/2.0"
)

OPTIMAL_PASSAGE_MIN = 134
OPTIMAL_PASSAGE_MAX = 167

DEFINITION_PATTERNS = [
    r"\b\w[\w\s]{2,30}\bis\b",
    r"\b\w[\w\s]{2,30}\brefers?\s+to\b",
    r"\b\w[\w\s]{2,30}\bmeans?\b",
    r"\b\w[\w\s]{2,30}\bcan\s+be\s+defined\s+as\b",
    r"\b\w[\w\s]{2,30}\bis\s+defined\s+as\b",
    r"\b\w[\w\s]{2,30}\bis\s+a\s+type\s+of\b",
]

AI_CRAWLERS = ["GPTBot", "OAI-SearchBot", "ClaudeBot", "PerplexityBot", "CCBot"]


# ─── Fetching ────────────────────────────────────────────────────────────────

def fetch_html(source: str) -> tuple:
    """Fetch HTML from URL or local file. Returns (html_content, base_url)."""
    if os.path.isfile(source):
        with open(source, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(), None

    url = validate_url(source)
    headers = {"User-Agent": DEFAULT_USER_AGENT}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text, url


def fetch_robots_txt(base_url: str) -> Optional[str]:
    """Fetch robots.txt from the site root."""
    if not base_url:
        return None
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    try:
        resp = requests.get(robots_url, headers={"User-Agent": DEFAULT_USER_AGENT}, timeout=15)
        if resp.status_code == 200:
            return resp.text
    except Exception:
        pass
    return None


def fetch_llms_txt(base_url: str) -> Optional[str]:
    """Check for llms.txt at site root."""
    if not base_url:
        return None
    parsed = urlparse(base_url)
    llms_url = f"{parsed.scheme}://{parsed.netloc}/llms.txt"
    try:
        resp = requests.get(llms_url, headers={"User-Agent": DEFAULT_USER_AGENT}, timeout=15)
        if resp.status_code == 200 and len(resp.text.strip()) > 10:
            return resp.text
    except Exception:
        pass
    return None


# ─── Section Analysis ────────────────────────────────────────────────────────

def extract_h2_sections(soup: BeautifulSoup) -> list:
    """Extract content sections split by H2 headings."""
    sections = []
    content_area = soup.find("article") or soup.find("main") or soup.find("body")
    if not content_area:
        return sections

    current_heading = None
    current_paragraphs = []

    for element in content_area.find_all(["h2", "p", "ul", "ol", "blockquote"]):
        if element.name == "h2":
            if current_heading is not None:
                sections.append({
                    "heading": current_heading,
                    "text": " ".join(current_paragraphs),
                })
            current_heading = element.get_text(strip=True)
            current_paragraphs = []
        elif current_heading is not None:
            text = element.get_text(strip=True)
            if text:
                current_paragraphs.append(text)

    if current_heading is not None and current_paragraphs:
        sections.append({
            "heading": current_heading,
            "text": " ".join(current_paragraphs),
        })

    return sections


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def has_definition_pattern(text: str) -> bool:
    """Check if text contains definition-style sentences."""
    for pattern in DEFINITION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def count_quotable_facts(text: str) -> int:
    """Count sentences containing numbers, statistics, dates, or percentages."""
    sentences = re.split(r'[.!?]+', text)
    count = 0
    for s in sentences:
        if re.search(r'\d+%|\d{4}|\$[\d,.]+|\d+\s*(million|billion|thousand|percent)', s, re.IGNORECASE):
            count += 1
        elif re.search(r'\b\d+\.\d+\b', s):
            count += 1
    return count


def is_self_contained(text: str) -> bool:
    """Check if a passage answers a question without needing external context."""
    words = count_words(text)
    if words < 40:
        return False
    # Should not start with pronouns or references to other sections
    starts_with_reference = re.match(r'^(This|These|That|Those|It|They|As mentioned|As noted)', text)
    if starts_with_reference:
        return False
    # Should contain at least one complete statement
    sentences = re.split(r'[.!?]+', text)
    complete_sentences = [s.strip() for s in sentences if count_words(s.strip()) >= 8]
    return len(complete_sentences) >= 2


def analyze_section(section: dict) -> dict:
    """Analyze a single H2 section for citability."""
    text = section["text"]
    word_count = count_words(text)

    # Passage length score
    if OPTIMAL_PASSAGE_MIN <= word_count <= OPTIMAL_PASSAGE_MAX:
        passage_score = 100
    elif word_count < OPTIMAL_PASSAGE_MIN:
        passage_score = max(0, int((word_count / OPTIMAL_PASSAGE_MIN) * 80))
    else:
        overshoot = word_count - OPTIMAL_PASSAGE_MAX
        passage_score = max(40, 100 - int(overshoot * 0.3))

    has_definition = has_definition_pattern(text)
    quotable_facts = count_quotable_facts(text)
    self_contained = is_self_contained(text)

    # Question-style heading bonus
    heading = section["heading"]
    is_question_heading = heading.strip().endswith("?") or heading.lower().startswith(
        ("what", "how", "why", "when", "where", "who", "which", "can", "should", "is", "are", "do", "does")
    )

    # Section citability score (0-100)
    score = 0
    score += min(35, passage_score * 0.35)
    score += 20 if has_definition else 0
    score += min(20, quotable_facts * 10)
    score += 15 if self_contained else 0
    score += 10 if is_question_heading else 0
    score = min(100, int(score))

    recommendations = []
    if word_count < OPTIMAL_PASSAGE_MIN:
        recommendations.append(f"Expand section to {OPTIMAL_PASSAGE_MIN}-{OPTIMAL_PASSAGE_MAX} words (currently {word_count})")
    elif word_count > OPTIMAL_PASSAGE_MAX * 2:
        recommendations.append(f"Split into smaller subsections for better AI citability ({word_count} words)")
    if not has_definition:
        recommendations.append("Add a clear definition sentence (e.g., 'X is...', 'X refers to...')")
    if quotable_facts == 0:
        recommendations.append("Add specific numbers, statistics, or dates for quotable facts")
    if not self_contained:
        recommendations.append("Make passage self-contained: avoid starting with 'This', 'These', pronouns")
    if not is_question_heading:
        recommendations.append("Consider rephrasing heading as a question for better AI matching")

    return {
        "heading": heading,
        "word_count": word_count,
        "citability_score": score,
        "passage_length_optimal": OPTIMAL_PASSAGE_MIN <= word_count <= OPTIMAL_PASSAGE_MAX,
        "has_definition_pattern": has_definition,
        "quotable_facts_count": quotable_facts,
        "is_self_contained": self_contained,
        "is_question_heading": is_question_heading,
        "recommendations": recommendations,
    }


# ─── Robots.txt Analysis ────────────────────────────────────────────────────

def analyze_robots(robots_txt: Optional[str]) -> dict:
    """Analyze robots.txt for AI crawler access."""
    result = {
        "found": robots_txt is not None,
        "crawlers": {},
    }

    if not robots_txt:
        for crawler in AI_CRAWLERS:
            result["crawlers"][crawler] = "no_robots_txt"
        return result

    lines = robots_txt.split("\n")
    current_agent = None

    agent_rules = {}
    for line in lines:
        line = line.strip()
        if line.lower().startswith("user-agent:"):
            current_agent = line.split(":", 1)[1].strip()
            if current_agent not in agent_rules:
                agent_rules[current_agent] = []
        elif current_agent and line.lower().startswith(("allow:", "disallow:")):
            agent_rules[current_agent] = agent_rules.get(current_agent, [])
            agent_rules[current_agent].append(line)

    for crawler in AI_CRAWLERS:
        if crawler in agent_rules:
            rules = agent_rules[crawler]
            has_disallow_all = any("disallow: /" == r.lower().strip() or "disallow:/" == r.lower().strip().replace(" ", "") for r in rules)
            if has_disallow_all:
                result["crawlers"][crawler] = "blocked"
            else:
                result["crawlers"][crawler] = "allowed"
        elif "*" in agent_rules:
            rules = agent_rules["*"]
            has_disallow_all = any("disallow: /" == r.lower().strip() or "disallow:/" == r.lower().strip().replace(" ", "") for r in rules)
            if has_disallow_all:
                result["crawlers"][crawler] = "blocked_by_wildcard"
            else:
                result["crawlers"][crawler] = "allowed"
        else:
            result["crawlers"][crawler] = "allowed"

    return result


# ─── Schema Analysis ────────────────────────────────────────────────────────

def check_author_schema(soup: BeautifulSoup) -> dict:
    """Check for Person schema markup (author E-E-A-T signal)."""
    result = {
        "has_author_schema": False,
        "author_name": None,
        "author_url": None,
        "schema_types_found": [],
    }

    # Check JSON-LD scripts
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string)
            items = data if isinstance(data, list) else [data]
            for item in items:
                schema_type = item.get("@type", "")
                if schema_type:
                    if isinstance(schema_type, list):
                        result["schema_types_found"].extend(schema_type)
                    else:
                        result["schema_types_found"].append(schema_type)

                # Check for author in BlogPosting/Article
                author = item.get("author")
                if author:
                    if isinstance(author, dict) and author.get("@type") == "Person":
                        result["has_author_schema"] = True
                        result["author_name"] = author.get("name")
                        result["author_url"] = author.get("url")
                    elif isinstance(author, list):
                        for a in author:
                            if isinstance(a, dict) and a.get("@type") == "Person":
                                result["has_author_schema"] = True
                                result["author_name"] = a.get("name")
                                result["author_url"] = a.get("url")
                                break
        except (json.JSONDecodeError, TypeError):
            continue

    return result


# ─── Main GEO Analysis ──────────────────────────────────────────────────────

def analyze_geo_readiness(source: str) -> dict:
    """Run full GEO readiness analysis on a URL or HTML file."""
    html, base_url = fetch_html(source)
    soup = BeautifulSoup(html, "html.parser")

    # 1. Section-level citability
    sections = extract_h2_sections(soup)
    section_results = [analyze_section(s) for s in sections]

    # 2. llms.txt check
    llms_txt = fetch_llms_txt(base_url) if base_url else None

    # 3. Robots.txt / AI crawler access
    robots_txt = fetch_robots_txt(base_url) if base_url else None
    robots_analysis = analyze_robots(robots_txt)

    # 4. Author schema
    author_schema = check_author_schema(soup)

    # ─── Scoring ─────────────────────────────────────────────────────
    # Citability (40%)
    if section_results:
        avg_citability = sum(s["citability_score"] for s in section_results) / len(section_results)
    else:
        avg_citability = 0
    citability_score = avg_citability * 0.40

    # AI Crawler Access (20%)
    crawler_statuses = list(robots_analysis["crawlers"].values())
    allowed_count = sum(1 for s in crawler_statuses if "allowed" in s)
    crawler_score = (allowed_count / max(1, len(crawler_statuses))) * 100 * 0.20

    # llms.txt (15%)
    llms_score = 100 * 0.15 if llms_txt else 0

    # Author Schema (15%)
    schema_score = 100 * 0.15 if author_schema["has_author_schema"] else 0

    # Structural quality (10%) - H2 count, question headings
    h2_count = len(section_results)
    question_headings = sum(1 for s in section_results if s["is_question_heading"])
    structural = 0
    if h2_count >= 3:
        structural += 50
    elif h2_count >= 1:
        structural += 25
    if h2_count > 0 and question_headings / h2_count >= 0.3:
        structural += 50
    structural_score = structural * 0.10

    total_score = int(citability_score + crawler_score + llms_score + schema_score + structural_score)
    total_score = max(0, min(100, total_score))

    # ─── Global recommendations ──────────────────────────────────────
    global_recommendations = []
    if not llms_txt:
        global_recommendations.append("Create /llms.txt to help AI systems understand your site content")
    blocked_crawlers = [c for c, s in robots_analysis["crawlers"].items() if "blocked" in s]
    if blocked_crawlers:
        global_recommendations.append(f"Unblock AI crawlers in robots.txt: {', '.join(blocked_crawlers)}")
    if not author_schema["has_author_schema"]:
        global_recommendations.append("Add Person schema for the author to strengthen E-E-A-T signals")
    if h2_count < 3:
        global_recommendations.append("Add more H2 sections (at least 3) to improve content structure")
    low_sections = [s for s in section_results if s["citability_score"] < 50]
    if low_sections:
        global_recommendations.append(
            f"{len(low_sections)} section(s) have low citability scores (<50). "
            "Review per-section recommendations to improve."
        )

    return {
        "source": source,
        "geo_readiness_score": total_score,
        "score_breakdown": {
            "citability": round(citability_score, 1),
            "ai_crawler_access": round(crawler_score, 1),
            "llms_txt": round(llms_score, 1),
            "author_schema": round(schema_score, 1),
            "structural_quality": round(structural_score, 1),
        },
        "sections_analyzed": len(section_results),
        "sections": section_results,
        "llms_txt": {
            "present": llms_txt is not None,
            "length": len(llms_txt) if llms_txt else 0,
        },
        "robots_txt": robots_analysis,
        "author_schema": author_schema,
        "recommendations": global_recommendations,
    }


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Analyze blog content for AI/LLM citation readiness (GEO)."
    )
    parser.add_argument("source", help="URL or path to HTML file to analyze")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    try:
        result = analyze_geo_readiness(args.source)
    except Exception as e:
        error = {"error": str(e), "source": args.source}
        if args.json:
            print(json.dumps(error, indent=2))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"GEO Readiness Score: {result['geo_readiness_score']}/100")
        print(f"{'='*60}")
        print(f"\nSource: {result['source']}")
        print(f"Sections analyzed: {result['sections_analyzed']}")
        print(f"\nScore Breakdown:")
        for key, val in result["score_breakdown"].items():
            print(f"  {key}: {val}")
        print(f"\nllms.txt: {'Present' if result['llms_txt']['present'] else 'MISSING'}")
        print(f"\nAI Crawler Access:")
        for crawler, status in result["robots_txt"]["crawlers"].items():
            icon = "OK" if "allowed" in status else "BLOCKED"
            print(f"  {crawler}: {icon}")
        print(f"\nAuthor Schema: {'Found' if result['author_schema']['has_author_schema'] else 'MISSING'}")
        if result["author_schema"]["author_name"]:
            print(f"  Author: {result['author_schema']['author_name']}")
        print(f"\nRecommendations:")
        for i, rec in enumerate(result["recommendations"], 1):
            print(f"  {i}. {rec}")
        if result["sections"]:
            print(f"\nPer-Section Analysis:")
            for s in result["sections"]:
                print(f"\n  [{s['citability_score']}/100] {s['heading']}")
                print(f"    Words: {s['word_count']} | Definition: {'Yes' if s['has_definition_pattern'] else 'No'} | Facts: {s['quotable_facts_count']} | Self-contained: {'Yes' if s['is_self_contained'] else 'No'}")
                for rec in s["recommendations"]:
                    print(f"    -> {rec}")


if __name__ == "__main__":
    main()
