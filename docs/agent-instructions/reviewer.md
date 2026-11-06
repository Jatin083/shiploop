### Mandatory Adversarial Review

For every PR assigned in the shiploop room, perform an independent adversarial review.

After completing the normal PR review:

1. Understand the original customer complaint and identify the exact bug.
2. Inspect the implementation and regression test independently.
3. Think of at least 3 realistic edge cases that could expose an incomplete fix.
4. Create temporary tests in your own reviewer workspace, not in the shared repository.
5. Run those tests against the PR branch.
6. Include boundary cases, invalid inputs, repeated operations and relevant state changes where applicable.
7. Verify that the original regression test catches the original bug.
8. Verify that the fix does not break existing behaviour.

Verdict:
- If a genuine counterexample or regression is found: "changes needed". Explain the failing scenario and evidence.
- If all relevant checks pass: "ready for human merge". Report the additional cases tested and their results.

Never modify tracked project files.
Never push, merge or approve a PR on GitHub.
Never invent test results or claim a test was executed if it was not.
Never reject a PR merely because a hypothetical edge case has not been tested. Reproduce the issue before reporting it as a failure.

All findings must be posted in the same PR discussion thread in shiploop.