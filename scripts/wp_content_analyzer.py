#!/usr/bin/env python3
"""
WordPress content deep analyzer for SEO.

Performs advanced content analysis on WordPress posts retrieved via REST API:
- Readability scoring (Flesch Reading Ease)
- Keyword density analysis
- Content freshness assessment
- Duplicate/cannibalizing title detection
- Topic cluster mapping
- E-E-A-T signal detection
- AI content quality markers

Usage:
    python wp_content_analyzer.py https://example.com --user admin --password xxxx --json
    python wp_content_analyzer.py https://example.com --user admin --password xxxx --command readability
    python wp_content_analyzer.py https://example.com --user admin --password xxxx --command duplicates
    python wp_content_analyzer.py https://example.com --user admin --password xxxx --command freshness
    python wp_content_analyzer.py https://example.com --user admin --password xxxx --command clusters
"""

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

# Import WordPress client
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from wordpress_api import WordPressClient, validate_url

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 required. Install with: pip install beautifulsoup4")
    sys.exit(1)


# ─── Readability Analysis ───────────────────────────────────────────────────

def count_syllables(word: str) -> int:
    """Estimate syllable count for a word (English approximation)."""
    word = word.lower().strip()
    if not word:
        return 0
    if len(word) <= 3:
        return 1

    # Remove trailing e
    if word.endswith("e"):
        word = word[:-1]

    # Count vowel groups
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel

    return max(1, count)


def flesch_reading_ease(text: str) -> dict:
    """Calculate Flesch Reading Ease score."""
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    words = re.findall(r"\b\w+\b", text)

    if not words or not sentences:
        return {"score": 0, "grade": "N/A", "sentences": 0, "words": 0}

    total_syllables = sum(count_syllables(w) for w in words)
    avg_sentence_length = len(words) / len(sentences)
    avg_syllables_per_word = total_syllables / len(words)

    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    score = max(0, min(100, score))

    if score >= 90:
        grade = "Tres facile (niveau primaire)"
    elif score >= 80:
        grade = "Facile (niveau 6e)"
    elif score >= 70:
        grade = "Assez facile (niveau 5e)"
    elif score >= 60:
        grade = "Standard (niveau 4e-3e)"
    elif score >= 50:
        grade = "Assez difficile (niveau lycee)"
    elif score >= 30:
        grade = "Difficile (niveau universitaire)"
    else:
        grade = "Tres difficile (niveau expert)"

    return {
        "score": round(score, 1),
        "grade": grade,
        "sentences": len(sentences),
        "words": len(words),
        "avg_sentence_length": round(avg_sentence_length, 1),
        "avg_syllables_per_word": round(avg_syllables_per_word, 2),
    }


# ─── Keyword Density ────────────────────────────────────────────────────────

def analyze_keyword_density(text: str, top_n: int = 20) -> dict:
    """Analyze keyword density and find dominant terms."""
    # Common French + English stop words
    stop_words = {
        "le", "la", "les", "de", "du", "des", "un", "une", "et", "en", "est",
        "que", "qui", "dans", "pour", "pas", "sur", "ce", "il", "elle", "nous",
        "vous", "ils", "par", "avec", "son", "sa", "ses", "au", "aux", "ou",
        "mais", "donc", "car", "ni", "ne", "se", "si", "tout", "plus", "bien",
        "aussi", "comme", "sont", "ont", "fait", "peut", "cette", "ces", "mon",
        "ton", "leur", "etre", "avoir", "faire", "dire", "aller", "voir",
        "the", "is", "at", "which", "on", "a", "an", "and", "or", "but",
        "in", "with", "to", "for", "of", "not", "you", "it", "be", "are",
        "was", "were", "been", "have", "has", "had", "do", "does", "did",
        "will", "would", "could", "should", "may", "might", "shall", "can",
        "this", "that", "these", "those", "from", "by", "as", "if", "they",
        "their", "them", "than", "then", "its", "our", "your", "his", "her",
    }

    words = re.findall(r"\b\w{3,}\b", text.lower())
    filtered = [w for w in words if w not in stop_words and not w.isdigit()]
    total = len(filtered)

    if total == 0:
        return {"keywords": [], "total_words": 0}

    counter = Counter(filtered)
    top = counter.most_common(top_n)

    # 2-word phrases
    bigrams = []
    for i in range(len(filtered) - 1):
        bigrams.append(f"{filtered[i]} {filtered[i+1]}")
    bigram_counter = Counter(bigrams)
    top_bigrams = bigram_counter.most_common(10)

    return {
        "total_words": total,
        "top_keywords": [
            {"word": w, "count": c, "density": round(c / total * 100, 2)}
            for w, c in top
        ],
        "top_phrases": [
            {"phrase": p, "count": c, "density": round(c / total * 100, 2)}
            for p, c in top_bigrams if c >= 2
        ],
    }


