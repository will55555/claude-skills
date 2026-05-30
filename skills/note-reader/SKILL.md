---
name: note-reader
description: |
  Read, extract, and work with notes from Notion, Obsidian, or other sources. Use this skill whenever the user wants to access, summarize, search, or act on content from their notes — even if they say things like "check my notes", "pull up my Notion page", "look at my Obsidian vault", "find what I wrote about X", "what are my action items from Y", "summarize my notes on Z", or "use my notes to help with this task". Also trigger when the user references a specific note, page, document, or vault by name. Supports all section types (headings, tags, full pages) and all downstream uses (summarizing, Q&A, feeding into tasks/workflows).
---

# Note Reader Skill

This skill reads notes from Notion, Obsidian, or other sources and surfaces the relevant content for summarizing, answering questions, or feeding into downstream workflows.

---

## Step 1: Identify the Source

Ask the user (or infer from context) which source to read from:

| Source | How to access |
|---|---|
| **Notion** | Notion MCP (already connected) — use `notion-search` or `notion-fetch` |
| **Obsidian** | Local markdown files — read from vault path on disk |
| **Google Drive** | Google Drive MCP — use `gdrive_search` or `gdrive_fetch` |
| **Local files** | Bash / `view` tool — read `.md`, `.txt`, `.pdf` directly |
| **Other** | Ask user for URL, file path, or how to access it |

If the user hasn't specified a source, ask: *"Where are these notes — Notion, Obsidian, or somewhere else?"*

---

## Step 2: Locate the Right Content

### Notion
Use the MCP tools in this order:
1. **`notion-search`** — search by keyword or page title to find the right page(s)
2. **`notion-fetch`** — fetch a specific page by URL or ID once found
3. If the user wants child pages or a database, follow links from the parent page

Key tip: Notion pages return their full block tree. Parse headings to navigate to the right section.

### Obsidian
Obsidian vaults are folders of `.md` files on disk. Common vault locations:
- macOS: `~/Documents/ObsidianVault/` or `~/ObsidianVault/`
- Windows: `C:/Users/<name>/Documents/ObsidianVault/`
- Custom: ask the user if not obvious

To find notes:
```bash
# List all notes
find ~/Documents/ObsidianVault -name "*.md" | head -30

# Search for a keyword across all notes
grep -rl "keyword" ~/Documents/ObsidianVault --include="*.md"

# Read a specific note
cat ~/Documents/ObsidianVault/path/to/note.md
```

#### Path Not Found — Fallback Flow

If the vault path doesn't exist on disk (the `find` or `cat` returns an error or empty result), **do not guess further**. Switch to manual path entry:

1. Tell the user clearly: *"I couldn't find your Obsidian vault at the expected location (`<path tried>`). Can you paste the full path to your vault or the specific note?"*
2. Wait for the user to provide the path.
3. Once received, verify it exists before reading:
   ```bash
   ls "<user-provided-path>"
   ```
4. If it still fails, ask them to confirm the path in their OS file explorer and paste it again. Do not proceed until a valid path is confirmed.
5. Once confirmed valid, continue with normal Step 2 logic (find/grep/cat).

Obsidian-specific syntax to handle:
- `[[wikilinks]]` — internal links to other notes
- `#tags` — inline tags on blocks or at top of file
- `---` frontmatter blocks (YAML metadata at top of file)
- `![[embeds]]` — embedded content from other files

### Google Drive / Other MCPs
Search and fetch with the relevant MCP. If Google Drive:
1. Use `gdrive_search` to find the document
2. Use `gdrive_fetch` or `gdrive_get_doc_content` to read it

### Local Files
Use `view` or `bash_tool` to read the file directly. Handle `.pdf` with the pdf-reading skill if needed.

---

## Step 3: Extract the Relevant Section(s)

After fetching the note content, extract what the user needs:

### By Heading
Parse markdown headings (`#`, `##`, `###`) and slice out the section:
- "Action items" → find `## Action Items` and read until the next same-level heading
- "Summary" → find `## Summary` block

### By Tag (Obsidian)
- Inline tags: `grep` for `#tagname` across notes or within a file
- Frontmatter tags: parse YAML `tags:` field

### Full Page / All Content
Return the entire note, then summarize or restructure for the user.

### Across Multiple Notes
If the user wants a theme across many notes (e.g., "all my meeting notes from last week"):
```bash
grep -rl "meeting" ~/ObsidianVault --include="*.md" | xargs ls -lt | head -10
```
Then read each relevant file and synthesize.

---

## Step 4: Deliver the Output

Match the output to what the user actually needs:

| Use case | Output format |
|---|---|
| **Summarize** | 3–5 bullet points of key ideas, or a short prose summary |
| **Q&A** | Answer the question directly, cite which note/section it came from |
| **Action items** | Bulleted checklist, optionally with assignees/dates if present |
| **Feed into workflow** | Pass structured content to the next step (task creation, calendar, etc.) |
| **Full extract** | Return the raw section with light formatting |

Always tell the user **which note / page / section** you read from, so they can verify.

---

## Tips & Edge Cases

- **Ambiguous request**: If the user says "check my notes" without specifying a topic, ask what they're looking for before fetching everything.
- **Large vaults**: Don't try to read every file. Search first, then read the most relevant hits.
- **Linked notes** (Obsidian `[[wikilinks]]`): If a section references another note and the user needs that content too, follow the link and read it.
- **Stale Notion content**: Notion MCP fetches live data — no caching concerns.
- **Private / missing files**: If a Notion page returns 404, tell the user and ask them to confirm the page URL or ID. For Obsidian/local paths that don't exist, follow the **Path Not Found — Fallback Flow** in Step 2 above — switch to manual path entry immediately, do not keep guessing paths.
- **Multiple sources**: It's fine to read from both Notion and Obsidian in one request if the user needs cross-source synthesis.
