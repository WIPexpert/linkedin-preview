# LinkedIn preview

**Version:** 4 · **Created:** 2026-10-28 20:22 · **Updated:** 2026-10-29 17:18

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

## Why I made this

<div style="display:flex;gap:16px;align-items:flex-start;padding:18px 20px;border-radius:16px;background:#f6f3ff;border:1px solid #e2dbff;margin:0 0 16px">
  <a href="https://talenthunt.work/?utm_source=lipv&utm_medium=btn&utm_campaign=signup&utm_content=readme"><img src="assets/talenthunt-logo.svg" alt="talenthunt" width="56" height="50"></a>
  <div>
    <p style="margin:0 0 10px">I'm Mike Daykhin, a solo founder. I write my LinkedIn posts with Claude, and every one of them still needed formatting inside LinkedIn before I could publish it. That is time I would rather spend on the product, so now Claude hands me the post the way the feed will show it, and I paste it once.</p>
    <p style="margin:0 0 14px">The product is <a href="https://talenthunt.work/?utm_source=lipv&utm_medium=btn&utm_campaign=signup&utm_content=readme">talenthunt</a>. It turns your CV into a live profile that answers questions from recruiters and AI agents, and it is always free for job seekers.</p>
    <a href="https://talenthunt.work/?utm_source=lipv&utm_medium=btn&utm_campaign=signup&utm_content=readme" style="display:inline-block;padding:8px 18px;border-radius:999px;background:#684BFF;color:#fff;font-weight:600;text-decoration:none">Make your talenthunt page</a>
  </div>
</div>

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

## More from me

- [Session Kit](https://github.com/WIPexpert/mikeday-session-kit): two
  Claude Code plugins for long sessions. `context-guard` shows how full the
  context is and asks what to do once it passes your threshold; `handoff`
  writes the session down as JSON, so a fresh session picks up what was
  actually done.
- [talenthunt job board](https://talenthunt.work/job-board?utm_source=lipv&utm_medium=btn&utm_campaign=board&utm_content=readme):
  every role comes with a fit check. Nothing is scraped: roles come from
  curators or from members, and a person reviews each member's role before
  it goes up.
- [Job post composer](https://talenthunt.work/for-recruiters/best-job-post?utm_source=lipv&utm_medium=btn&utm_campaign=genpost&utm_content=readme),
  for people who hire: paste a job description and get a LinkedIn post that
  tells candidates in seconds whether the role is theirs, with a fit check
  link. Free during the open beta.

## Contributing

Found a post the preview cuts in the wrong place, or LinkedIn changed its
layout? Open an issue with the post text and what you saw in the feed, or
send a pull request. Keep the page a single file with no network calls and
the renderer on the Python standard library.

## License

[MIT](LICENSE)
