# LinkedIn preview

**Version:** 2 · **Created:** 2026-10-28 20:22 · **Updated:** 2026-10-29 09:57

A Claude Code skill for writing LinkedIn posts. Ask Claude to write a post and
it hands you one HTML page instead of a block of text in the chat. The page
shows the post as the LinkedIn feed will show it, on a phone and on a
desktop, cut at "…more" where the feed cuts it. It also has an editor with a
live counter against LinkedIn's 3,000-character limit, a checklist of what to
confirm before you publish, notes on the choices Claude made, and buttons that
copy the post and the first comment.

The page is a single file and makes no network calls, so you can open it from
disk or send it to someone.

## See an example

[Open the example page](https://wipexpert.github.io/linkedin-preview/skills/linkedin-preview/examples/post.html): a finished post, rendered from
[`examples/post.md`](skills/linkedin-preview/examples/post.md). Try the
phone and desktop views, unfold the post, edit it and watch the cut move.
The file itself is
[`skills/linkedin-preview/examples/post.html`](skills/linkedin-preview/examples/post.html).

## Install

In Claude Code, at the prompt of a terminal session:

```
/plugin install linkedin-preview --marketplace WIPexpert/linkedin-preview
```

Answer `y` to add the marketplace, then pick a scope.

From a shell:

```bash
claude plugin install linkedin-preview --marketplace WIPexpert/linkedin-preview
```

In the Claude desktop app, click + next to the prompt box, then Plugins, Add
marketplace with `WIPexpert/linkedin-preview`, then Add plugin.

Then start a new session and ask: "write a LinkedIn post about our new
onboarding flow", or "turn these notes into a LinkedIn post".

You need Python 3.8 or later (standard library only) and a browser.

## More

How the skill works, the input format, the renderer and how the "…more" cut
is measured: [`skills/linkedin-preview/README.md`](skills/linkedin-preview/README.md).