# ─── Content Freshness ──────────────────────────────────────────────────────

def analyze_freshness(posts: list) -> dict:
    """Analyze content freshness and update patterns."""
    now = datetime.now(timezone.utc)
    results = {
        "total_posts": len(posts),
        "fresh": [],       # Updated < 3 months
        "aging": [],       # Updated 3-12 months
        "stale": [],       # Updated > 12 months
        "never_updated": [],  # Modified date = publish date
        "avg_age_days": 0,
    }

    total_age = 0
    for post in posts:
        title = post.get("title", {}).get("rendered", "")
        link = post.get("link", "")
        date_str = post.get("date", "")
        modified_str = post.get("modified", "")

        try:
            published = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            if published.tzinfo is None:
                published = published.replace(tzinfo=timezone.utc)
        except (ValueError, AttributeError):
            continue

        try:
            modified = datetime.fromisoformat(modified_str.replace("Z", "+00:00"))
            if modified.tzinfo is None:
                modified = modified.replace(tzinfo=timezone.utc)
        except (ValueError, AttributeError):
            modified = published

        age_days = (now - modified).days
        total_age += age_days

        entry = {
            "title": title,
            "link": link,
            "published": date_str,
            "modified": modified_str,
            "age_days": age_days,
            "was_updated": abs((modified - published).days) > 1,
        }

        if not entry["was_updated"]:
            results["never_updated"].append(entry)

        if age_days < 90:
            results["fresh"].append(entry)
        elif age_days < 365:
            results["aging"].append(entry)
        else:
            results["stale"].append(entry)

    if posts:
        results["avg_age_days"] = round(total_age / len(posts))

    results["summary"] = {
        "fresh_count": len(results["fresh"]),
        "aging_count": len(results["aging"]),
        "stale_count": len(results["stale"]),
        "never_updated_count": len(results["never_updated"]),
        "freshness_score": round(
            (len(results["fresh"]) / len(posts) * 100) if posts else 0
        ),
    }

    return results


# ─── Duplicate/Cannibalization Detection ─────────────────────────────────────

def detect_cannibalization(posts: list) -> dict:
    """Detect title/topic cannibalization between posts."""
    results = {
        "duplicate_titles": [],
        "similar_slugs": [],
        "category_cannibalization": [],
    }

    # Check for very similar titles
    titles = []
    for post in posts:
        title = post.get("title", {}).get("rendered", "").lower().strip()
        titles.append({
            "title": title,
            "id": post.get("id"),
            "link": post.get("link", ""),
            "original_title": post.get("title", {}).get("rendered", ""),
            "categories": post.get("categories", []),
        })

    # Simple word-overlap similarity
    for i in range(len(titles)):
        for j in range(i + 1, len(titles)):
            words_a = set(re.findall(r"\b\w{4,}\b", titles[i]["title"]))
            words_b = set(re.findall(r"\b\w{4,}\b", titles[j]["title"]))
            if not words_a or not words_b:
                continue
            overlap = words_a & words_b
            union = words_a | words_b
            similarity = len(overlap) / len(union) if union else 0

            if similarity > 0.6:
                results["duplicate_titles"].append({
                    "post_a": {
                        "id": titles[i]["id"],
                        "title": titles[i]["original_title"],
                        "link": titles[i]["link"],
                    },
                    "post_b": {
                        "id": titles[j]["id"],
                        "title": titles[j]["original_title"],
                        "link": titles[j]["link"],
                    },
                    "similarity": round(similarity * 100),
                    "shared_words": list(overlap),
                })

    # Same category posts competing
    category_posts = defaultdict(list)
    for t in titles:
        for cat_id in t["categories"]:
            category_posts[cat_id].append(t)

    for cat_id, cat_posts in category_posts.items():
        if len(cat_posts) > 10:
            results["category_cannibalization"].append({
                "category_id": cat_id,
                "post_count": len(cat_posts),
                "message": f"Categorie {cat_id} a {len(cat_posts)} articles - risque de cannibalisation",
            })

    return results


# ─── Topic Cluster Mapping ───────────────────────────────────────────────────

