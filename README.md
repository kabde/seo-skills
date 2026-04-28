<!-- Updated: 2026-04-22 -->

# SEO Blogger Toolkit - Skills SEO pour Claude Code

Toolkit SEO complet pour blogueurs WordPress. **15 skills** couvrant l'audit WordPress via REST API, la redaction assistee d'articles SEO, la publication WordPress, les topic clusters (pillar + secondaires), l'analyse E-E-A-T, le schema markup, l'optimisation images, le SEO technique, et le referencement sur les moteurs IA (ChatGPT, Perplexity, Google AI Overviews).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Table des matieres

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commandes](#commandes)
- [Workflow complet](#workflow-complet)
- [Extensions (optionnelles)](#extensions-optionnelles)
- [Configuration WordPress](#configuration-wordpress)
- [Requirements](#requirements)

## Installation

```bash
git clone https://github.com/Abderrahim-KHALID/claude-seo.git
bash claude-seo/install.sh
```

## Quick Start

### Auditer un blog existant

```bash
# Demarrer Claude Code
claude

# Auditer ton blog WordPress
/seo-wordpress https://monblog.com

# Analyser ta strategie de contenu
/seo-wp-strategy https://monblog.com

# Verifier un article existant (E-E-A-T)
/seo-content https://monblog.com/mon-article

# Optimiser pour ChatGPT et les IA
/seo-geo https://monblog.com/mon-article
```

### Creer un nouvel article de A a Z

```bash
# Definir ta voix de marque
/seo-brand-voice

# Planifier un topic cluster
/seo-cluster "mot-cle principal"

# Structurer l'article (plan H1-H3)
/seo-outline-article "mot-cle principal"

# Rediger l'article optimise SEO + GEO
/seo-write-article "mot-cle principal"

# Publier sur WordPress
/seo-wordpress-publish article.md
```

## Commandes

| Commande | Description |
|----------|-------------|
| `/seo-audit <url>` | Audit SEO complet avec agents paralleles |
| `/seo-wordpress <url>` | Audit SEO du blog via WordPress REST API |
| `/seo-wp-strategy <url>` | Strategie de contenu et calendrier editorial |
| `/seo-cluster <keyword>` | Topic clusters : pillar article + articles secondaires |
| `/seo-content <url>` | Analyse E-E-A-T et qualite de contenu |
| `/seo-page <url>` | Analyse SEO approfondie d'une page |
| `/seo-schema <url>` | Detection et generation de schema JSON-LD |
| `/seo-geo <url>` | Optimisation pour IA (ChatGPT, Perplexity, AI Overviews) |
| `/seo-images <url>` | Optimisation images (alt text, poids, WebP) |
| `/seo-technical <url>` | Audit technique (Core Web Vitals, mobile, crawlers IA) |
| `/seo-outline-article <keyword>` | Plan de l'article (structure H1-H3, sources) |
| `/seo-write-article <keyword>` | Redaction assistee d'article SEO + GEO |
| `/seo-brand-voice` | Voix de marque et charte editoriale |
| `/seo-wordpress-publish <file>` | Publication d'article sur WordPress via REST API |

## Workflow complet

Le parcours complet d'un blogueur, de l'audit a la publication :

```
 1. /seo-wordpress           → Auditer le contenu existant sur WordPress
 2. /seo-wp-strategy         → Generer un calendrier editorial 12 semaines
 3. /seo-cluster             → Planifier pillar article + articles secondaires
 4. /seo-brand-voice         → Definir la voix de marque et le ton editorial
 5. /seo-outline-article     → Structurer l'article (plan H1-H3, sources, CTA)
 6. /seo-write-article       → Rediger l'article optimise SEO + GEO
 7. /seo-content             → Verifier E-E-A-T et qualite avant publication
 8. /seo-schema              → Ajouter le schema BlogPosting/Article
 9. /seo-geo                 → Optimiser pour les moteurs IA (LLM)
10. /seo-wordpress-publish   → Publier sur WordPress via API REST
```

### Strategie Pillar + Articles Secondaires

Le coeur de ce toolkit est la strategie de contenu en cluster :

- **Article Pillar** : Guide complet de 3000+ mots sur un sujet principal
- **Articles Secondaires** : Chaque section du pillar devient un article dedie de 1500+ mots
- **Maillage Interne** : Tous les articles secondaires pointent vers le pillar et inversement
- **Resultat** : Un cluster de contenu qui domine les SERPs et les reponses IA

## Extensions (optionnelles)

Le toolkit peut etre enrichi avec des extensions MCP :

| Extension | Usage |
|-----------|-------|
| **Banana** | Scraping avance de pages web pour l'analyse concurrentielle |
| **DataForSEO** | Donnees SERP en temps reel, volumes de recherche, difficulte de mots-cles |
| **Firecrawl** | Crawl complet de sites pour audit technique et extraction de contenu |

Ces extensions ne sont pas requises. Le toolkit fonctionne de maniere autonome sans elles.

## Configuration WordPress

### 1. Creer un Application Password

1. Aller dans WordPress Admin > Utilisateurs > Votre Profil
2. Descendre a "Mots de passe d'application"
3. Entrer un nom (ex: "Claude SEO Audit")
4. Cliquer "Ajouter un nouveau mot de passe d'application"
5. Copier le mot de passe genere (les espaces sont normaux)

### 2. Utiliser avec les skills

```bash
/seo-wordpress https://monblog.com --user admin --password xxxx xxxx xxxx xxxx
```

### 3. Configuration permanente (optionnel)

Stocker les credentials dans `~/.config/claude-seo/wordpress.json` :

```json
{
  "sites": {
    "monblog.com": {
      "url": "https://monblog.com",
      "username": "admin",
      "app_password": "xxxx xxxx xxxx xxxx"
    }
  }
}
```

## Requirements

- Python 3.10+
- Claude Code CLI
- WordPress 4.7+ (REST API native)
- Plugin SEO recommande : Yoast ou RankMath

## License

MIT License - voir [LICENSE](LICENSE) pour les details.

---

## Auteur

Cree par **Abderrahim KHALID** de **[MEDIA BUYING ACADEMY](https://mediabuying.ac/)** — 20 ans d'experience dans le digital, avec un background technique et marketing numerique.
