# LinkedIn preview

**Version:** 8 · **Created:** 2026-10-28 18:15 · **Updated:** 2026-10-29 10:04

A skill for Claude Code (or any agent that reads `SKILL.md` skills). Ask it to
write a LinkedIn post and you get one HTML file back: the post previewed in
the LinkedIn feed on a phone and on a desktop, cut at "…more" the way the feed
cuts it, an editor with a live counter against LinkedIn's 3,000-character
limit, and buttons that copy the post and the first comment.

The page is a single file with no network calls: images are embedded, fonts
are the system's. You can open it from disk or send it to someone.

## Install

In Claude Code, at the prompt of a terminal session:

```
/plugin install linkedin-preview --marketplace WIPexpert/linkedin-preview
```

Answer `y` to add the marketplace, then pick a scope. From a shell, the same
thing is `claude plugin install linkedin-preview --marketplace WIPexpert/linkedin-preview`.
In the Claude desktop app, click + next to the prompt box, then Plugins, Add
marketplace with `WIPexpert/linkedin-preview`, then Add plugin.

Without the plugin system, copy the skill folder into your skills directory:

```bash
git clone https://github.com/WIPexpert/linkedin-preview.git
```

```bash
cp -R linkedin-preview/skills/linkedin-preview ~/.claude/skills/linkedin-preview
```

Then ask for a post in a new session: "write a LinkedIn post about our new
onboarding flow", "turn these notes into a LinkedIn post".

Requirements: Python 3.8+ (standard library only) and a browser.

## What is in the folder

| Path | What it is |
|---|---|
| `SKILL.md` | The instructions the agent follows: questions, writing rules, rendering, hand-over |
| `assets/linkedin-preview.html` | The page template. Opened as is, it shows sample data |
| `scripts/render.py` | Fills the template from your input and checks the feed cut |
| `examples/post.md` | An example input in markdown |
| `examples/post.json` | The same idea as JSON |
| `examples/post.html` | `post.md`, rendered ([open it online](https://wipexpert.github.io/linkedin-preview/skills/linkedin-preview/examples/post.html)) |

## Run the renderer yourself

The agent runs it for you. To run it by hand, point at the script in the
skill's folder:

```bash
python3 path/to/linkedin-preview/scripts/render.py post.md
```

```bash
python3 path/to/linkedin-preview/scripts/render.py post.json -o preview.html
```

```bash
python3 path/to/linkedin-preview/scripts/render.py post.md --check
```

The first writes `post.html` next to `post.md`; the second picks the output
path; the third only prints the report and exits with 1 if something needs a
look. The report shows the length and an estimate of the three lines the
feed shows before "…more" (the page measures the real cut; see below):

```
length: 1030 of 3000 characters
first comment: 90 of 1250 characters
phone, estimate at ~55/line: OK  The first two lines show before …more.
    | Our most used screen started as three support tickets.
    | Nobody flagged them. Nobody asked for a new feature.
    | Each ticket used different words, and all three …more
```

## Input

### Markdown

Front matter, then the post as plain text, then optional `##` sections.
`## First comment` and `## Checklist` are recognised; any other `##` heading
becomes a notes block with that title on the page.

```markdown
---
title: Three support tickets
author: Alex Morgan
headline: Head of Product at Northwind
avatar: avatar.jpg
image: chart.png
---
Our most used screen started as three support tickets.
Nobody flagged them. Nobody asked for a new feature.
Each ticket used different words, and all three wanted the same thing.

What does your support queue keep asking for?

## First comment
The routine, step by step: https://example.com/blog/reading-support-tickets

## Checklist
- The customer quotes are cleared for public use

## Notes
If you need a shorter version, cut the paragraph with the quotes.
```

### JSON

```json
{
  "title": "Three support tickets",
  "author": { "name": "Alex Morgan", "title": "Head of Product at Northwind", "avatar": "avatar.jpg" },
  "post": "Our most used screen started as three support tickets.\nNobody flagged them.",
  "first_comment": "The routine: https://example.com/blog/reading-support-tickets",
  "checklist": ["The customer quotes are cleared for public use"],
  "notes": [{ "title": "Notes", "text": "Plain text. Blank lines split paragraphs; lines starting with - make a list." }],
  "image": "chart.png"
}
```

Every field except `post` is optional. `title` defaults to the first line of
the post, the author name to "Your Name", and the avatar to the author's
initials. Image paths are relative to the input file; local images are
embedded in the page, URLs are left as links.

## How the "…more" cut works

The feed shows three lines of a post, then "…more". Where the third line ends
depends on the font and the card width, so the page measures it: each preview
card finds the longest whole-word start of the post that still fits in three
rendered lines with "…more" after it, with no line longer than 80 characters
(spaces included). The desktop card copies LinkedIn's desktop feed: a head of
at most 550 x 62 px and a 508 x 60 px block for the first three lines (14 px
text on 20 px lines). The phone card is 380 px wide; real phones vary with the
screen width, so treat it as an estimate. Under the cards a line reports the total length and, per
card, how many characters show before "…more" and how long each of the three
lines is, for example "Phone: 92 characters before …more, lines of 45 / 8 / 39"
(the example post in a 380 px phone card).

LinkedIn's own rendering can still differ by a word: it may use another font
on the reader's device.

`scripts/render.py` cannot measure fonts, so its terminal report estimates the
cut by counting characters: about 55 a line on a phone and 80 on a desktop,
with 8 kept for "…more". The constants (`PHONE_WIDTH`, `DESKTOP_WIDTH`,
`MORE_LABEL`) sit at the top of the script. On the desktop 80 is the upper
bound, so the estimate can only run long; on a phone it runs generous, the
card holds closer to 48-49 characters a line. Use it as a hint and trust the
page. The 3,000-character cap (`POST_LIMIT`) is exact.

## Behaviour of the page

- The post editor comes first, then the preview.
- Name and Headline fields above the editor change the author shown on the
  cards; they start from the rendered input.
- Phone or Desktop, remembered per browser. The counts under the preview cover
  both devices, whichever one is on screen.
- Each card folds to three measured lines; "…more" and "Show the whole post"
  unfold it.
- The post editor uses the desktop feed's 508 px text block, font and 14/20
  type, so it wraps where LinkedIn's desktop feed wraps (on screens narrower
  than that it takes the full width).
- Editing the post or the comment updates the preview, the cut, the counts
  under the preview and the counter under the editor as you type. Edits are kept in the browser's local storage for that page
  only; "Back to the original text" restores the rendered version.
- Copy uses the clipboard API, falls back to the older copy command when the
  page is opened from disk, and shows a message if the browser blocks both.
- The page never shows the post in a monospace or code font, and nothing on
  it scrolls sideways, down to a 375-pixel phone screen.
- The footer links to this repository and carries one line of the author's
  ad for talenthunt, with a tracked link. It sits in
  `assets/linkedin-preview.html`, marked with a comment, if you want it out.