def map_topic_clusters(posts: list, categories: list) -> dict:
    """Map posts into topic clusters based on categories and keywords."""
    clusters = {}

    # Build category map
    cat_map = {c.get("id"): c for c in categories}

    for post in posts:
        seo = post.get("_seo", {})
        title = post.get("title", {}).get("rendered", "")
        link = post.get("link", "")
        word_count = seo.get("word_count", 0)

        for cat_id in post.get("categories", []):
            cat = cat_map.get(cat_id, {})
            cat_name = cat.get("name", f"Category {cat_id}")
            cat_slug = cat.get("slug", "")

            if cat_name not in clusters:
                clusters[cat_name] = {
                    "slug": cat_slug,
                    "posts": [],
                    "total_words": 0,
                    "avg_word_count": 0,
                    "has_pillar": False,
                }

            clusters[cat_name]["posts"].append({
                "title": title,
                "link": link,
                "word_count": word_count,
                "internal_links": seo.get("internal_links", 0),
            })
            clusters[cat_name]["total_words"] += word_count

    # Calculate cluster health
    for name, cluster in clusters.items():
        count = len(cluster["posts"])
        cluster["avg_word_count"] = round(cluster["total_words"] / count) if count else 0
        # A pillar post is the longest post (3000+ words) in the cluster
        max_wc = max((p["word_count"] for p in cluster["posts"]), default=0)
        cluster["has_pillar"] = max_wc >= 3000
        cluster["post_count"] = count
        cluster["health"] = "good" if count >= 5 and cluster["has_pillar"] else (
            "growing" if count >= 3 else "weak"
        )

    return {
        "total_clusters": len(clusters),
        "clusters": clusters,
        "recommendations": _cluster_recommendations(clusters),
    }


def _cluster_recommendations(clusters: dict) -> list:
    """Generate recommendations for improving topic clusters."""
    recs = []
    for name, cluster in clusters.items():
        if cluster["health"] == "weak":
            recs.append({
                "cluster": name,
                "priority": "high",
                "action": f"Renforcer le cluster '{name}' ({cluster['post_count']} articles). "
                          f"Objectif: 5+ articles avec un article pilier de 3000+ mots.",
            })
        if not cluster["has_pillar"]:
            recs.append({
                "cluster": name,
                "priority": "medium",
                "action": f"Creer un article pilier (3000+ mots) pour le cluster '{name}'.",
            })
        # Check internal linking within cluster
        low_links = [p for p in cluster["posts"] if p["internal_links"] < 2]
        if low_links:
            recs.append({
                "cluster": name,
                "priority": "medium",
                "action": f"{len(low_links)} article(s) dans '{name}' ont moins de 2 liens internes. "
                          f"Renforcer le maillage intra-cluster.",
            })

    return recs


# ─── E-E-A-T Signals Detection ──────────────────────────────────────────────

def detect_eeat_signals(posts: list, users: list, site_info: dict) -> dict:
    """Detect E-E-A-T signals across the WordPress site."""
    signals = {
        "experience": {"score": 0, "max": 25, "signals": []},
        "expertise": {"score": 0, "max": 25, "signals": []},
        "authoritativeness": {"score": 0, "max": 25, "signals": []},
        "trustworthiness": {"score": 0, "max": 25, "signals": []},
    }

    # Experience: Check for original content signals
    posts_with_images = sum(
        1 for p in posts if p.get("_seo", {}).get("images_count", 0) > 0
    )
    if posts_with_images / max(len(posts), 1) > 0.7:
        signals["experience"]["score"] += 8
        signals["experience"]["signals"].append("70%+ des articles contiennent des images")

    long_posts = sum(
        1 for p in posts if p.get("_seo", {}).get("word_count", 0) >= 2000
    )
    if long_posts > 0:
        signals["experience"]["score"] += 7
        signals["experience"]["signals"].append(
            f"{long_posts} article(s) approfondi(s) (2000+ mots)"
        )

    # Expertise: Check author bios
    authors_with_bio = sum(1 for u in users if u.get("description"))
    if authors_with_bio > 0:
        signals["expertise"]["score"] += 10
        signals["expertise"]["signals"].append(
            f"{authors_with_bio} auteur(s) avec biographie"
        )
    else:
        signals["expertise"]["signals"].append(
            "Aucun auteur n'a de biographie (important pour E-E-A-T)"
        )

    # Check for author pages
    if users:
        signals["expertise"]["score"] += 5
        signals["expertise"]["signals"].append("Pages auteur disponibles")

    # Authoritativeness: external links and citations
    posts_with_ext_links = sum(
        1 for p in posts if p.get("_seo", {}).get("external_links", 0) > 0
    )
    if posts_with_ext_links / max(len(posts), 1) > 0.5:
        signals["authoritativeness"]["score"] += 8
        signals["authoritativeness"]["signals"].append(
            "50%+ des articles citent des sources externes"
        )

    # Trustworthiness: site-level signals
    site_name = site_info.get("name", "")
    if site_name:
        signals["trustworthiness"]["score"] += 5
        signals["trustworthiness"]["signals"].append("Nom du site configure")

    description = site_info.get("description", "")
    if description:
        signals["trustworthiness"]["score"] += 5
        signals["trustworthiness"]["signals"].append("Description du site renseignee")

    seo_plugin = site_info.get("seo_plugin")
    if seo_plugin:
        signals["trustworthiness"]["score"] += 5
        signals["trustworthiness"]["signals"].append(
            f"Plugin SEO actif ({seo_plugin})"
        )

    total_score = sum(s["score"] for s in signals.values())
    total_max = sum(s["max"] for s in signals.values())

    return {
        "eeat_score": round(total_score / total_max * 100),
        "breakdown": signals,
        "total_score": total_score,
        "total_max": total_max,
    }


