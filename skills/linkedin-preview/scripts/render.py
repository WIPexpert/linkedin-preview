#!/usr/bin/env python3
"""Render one LinkedIn post into a self-contained HTML preview page.

    python3 render.py post.md                 # writes post.html next to it
    python3 render.py post.json -o out.html
    python3 render.py post.md --check         # report only, write nothing

The input is a JSON file or a markdown file (see README.md for both shapes).
The output is a copy of ../assets/linkedin-preview.html with its post-data block
filled in; images (avatar, post image) given as local paths are embedded as
data URIs, so the page works offline and can be sent as one file.

The script also prints a rough estimate of what the feed shows before "…more"
on a phone and on a desktop, so an agent can sanity-check the hook without a
browser. The page itself does not use that estimate: it folds each card by
measuring it, which is the number to trust.

Standard library only.
"""

import argparse
import base64
import datetime as dt
import json
import mimetypes
import re
import sys
from pathlib import Path

# Feed geometry for the terminal report. LinkedIn cuts by pixels in a
# proportional font, so a character count is only an estimate; the page
# measures its own cards instead. Measured on the desktop feed: the first
# three lines are a 508 x 60 px block and one line holds at most 80 characters
# with spaces. The phone depends on the screen width (a 380px card holds about
# 48-49 characters a line in the system font) but never more than 80.
PHONE_WIDTH = 55     # characters per rendered line on a phone, rough estimate
DESKTOP_WIDTH = 80   # characters per rendered line in the desktop feed, upper bound
MAX_LINE = 80        # no shown line is longer, on any device; the page enforces it
MORE_LABEL = 8       # room the "…more" link takes at the end of line three
POST_LIMIT = 3000    # LinkedIn's hard cap for a post, in characters (exact)
COMMENT_LIMIT = 1250  # LinkedIn's cap for a comment

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "linkedin-preview.html"
DATA_RE = re.compile(r'(<script type="application/json" id="post-data">)(.*?)(</script>)', re.S)


# ---------------------------------------------------------------- the feed cut

def feed_cut(post, width, more=MORE_LABEL):
    """What three rendered lines of the feed show at `width` characters a line.

    Each hard line is word-wrapped at `width`; the feed shows three rendered
    lines and, when more text follows, the third keeps room for "…more".
    Returns (lines shown, index of the hard line the cut is in, whether that
    hard line was shown to its end, whether "…more" appears).
    An estimate for the report; the page measures the real cut.
    """
    hard = post.split("\n")
    rendered = []  # (text, index of hard line, is last piece of that line)
    for idx, line in enumerate(hard):
        cur, pieces = "", []
        for w in line.split():
            if cur and len(cur) + 1 + len(w) > width:
                pieces.append(cur)
                cur = w
            else:
                cur = f"{cur} {w}" if cur else w
        pieces.append(cur)
        rendered += [(p, idx, k == len(pieces) - 1) for k, p in enumerate(pieces)]
        if len(rendered) >= 3:
            break
    shown = rendered[:3]
    if not shown:
        return [], 0, True, False
    text3, idx3, last_piece = shown[-1]
    more_follows = len(rendered) > 3 or idx3 < len(hard) - 1 or not last_piece
    complete = last_piece
    if more_follows and len(text3) > width - more:
        text3, complete = text3[: width - more], False
    return [t for t, _, _ in shown[:-1]] + [text3], idx3, complete, more_follows


def cut_verdict(post, device, width):
    """(ok, message) for one device, from the estimated cut."""
    hard = post.split("\n")
    _, idx, complete, more = feed_cut(post, width)
    if not more:
        return True, "The whole post fits; LinkedIn shows no …more."
    if any(not l.strip() for l in hard[:2]):
        return False, "A blank line in the first two lines spends the preview on nothing."
    if not (idx > 1 or (idx == 1 and complete)):
        return False, "The first two lines do not both fit before …more. Shorten them."
    if device == "desktop" and (idx != 2 or complete):
        return False, "The cut does not land in line 3: line 3 is blank or short, so the preview looks thin."
    return True, "The first two lines show before …more."


# ---------------------------------------------------------------- input

def data_uri(value, base):
    """A local image path becomes a data URI; URLs and data URIs pass through."""
    if not value:
        return None
    if re.match(r"^(https?:|data:)", value):
        return value
    p = Path(value).expanduser()
    if not p.is_absolute():
        p = base / p
    if not p.is_file():
        sys.exit(f"render.py: image not found: {p}")
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode("ascii")


def as_list(value):
    if value is None:
        return []
    if isinstance(value, str):
        return [l.strip()[2:].strip() if l.strip()[:2] in ("- ", "* ") else l.strip()
                for l in value.split("\n") if l.strip()]
    return [str(v).strip() for v in value if str(v).strip()]


def as_notes(value):
    if not value:
        return []
    if isinstance(value, str):
        return [{"title": "Notes", "text": value.strip()}]
    out = []
    for n in value:
        if isinstance(n, str):
            out.append({"title": "Notes", "text": n.strip()})
        else:
            out.append({"title": str(n.get("title") or "Notes"), "text": str(n.get("text") or "").strip()})
    return [n for n in out if n["text"]]


def read_json(path):
    raw = json.loads(path.read_text(encoding="utf-8"))
    author = raw.get("author") or {}
    if isinstance(author, str):
        author = {"name": author}
    return {
        "title": raw.get("title"),
        "post": raw.get("post") or raw.get("text") or "",
        "comment": raw.get("first_comment") or raw.get("comment") or "",
        "checklist": as_list(raw.get("checklist")),
        "notes": as_notes(raw.get("notes")),
        "author": {"name": author.get("name"), "title": author.get("title") or author.get("headline"),
                   "avatar": author.get("avatar")},
        "image": raw.get("image"),
        "image_alt": raw.get("image_alt") or "",
    }


