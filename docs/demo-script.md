# ShipLoop — Hackathon Demo Script

**Target duration:** 2–3 minutes

**Tagline:** From customer complaint to merged fix, without leaving chat.

## Scene 1 — The Problem (0:00–0:20)

Show the ShipLoop Mattermost room.

Narration:

"Customer bugs often get stuck between support and engineering. ShipLoop connects customer reports, AI agents and human approval through one shared chat workflow powered by Switch."

## Scene 2 — Customer Complaint (0:20–0:45)

Show the customer complaint:

"You had exactly 5 monitors left. I tried to buy all 5, but checkout said there wasn't enough stock. Why can't I buy them?"

Show Triager classifying it as a bug and handing it to Fixer in the same thread.

Narration:

"Triager understands the customer's language, identifies the issue and hands it to the engineering agent."

## Scene 3 — Automated Fix (0:45–1:25)

Show Fixer working.

Highlight:

- Bug reproduction.
- Regression test failing before the fix.
- Minimal code change.
- Full test suite passing.
- GitHub pull request creation.

Narration:

"Fixer reproduces the problem, writes a regression test, implements the smallest fix and opens a pull request."

## Scene 4 — Independent Review (1:25–1:55)

Show Reviewer inspecting the pull request.

Highlight:

- Review findings.
- Additional edge-case tests.
- Test results.
- Review verdict.

Narration:

"Reviewer independently challenges the proposed fix instead of blindly trusting the implementation."

Only show adversarial tests and results that were genuinely executed.

## Scene 5 — Human Approval (1:55–2:20)

Show the GitHub pull request and human merge action.

Narration:

"Agents never merge code or send customer replies independently. The human makes the final decision."

## Scene 6 — Closing (2:20–2:40)

Show the ShipLoop architecture and repository.

Narration:

"ShipLoop turns customer complaints into reviewed engineering fixes through one coordinated AI and human workflow, powered by Switch."

## Recording Checklist

- [ ] Mattermost shared room visible.
- [ ] Customer complaint visible.
- [ ] Triager classification visible.
- [ ] Fixer regression test visible.
- [ ] GitHub PR visible.
- [ ] Reviewer findings visible.
- [ ] Human merge decision visible.
- [ ] Final project architecture visible.

## Disclosure

The shopping API is a demonstration application containing deliberately planted bugs. The video must clearly disclose this.

Do not present simulated timestamps, unexecuted tests or planned functionality as completed features.