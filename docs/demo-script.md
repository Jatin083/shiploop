# ShipLoop — Hackathon Demo Script

**Target duration:** 2–3 minutes

**Tagline:** From customer complaint to merged fix, without leaving chat.

## Scene 1 — The Problem (0:00–0:20)

Show the repository, then Discord `#shiploop-demo`.

Narration:

"Customer bugs often get stuck between support and engineering. ShipLoop connects customer reports, AI agents and human approval in one chat room, powered by Switch. This is a demo shop with deliberately planted bugs."

## Scene 2 — Customer Complaint (0:20–0:45)

Show the kept customer complaint in `#shiploop-demo`:

"I cancelled my order for 2 monitors, then the page froze so I pressed cancel again. Now your site shows 7 monitors in stock, but you only had 5. Something looks wrong."

Show Triager classifying it as a bug and handing it to Fixer.

Narration:

"Triager reads the customer's own words, identifies a bug and hands it to Fixer."

## Scene 3 — Fix and Pull Request (0:45–1:20)

Show Fixer's messages, then PR #6 on GitHub.

Highlight:

- Before the fix: 1 failed, 40 passed.
- After the fix: 41 passed.
- The small change in `app/orders.py`.

Narration:

"Fixer reproduces the problem, writes a failing test, makes the fix and opens a real pull request."

## Scene 4 — Independent Review (1:20–1:50)

Show Reviewer's findings in Discord.

Highlight:

- 11 extra edge-case tests passed on the fix.
- The same tests on the old code: 7 failed, 4 passed.
- The limitations Reviewer reported.

Narration:

"Reviewer does not just trust Fixer. It writes its own edge-case tests, and shows that they catch the old bug."

## Scene 5 — Human Merge (1:50–2:15)

Show PR #6 merged on GitHub, then the stopwatch result in Discord.

Narration:

"Agents do not merge. A human made that decision. From the kept complaint to the human merge took 3 minutes and 6 seconds."

## Scene 6 — Customer Update and Limits (2:15–2:40)

Show Triager's customer update draft.

Narration:

"Triager drafts an honest update for human approval. This draft was not sent. The fix is merged in a demo app with no production deployment, and stock that was already wrong is not repaired. That is ShipLoop: from customer complaint to merged fix, without leaving chat."

## Recording Checklist

- [ ] Say that the shop is a demo with planted bugs.
- [ ] Customer complaint visible.
- [ ] Triager classification and handoff visible.
- [ ] Fixer test results visible.
- [ ] PR #6 visible.
- [ ] Reviewer findings visible.
- [ ] Human merge visible.
- [ ] Stopwatch result visible: 3 minutes 6.33 seconds.
- [ ] Customer update draft shown as not sent.
- [ ] No token, password or other secret on screen.

## Accuracy Notes

- The complaint was accidentally posted three times. Show the kept report and do not describe the duplicates as separate customers.
- The time runs from the latest post to the human merge.
- Do not say the fix is live on a website.
- Do not claim Copilot approval.
- Do not present simulated timestamps, unexecuted tests or planned functionality as completed features.
