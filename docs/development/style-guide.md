# Documentation Style Guide

Conventions for writing these docs. For code conventions, see the root
`STYLE_GUIDE.md`.

## Tone

- Be concise and task-oriented. Lead with the example, then explain.
- Address the reader as "you".

## Structure

- Start each page with a one-line summary of what it covers.
- Prefer short sections with descriptive `##` headings.

## Code blocks

- Use fenced code blocks with a language tag.
- Use content tabs (`=== "Tab"`) to show alternative approaches.
- Keep examples runnable and minimal.

## Admonitions

Use Material admonitions for asides:

```markdown
!!! note "Title"
    Body text.
```

- `note` for neutral context.
- `tip` for recommendations.
- `warning` for limitations and footguns.

## API reference pages

Each resource page is a short intro plus an mkdocstrings directive
(`::: signtraker.<module>.<Class>`). Keep prose in guides, not in the generated
reference.
