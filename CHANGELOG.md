# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-04-23

### Added
- **15 skills** pour le cycle de vie complet du contenu blog
- **seo-wordpress**: Audit WordPress via REST API avec Application Password
- **seo-wp-strategy**: Strategie de contenu et calendrier editorial 12 semaines
- **seo-write-article**: Redaction assistee d'articles SEO + GEO (6 templates)
- **seo-outline-article**: Planification de structure d'article (H1-H3, sources)
- **seo-wordpress-publish**: Publication directe sur WordPress via REST API
- **seo-brand-voice**: Gestion du ton editorial et guidelines de marque
- **seo-cluster**: Topic clusters avec architecture pillar + articles secondaires
- **seo-content**: Analyse E-E-A-T et qualite de contenu
- **seo-page**: Analyse SEO approfondie d'une page
- **seo-schema**: Detection et generation de schema JSON-LD (BlogPosting, BreadcrumbList)
- **seo-geo**: Optimisation pour IA (ChatGPT, Perplexity, Google AI Overviews)
- **seo-images**: Optimisation images (alt text, poids, formats)
- **seo-technical**: Audit technique (Core Web Vitals, mobile, crawlers IA)
- **seo-audit**: Audit global avec 8 agents paralleles
- **8 agents** specialises pour l'analyse parallele
- **10 scripts Python**: wordpress_api.py, wp_content_analyzer.py, georeadiness_analyzer.py, llms_txt_generator.py, fetch_page.py, parse_html.py, pagespeed_check.py, google_report.py, capture_screenshot.py, analyze_visual.py
- Templates schema JSON-LD: BlogPosting, BreadcrumbList, Article, ProfilePage
- Workflow blogueur complet en 10 etapes (audit → publication)

### Architecture
- Format commandes uniforme: `/seo-xxx` (tiret)
- Auteur: Abderrahim KHALID - MEDIA BUYING ACADEMY (https://mediabuying.ac/)
- License: MIT