def read_markdown(path):
    """Front matter, then the post as plain text, then optional ## sections.

    ## First comment, ## Checklist and ## Notes are known; any other ## heading
    becomes a notes block with that title.
    """
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    meta = {}
    m = re.match(r"---\n(.*?)\n---\n?", text, re.S)
    if m:
        for line in m.group(1).split("\n"):
            k, sep, v = line.partition(":")
            if sep:
                v = re.sub(r"\s+#.*$", "", v)  # allow a trailing "# comment"
                meta[k.strip().lower()] = v.strip().strip('"').strip("'")
        text = text[m.end():]
    parts = re.split(r"^## +(.+?)\s*$", text, flags=re.M)
    post = parts[0].strip("\n").rstrip()
    comment, checklist, notes = "", [], []
    for title, body in zip(parts[1::2], parts[2::2]):
        body = body.strip()
        key = title.strip().lower()
        if key in ("first comment", "comment"):
            comment = body
        elif key in ("checklist", "check before publishing"):
            checklist = as_list(body)
        else:
            notes.append({"title": title.strip(), "text": body})
    return {
        "title": meta.get("title"),
        "post": post,
        "comment": comment,
        "checklist": checklist,
        "notes": [n for n in notes if n["text"]],
        "author": {"name": meta.get("author") or meta.get("name"),
                   "title": meta.get("headline") or meta.get("author_title"),
                   "avatar": meta.get("avatar")},
        "image": meta.get("image"),
        "image_alt": meta.get("image_alt", ""),
    }


def build(src):
    raw = read_json(src) if src.suffix.lower() == ".json" else read_markdown(src)
    post = raw["post"].replace("\r\n", "\n").strip("\n")
    if not post.strip():
        sys.exit(f"render.py: no post text in {src}")
    base = src.parent
    title = raw["title"] or next((l.strip() for l in post.split("\n") if l.strip()), "LinkedIn post")
    if len(title) > 80:
        title = title[:77].rsplit(" ", 1)[0] + "…"
    image = data_uri(raw["image"], base)
    return {
        "schema": 1,
        "title": title,
        "rendered": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "author": {"name": raw["author"]["name"] or "Your Name", "title": raw["author"]["title"] or None,
                   "avatar": data_uri(raw["author"]["avatar"], base)},
        "limits": {"chars": POST_LIMIT, "comment": COMMENT_LIMIT, "line": MAX_LINE},
        "post": post,
        "comment": raw["comment"].strip(),
        "image": {"src": image, "alt": raw["image_alt"]} if image else None,
        "checklist": raw["checklist"],
        "notes": raw["notes"],
    }


# ---------------------------------------------------------------- output

def render(data, template=TEMPLATE):
    html = template.read_text(encoding="utf-8")
    # "</" inside a <script> block would close it early.
    blob = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    if not DATA_RE.search(html):
        sys.exit(f"render.py: no post-data block in {template}")
    return DATA_RE.sub(lambda m: m.group(1) + "\n" + blob + "\n" + m.group(3), html, count=1)


def report(data):
    """Counts and the feed cut, for the agent to read."""
    post = data["post"]
    n = len(post)
    ok = True
    lines = [f"length: {n} of {POST_LIMIT} characters" + (f"  OVER by {n - POST_LIMIT}" if n > POST_LIMIT else "")]
    ok &= n <= POST_LIMIT
    if data["comment"]:
        c = len(data["comment"])
        lines.append(f"first comment: {c} of {COMMENT_LIMIT} characters" + ("  OVER" if c > COMMENT_LIMIT else ""))
        ok &= c <= COMMENT_LIMIT
    for device, width in (("phone", PHONE_WIDTH), ("desktop", DESKTOP_WIDTH)):
        shown, _, _, more = feed_cut(post, width)
        good, msg = cut_verdict(post, device, width)
        lines.append(f"{device}, estimate at ~{width}/line: {'OK' if good else 'CHECK'}  {msg}")
        ok &= good
        for i, l in enumerate(shown):
            lines.append(f"    | {l}" + (" …more" if more and i == len(shown) - 1 else ""))
    if re.search(r"\*\*|^#{1,6} |`", post, re.M):
        lines.append("markdown: CHECK  LinkedIn shows ** # ` literally; use plain text")
        ok = False
    return "\n".join(lines), ok


def main():
    ap = argparse.ArgumentParser(description="Render a LinkedIn post into a preview page.")
    ap.add_argument("input", type=Path, help="post.json or post.md")
    ap.add_argument("-o", "--out", type=Path, help="output .html (default: next to the input)")
    ap.add_argument("--template", type=Path, default=TEMPLATE, help="page template")
    ap.add_argument("--check", action="store_true", help="print the report, write nothing")
    args = ap.parse_args()

    src = args.input.expanduser().resolve()
    if not src.is_file():
        sys.exit(f"render.py: no such file: {src}")
    data = build(src)
    text, ok = report(data)
    print(text)
    if args.check:
        sys.exit(0 if ok else 1)
    out = (args.out.expanduser() if args.out else src.with_suffix(".html")).resolve()
    if out == src:
        sys.exit("render.py: the output would overwrite the input")
    out.write_text(render(data, args.template), encoding="utf-8")
    print(f"page: {out}")


if __name__ == "__main__":
    main()
