# WordPress SEO Checklist

## Technical Foundation
- [ ] Permalink structure: /%postname%/ (not default ?p=123)
- [ ] SSL/HTTPS enabled
- [ ] XML sitemap active (WP 5.5+ native or plugin)
- [ ] Robots.txt properly configured
- [ ] SEO plugin installed (Yoast or RankMath)
- [ ] Caching plugin active (WP Super Cache, W3 Total Cache, LiteSpeed)
- [ ] Image optimization plugin (ShortPixel, Imagify, or Smush)
- [ ] Lazy loading enabled for images
- [ ] PHP version 8.0+ for performance

## On-Page SEO (Per Post)
- [ ] SEO title set (30-60 characters)
- [ ] Meta description set (120-160 characters)
- [ ] Focus keyword defined
- [ ] H1 = post title (single H1)
- [ ] H2 subheadings (3+ per article)
- [ ] Keyword in first 100 words
- [ ] Keyword in at least one H2
- [ ] 1500+ words for blog posts
- [ ] Internal links (3-5 per article)
- [ ] External links to authoritative sources (1-3)
- [ ] Images with descriptive alt text
- [ ] Featured image set
- [ ] Custom excerpt written
- [ ] Slug optimized (short, keyword-rich)

## Schema Markup (Blog)
- [ ] BlogPosting or Article on every post
- [ ] BreadcrumbList for navigation
- [ ] Organization or Person for site/author
- [ ] WebSite with SearchAction on homepage
- [ ] ImageObject for featured images
- [ ] Author schema linked to author pages

## Taxonomy
- [ ] Categories have descriptions
- [ ] Category hierarchy (parent/child) organized
- [ ] No empty categories
- [ ] Tags used consistently (3+ posts per tag)
- [ ] No duplicate category+tag names
- [ ] Category pages have unique intro text (not just post list)

## E-E-A-T for Bloggers
- [ ] About page with author bio and credentials
- [ ] Author box on posts with photo, bio, social links
- [ ] Contact page with real contact information
- [ ] Privacy policy page
- [ ] Terms of service (if applicable)
- [ ] External credentials/certifications mentioned
- [ ] Social proof (testimonials, media mentions)

## Content Freshness
- [ ] Publication date visible on posts
- [ ] "Last updated" date shown for revised content
- [ ] Stale articles (>12 months) reviewed quarterly
- [ ] Evergreen content updated with fresh data annually

## WordPress-Specific Performance
- [ ] Database optimized (revisions limited, transients cleaned)
- [ ] Unused plugins deactivated and deleted
- [ ] Theme optimized (lightweight, no bloat)
- [ ] CDN configured for static assets
- [ ] WebP image format enabled
- [ ] Render-blocking CSS/JS minimized

## Application Password Setup (for API Access)
1. Go to WordPress Admin > Users > Your Profile
2. Scroll to "Application Passwords" section
3. Enter a name (e.g., "Claude SEO Audit")
4. Click "Add New Application Password"
5. Copy the generated password (spaces are normal)
6. Store in ~/.config/claude-seo/wordpress.json
