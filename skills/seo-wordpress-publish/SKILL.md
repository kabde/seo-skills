---
name: seo-wordpress-publish
description: >
  Publish articles to WordPress via REST API. Supports creating posts, setting
  categories/tags, featured images, Yoast/RankMath meta, and scheduling. Can publish
  from Markdown files or direct content. Use when user says "publish", "publier",
  "post to wordpress", or "mettre en ligne".
user-invokable: true
argument-hint: "<markdown-file|content> [--site url] [--status draft|publish|scheduled]"
license: MIT
metadata:
  author: Abderrahim KHALID (MEDIA BUYING ACADEMY)
  version: "1.0.0"
  category: seo
---

# WordPress Publish

Publish articles to WordPress via the REST API from Markdown files or direct content.

## Invocation

```
/seo-wordpress-publish <file.md>
/seo-wordpress-publish <file.md> --site https://example.com --status publish
/seo-wordpress-publish <file.md> --status scheduled --date 2026-05-01T09:00:00
```

## Prerequisites

WordPress credentials must be configured in `~/.config/claude-seo/wordpress.json`:

```json
{
  "site_url": "https://your-site.com",
  "username": "your-username",
  "application_password": "xxxx xxxx xxxx xxxx"
}
```

Generate an Application Password in WordPress: Users > Profile > Application Passwords.

## Workflow

1. **Read Markdown file** -- Parse frontmatter (YAML) and body content
2. **Convert Markdown to HTML** -- Preserve headings, lists, code blocks, images
3. **Authenticate** -- Connect via Application Password (Basic Auth over HTTPS)
4. **Create or update post** -- POST to `/wp/v2/posts` (or PUT for updates)
5. **Set categories and tags** -- Look up by name, create if they don't exist
6. **Set featured image** -- Upload via `/wp/v2/media` if `featured_image` path given
7. **Set SEO meta** -- Auto-configure Yoast or RankMath title + description via REST API
8. **Set status** -- `draft` (default), `publish`, or `future` (scheduled)
9. **Return post URL and ID** -- Confirm publication with direct link

## Supported Frontmatter Fields

```yaml
---
title: "Mon article SEO optimise"
description: "Meta description pour les moteurs de recherche (max 160 chars)"
category: "Marketing Digital"
tags:
  - SEO
  - WordPress
  - Content Marketing
featured_image: "./images/hero.jpg"
status: draft          # draft | publish | future
date: "2026-05-01T09:00:00"   # Required if status is 'future'
slug: "mon-article-seo"
---
```

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `title` | Yes | -- | Post title (H1) |
| `description` | Recommended | -- | Meta description for SEO plugins |
| `category` | Recommended | Uncategorized | Primary category name |
| `tags` | Optional | [] | List of tag names |
| `featured_image` | Recommended | -- | Path to image file (local or URL) |
| `status` | Optional | draft | Post status |
| `date` | Optional | now | Publish date (ISO 8601), required for scheduled |
| `slug` | Optional | auto | URL slug |

## SEO Meta Handling

The skill auto-detects the active SEO plugin (Yoast or RankMath) and sets:

- **SEO Title**: From `title` frontmatter field
- **Meta Description**: From `description` frontmatter field
- **Focus Keyword**: From `tags[0]` if no explicit keyword set
- **Canonical URL**: Auto-set to post permalink
- **Open Graph**: Title + description propagated to OG tags

Detection order: Yoast (`yoast/v1` namespace) > RankMath (`rankmath/v1`) > skip.

## Safety Rules

- **Default to draft** -- Never publish live without explicit `--status publish`
- **Confirmation prompt** -- When `--status publish`, display a summary and ask for confirmation
- **No overwrite without ID** -- Creating always makes a new post; updating requires `--post-id`
- **Credential security** -- Credentials read from config file, never passed as CLI args in logs

## Pre-Publish Checklist

Before publishing (status=publish), the skill verifies:

| Check | Threshold | Action on Fail |
|-------|-----------|----------------|
| Word count | >= 1500 words | Warn, suggest expanding |
| Meta description | Set and 120-160 chars | Warn, suggest writing one |
| Featured image | Set | Warn, suggest adding one |
| Categories | At least 1 assigned | Warn, assign Uncategorized |
| Title length | 20-60 characters | Warn with current length |
| Internal links | >= 1 | Warn, suggest adding links |
| H2 headings | >= 2 | Warn about flat structure |

Warnings do not block draft saves. For `--status publish`, all critical checks must pass or user must confirm override.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `401 Unauthorized` | Bad credentials | Check username + application password |
| `403 Forbidden` | Insufficient permissions | User needs Editor or Administrator role |
| `404 Not Found` | REST API disabled | Enable via Settings > Permalinks (save) |
| `413 Entity Too Large` | Image too big | Compress image before upload |
| `500 Internal Server Error` | Server-side issue | Check WP error logs, retry |
| `Connection refused` | SSRF protection triggered | URL resolves to private IP |
| `Missing frontmatter` | No YAML block in Markdown | Add `---` delimited frontmatter |

## Cross-Skill Integration

- Before publishing, suggest running `/seo-content <draft-url>` for E-E-A-T audit
- After publishing, suggest `/seo-page <post-url>` for live page verification
- Use `/seo-brand-voice check <file>` to verify tone before publishing
- Load brand voice profile if available in project root

## Examples

```bash
# Publish as draft (default, safe)
/seo-wordpress-publish article.md

# Publish live with explicit status
/seo-wordpress-publish article.md --status publish

# Schedule for future date
/seo-wordpress-publish article.md --status scheduled --date 2026-05-01T09:00:00

# Publish to a specific site (overrides config)
/seo-wordpress-publish article.md --site https://other-blog.com
```
