### ShipLoop Stopwatch

Track the lifecycle of every customer report in the same shiploop thread.

1. When a new customer report arrives, record its received timestamp in ISO 8601 format.
2. When fixer starts investigating, record the investigation start timestamp if available.
3. When fixer posts the PR link, record the PR creation/completion timestamp.
4. When the human confirms that the PR has been merged, record the human merge timestamp.
5. Calculate the elapsed time from complaint received to human-confirmed merge.
6. Post a concise stopwatch summary in the same thread.

Rules:
- Use actual timestamps from messages or reliable event metadata.
- Never invent timestamps.
- Never report PR creation as a completed fix.
- Never claim a PR was merged without human confirmation.
- If a timestamp is missing, clearly report that the duration cannot yet be calculated.
- Keep separate timestamps for each customer report.