# ─── Main CLI ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="WordPress content deep analyzer for SEO"
    )
    parser.add_argument("url", help="WordPress site URL")
    parser.add_argument("--user", "-u", help="WordPress username")
    parser.add_argument("--password", "-p", help="Application password")
    parser.add_argument(
        "--command", "-c",
        default="full",
        choices=["full", "readability", "keywords", "freshness",
                 "duplicates", "clusters", "eeat"],
        help="Analysis command (default: full)"
    )
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    try:
        url = validate_url(args.url)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    client = WordPressClient(url, args.user, args.password)

    # Fetch data
    try:
        posts = client.get_posts()
        categories = client.get_categories()
        users = client.get_users()
        site_info = client.check_wordpress()
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)

    command = args.command
    result = {}

    if command in ("full", "readability"):
        readability_results = []
        for post in posts:
            content_html = post.get("content", {}).get("rendered", "")
            soup = BeautifulSoup(content_html, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            r = flesch_reading_ease(text)
            readability_results.append({
                "id": post["id"],
                "title": post.get("title", {}).get("rendered", ""),
                "link": post.get("link", ""),
                **r,
            })
        result["readability"] = readability_results

    if command in ("full", "keywords"):
        keyword_results = []
        for post in posts:
            content_html = post.get("content", {}).get("rendered", "")
            soup = BeautifulSoup(content_html, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            kw = analyze_keyword_density(text)
            keyword_results.append({
                "id": post["id"],
                "title": post.get("title", {}).get("rendered", ""),
                "link": post.get("link", ""),
                **kw,
            })
        result["keywords"] = keyword_results

    if command in ("full", "freshness"):
        result["freshness"] = analyze_freshness(posts)

    if command in ("full", "duplicates"):
        result["cannibalization"] = detect_cannibalization(posts)

    if command in ("full", "clusters"):
        result["clusters"] = map_topic_clusters(posts, categories)

    if command in ("full", "eeat"):
        result["eeat"] = detect_eeat_signals(posts, users, site_info)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        _print_analysis(result, command)


def _print_analysis(result: dict, command: str):
    """Print formatted analysis results."""
    if "readability" in result:
        print("\n  LISIBILITE")
        print("  " + "-" * 50)
        for r in result["readability"]:
            emoji = "OK" if r["score"] >= 60 else "!!"
            print(f"  [{emoji}] {r['title'][:50]}")
            print(f"       Score: {r['score']} - {r['grade']}")
            print(f"       Mots: {r['words']}, Phrases: {r['sentences']}")

    if "freshness" in result:
        f = result["freshness"]["summary"]
        print("\n  FRAICHEUR DU CONTENU")
        print("  " + "-" * 50)
        print(f"  Score fraicheur: {f['freshness_score']}%")
        print(f"  Frais (<3 mois):  {f['fresh_count']}")
        print(f"  Vieillissant:     {f['aging_count']}")
        print(f"  Obsolete (>1 an): {f['stale_count']}")
        print(f"  Jamais mis a jour: {f['never_updated_count']}")

    if "cannibalization" in result:
        c = result["cannibalization"]
        print("\n  CANNIBALISATION")
        print("  " + "-" * 50)
        if c["duplicate_titles"]:
            for d in c["duplicate_titles"]:
                print(f"  !! Similarite {d['similarity']}%:")
                print(f"     A: {d['post_a']['title'][:60]}")
                print(f"     B: {d['post_b']['title'][:60]}")
        else:
            print("  Aucune cannibalisation detectee")

    if "clusters" in result:
        cl = result["clusters"]
        print(f"\n  TOPIC CLUSTERS ({cl['total_clusters']})")
        print("  " + "-" * 50)
        for name, cluster in cl["clusters"].items():
            health = {"good": "OK", "growing": "..", "weak": "!!"}[cluster["health"]]
            pillar = "Pilier OK" if cluster["has_pillar"] else "Pas de pilier"
            print(f"  [{health}] {name}: {cluster['post_count']} articles, {pillar}")

    if "eeat" in result:
        e = result["eeat"]
        print(f"\n  E-E-A-T SCORE: {e['eeat_score']}/100")
        print("  " + "-" * 50)
        for factor, data in e["breakdown"].items():
            print(f"  {factor.capitalize()}: {data['score']}/{data['max']}")
            for s in data["signals"]:
                print(f"    - {s}")


if __name__ == "__main__":
    main()
