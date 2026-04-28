---
name: seo-brand-voice
description: >
  Brand voice and editorial guidelines manager. Creates, stores, and enforces writing
  tone, style rules, audience persona, and vocabulary preferences. Used by write-article
  skill to maintain consistent voice. Use when user says "brand voice", "ton editorial",
  "style guide", "editorial guidelines", or "voix de marque".
user-invokable: true
argument-hint: "[create|check|update]"
license: MIT
metadata:
  author: Abderrahim KHALID (MEDIA BUYING ACADEMY)
  version: "1.0.0"
  category: seo
---

# Brand Voice Manager

Create, store, and enforce brand voice and editorial guidelines across all content.

## Invocation

```
/seo-brand-voice create
/seo-brand-voice check <file.md>
/seo-brand-voice update
```

## Three Modes

### 1. CREATE -- Interactive Brand Voice Wizard

Launches a guided questionnaire to build a complete brand voice profile:

1. **Brand Identity** -- Name, tagline, mission statement
2. **Tone Selection** -- Choose primary + secondary tones
3. **Audience Definition** -- Who they are, what they know, what they need
4. **Vocabulary Rules** -- Preferred terms, banned words, jargon policy
5. **Style Rules** -- Sentence length, paragraph style, formatting
6. **Content Rules** -- Citations, CTAs, humor, examples
7. **SEO Voice** -- How to integrate keywords naturally

Output: Saves `brand-voice.md` in the project root.

### 2. CHECK -- Audit a Draft Against Brand Voice

Reads the brand voice profile and analyzes a draft article for compliance:

```
/seo-brand-voice check draft-article.md
```

**Output format:**

- **Compliance score**: X/100
- **Tone analysis**: Does the tone match the profile?
- **Violations list**: Specific lines that break rules
- **Vocabulary flags**: Banned words found, missing preferred terms
- **Style metrics**: Average sentence length, paragraph length, person used
- **Suggestions**: Concrete rewrites for flagged sections

### 3. UPDATE -- Modify Existing Profile

Edit specific sections of an existing `brand-voice.md` without rebuilding from scratch:

```
/seo-brand-voice update
```

Presents current profile sections and asks which to modify.

## Brand Voice Profile Structure

The profile is saved as `brand-voice.md` in the project root with this structure:

```markdown
# Brand Voice Profile

## Brand Identity
- **Name**: [Brand name]
- **Tagline**: [One-line tagline]
- **Mission**: [What the brand helps people do]

## Tone
- **Primary tone**: [expert | friendly | formal | conversational | authoritative]
- **Secondary tone**: [warm | precise | witty | empathetic | bold]
- **Tone spectrum**: [Where on formal <-> casual scale, 1-10]
- **Emotional register**: [inspire | educate | reassure | challenge | entertain]

## Audience Persona
- **Who**: [Target reader description]
- **Experience level**: [beginner | intermediate | advanced | mixed]
- **Pain points**: [Top 3 problems they face]
- **Goals**: [What they want to achieve]
- **Reading context**: [Mobile commute | Desktop work | Research mode]

## Vocabulary Rules
- **Preferred terms**: [Words that reinforce brand identity]
- **Avoided terms**: [Words that contradict brand voice]
- **Jargon policy**: [Define on first use | Avoid entirely | Use freely]
- **Power words**: [Action words that drive engagement]
- **Transition phrases**: [Preferred connectors between ideas]

## Style Rules
- **Sentence length**: [Target average, e.g., 15-20 words]
- **Paragraph length**: [Target, e.g., 2-4 sentences]
- **Contractions**: [Yes | No | Sparingly]
- **Person**: [1st (we/I) | 2nd (you) | 3rd (they/one)]
- **Active voice**: [Required | Preferred | Flexible]
- **Lists and formatting**: [Bullet points encouraged | Minimal formatting]
- **Heading style**: [Question-based | Action-based | Descriptive]

## Content Rules
- **Citation style**: [Link inline | Footnotes | "According to X" pattern]
- **CTA style**: [Soft suggestion | Direct command | Question-based]
- **Humor policy**: [None | Light and relevant | Frequent]
- **Example usage**: [Real examples | Hypothetical | Data-driven]
- **Emoji usage**: [None | Sparingly in headings | Freely]
- **Opening style**: [Hook with stat | Question | Story | Direct statement]
- **Closing style**: [Summary + CTA | Question | Forward-looking statement]

## SEO Voice Integration
- **Keyword placement**: [Natural flow | First paragraph required | H2 required]
- **Keyword density**: [Target range, e.g., 1-2%]
- **Internal link style**: [Contextual anchor text | "Read more" pattern]
- **Meta description voice**: [Matches article tone | More formal | More direct]
```

## Check Mode Output

When running `check`, the output follows this format:

```
BRAND VOICE AUDIT: article-draft.md
================================================

Score: 78/100

TONE ANALYSIS
  Target: expert + friendly
  Detected: expert + formal (mismatch on secondary tone)
  Suggestion: Add more conversational transitions

VOCABULARY VIOLATIONS (3 found)
  Line 12: "utilize" -> Use "use" instead (simplicity rule)
  Line 34: "synergy" -> Banned corporate jargon
  Line 56: Missing preferred term "actionable" (0 occurrences)

STYLE METRICS
  Avg sentence length: 24 words (target: 15-20) -- TOO LONG
  Avg paragraph length: 5.2 sentences (target: 2-4) -- TOO LONG
  Active voice: 72% (target: >80%) -- BELOW TARGET
  Person: Mixed 2nd/3rd (target: 2nd) -- INCONSISTENT

SUGGESTIONS
  1. Break paragraph at line 15 into two shorter paragraphs
  2. Rewrite line 23 in active voice: "We analyzed..." -> OK, "The data was analyzed..." -> Rewrite
  3. Add a conversational question before the H2 at line 40
```

## Cross-Skill Integration

- **seo-write-article**: Loads `brand-voice.md` before writing to apply tone and style rules
- **seo-wordpress-publish**: Suggests running brand voice check before publishing
- **seo-content**: E-E-A-T audit considers brand voice consistency as a quality signal

## File Location

The brand voice profile is stored at `./brand-voice.md` (project root). The skill checks for this file automatically when invoked by other skills. If not found, it suggests running `/seo-brand-voice create`.

## Examples

```bash
# Create a new brand voice profile (interactive)
/seo-brand-voice create

# Check an article draft against the profile
/seo-brand-voice check articles/mon-guide-seo.md

# Update specific sections of the profile
/seo-brand-voice update
```
