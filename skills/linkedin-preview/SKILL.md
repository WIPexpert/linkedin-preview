---
name: linkedin-preview
description: Write a LinkedIn post and hand it over as one self-contained HTML page that previews the post in the LinkedIn feed (phone and desktop, with the "…more" cut), with an editor, a live 3,000-character counter and copy buttons. Use when someone asks to "write a LinkedIn post", "draft a LinkedIn post about X", "turn this into a LinkedIn post", "make a LinkedIn post from these notes / this article / this link", or to rewrite or tighten a LinkedIn post they already have. Not for LinkedIn articles, DMs or comments on other people's posts.
---

# LinkedIn preview

**Version:** 5 · **Created:** 2026-10-28 18:15 · **Updated:** 2026-10-28 20:18

You write one LinkedIn post, check how it previews in the feed, and give the
person an HTML page they open in a browser to read, tweak and copy it.

## 1. Get what you need, ask only for what is missing

A post needs three things. Take them from the request and from any material
the person gave you (notes, an article, a link, a transcript, an old post):

- **Topic and point**: what happened or what they learned, and the one thing a
  reader should take away.
- **Reader**: who should stop scrolling for this (recruiters, founders,
  engineers, customers in some field).
- **Ask**: what the reader should do after reading: comment, try something,
  click a link, nothing at all.

If any of the three is missing and you cannot infer it, ask at most 2–3 short
questions in one message, then write. Also ask for the author's name and
headline if you do not have them; they appear on the preview card. Do not
invent facts, numbers, names or quotes. If the post needs a detail you do not
have, leave a clear placeholder like `[number of customers]` and add it to the
checklist.

## 2. Write the post

- **Plain text only.** LinkedIn does not render markdown: no `**bold**`, no
  `#` headings, no backticks, no bullet syntax that relies on markdown. No
  Unicode "bold" letters. Line breaks and short paragraphs do the formatting.
- **No emoji** unless the person asks for them.
- **The hook is the first two lines.** The feed shows about three lines, then
  "…more". Lines 1 and 2 must carry the reason to keep reading: a concrete
  result, a surprising detail, a tension. Do not open with "I'm excited to
  announce", a greeting, the company name or context the reader does not need
  yet. Keep line 1 and line 2 short (under ~45 characters each fits one phone line),
  and make line 3 a full sentence so the cut lands inside it.
- **One idea per post.** Specific beats general: a number, a name of a thing,
  a moment, a quote someone actually said.
- **Short paragraphs**, one to three sentences, a blank line between them.
- **End with the ask** from step 1. A question works only if it is one people
  can answer from their own experience.
- **Length**: most posts land between 600 and 1,500 characters. The hard cap
  is 3,000.
- **Links go in the first comment**, not in the post, unless the person wants
  them in the post. Write that comment too when there is a link to share.
- **Hashtags**: none or up to three, at the very end, only if the person uses
  them.
- **Sound like a person.** Cut filler ("in today's fast-paced world"),
  inflated words ("game-changer", "unlock", "delve"), "it's not X, it's Y"
  contrasts, lists of three by reflex, and a one-line moral at the end.

If the person gave you a draft to improve, keep their voice and facts; fix the
hook, the structure and the length.

## 3. Render the page

Save the post as a markdown input file and run the renderer from this skill's
folder. Put the file where the person is working, or in a folder they name,
for example `linkedin-posts/2026-10-28-support-tickets/post.md`:

```markdown
---
title: Three support tickets
author: Alex Morgan
headline: Head of Product at Northwind
avatar: avatar.jpg        # optional, local path or URL
image: chart.png          # optional, the image attached to the post
---
The post text, exactly as it will be pasted into LinkedIn.

## First comment
Optional. The comment with the link.

## Checklist
- Every [placeholder] left in the post.
- Every number, name, date or quote to confirm before publishing.

## Notes
Why the hook works, a shorter variant if the post runs long, and what you
left out and why.
```

Always fill the checklist and the notes; the page shows them next to the
editor, with checkboxes the person ticks off. The checklist covers what the
person must do or confirm before posting: each placeholder, each fact you took
from their material or could not verify, an image to attach, someone to tag.
The notes cover your choices: why the hook should stop the reader, one shorter
or sharper variant of the opening, and anything you cut. Keep each item to one
line. If there is honestly nothing to check, leave the checklist out rather
than padding it.

Then run:

```bash
python3 <this skill's folder>/scripts/render.py linkedin-posts/2026-10-28-support-tickets/post.md
```

It writes `post.html` next to the input and prints the character count and a
rough estimate of the three lines the feed shows before "…more". If a line
says `CHECK`, fix the post (usually: shorten line 1 or 2, remove a blank line
from the first two lines, or make line 3 longer) and run it again. The
estimate is generous on a phone; the page measures the real cut in each card,
so if you can open the page, trust what it shows. `--check` prints the report
without writing the page. A JSON input works too; see `README.md`.

## 4. Hand it over

Give the person the path to `post.html` (open it for them if your environment
can, for example `open post.html` on macOS) and, in a sentence or two, the
hook and anything left for them to check. Do not paste the whole post again
in chat unless they ask. The page lets them change the name and headline,
switch phone/desktop, unfold
the post, edit it with a live counter, see how many characters each card
shows before "…more", and copy the post and the first comment. Their edits stay in their browser; they copy the final text from the
page into LinkedIn themselves. Never publish or post on their behalf.
