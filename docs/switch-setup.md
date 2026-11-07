# Switch Setup Guide

This guide explains how to configure the ShipLoop multi-agent workflow using Switch.

## 1. Prerequisites

Install and configure:

- Windows 11, macOS or Linux
- Docker Desktop
- Git
- Python 3.13
- Node.js
- Switch Console and switch-core
- Claude Code
- GitHub CLI
- GitHub account
- Discord, connected through Switch, for the final demo
- Mattermost through Switch, as the fallback

## 2. Start Switch and Mattermost

1. Start Docker Desktop.
2. Start Switch Console.
3. Open Switch Console.
4. Navigate to Home → Messaging apps → Mattermost.
5. Select Open in Mattermost.
6. Confirm that Mattermost is accessible.

### Connect Discord

Follow the official guide: https://docs.switchagents.ai/switch-rooms/deploy/messaging-apps/discord.md

In short:

1. Create a Discord server and a bot in the Discord Developer Portal.
2. Turn on Server Members Intent and Message Content Intent.
3. Invite the bot with the permissions the guide lists. Agent replies fail without **Manage Webhooks**.
4. In Switch Console, go to Home → Messaging apps → Connect → Discord. Enter the bot token and server ID.
5. Link your Discord account with **This is me**.

Keep the bot token secret. Enter it only in Switch Console.

### Troubleshooting on Windows

- **`address already in use`, but no program holds the port:** Windows may have reserved that port range. Check with `netsh interface ipv4 show excludedportrange protocol=tcp`. To clear it, quit Docker Desktop and Switch Console, then run `net stop winnat` and `net start winnat` as administrator.
- **Claude Code shows `CLI not installed` while the same panel finds its version:** this label appeared in Switch Console 0.40.1 on Windows, and agents still ran. Do not reinstall because of the label alone.

## 3. Create the Shared Room

Create one shared room. The final demo uses the Discord channel `#shiploop-demo`. The Mattermost fallback room is named:

`shiploop`

Configure three exclusive roles:

| Role | Agent |
|---|---|
| triager | triager |
| fixer | fixer |
| reviewer | reviewer |

All three agents must operate in the same shared room.

## 4. Configure the Agents

Create three Claude Code agents through Switch Console.

Assign their responsibilities:

- Triager: customer report classification and coordination.
- Fixer: bug reproduction, regression testing and pull requests.
- Reviewer: independent pull request review and adversarial testing.

Use the corresponding instruction files in:

`docs/agent-instructions/`

Each agent must connect to its addressed room and acquire its assigned role before performing work.

## 5. Connect GitHub

1. Authenticate GitHub CLI.
2. Clone the ShipLoop repository.
3. Ensure the fixer can create feature branches and pull requests.
4. Ensure the reviewer has permission to inspect pull requests and run tests.
5. Keep main-branch changes under human control.

Repository:

https://github.com/Jatin083/shiploop

## 6. Start the Demo API

Follow the main README setup instructions.

Run:

`python -m uvicorn app.main:app --reload`

API documentation:

`http://127.0.0.1:8000/docs`

## 7. Verify Agent Roles

In the shared room, execute:

`!roles`

Expected role holders:

- triager
- fixer
- reviewer

Use `!agents-status` to inspect agent availability without intentionally waking agents.

## 8. Run the Workflow

1. Submit a customer complaint in the shared room.
2. Let triager classify it.
3. For a bug, let fixer investigate and open a PR.
4. Let reviewer independently examine the PR.
5. Inspect the review findings.
6. Human reviews and merges the PR.
7. Human confirms the merge to triager.
8. Approve the drafted customer update.

## 9. Safety Rules

- Agents never merge pull requests.
- Agents never push to main.
- Customer replies require human approval.
- Review findings must be based on executed checks.
- Never expose API keys, passwords or access tokens in the repository.

## 10. Important

Cloning the ShipLoop repository provides the FastAPI demo application and documentation. Switch Console, Mattermost and Claude Code must be configured separately.

The exact Switch installation and configuration requirements may change with Switch releases. Consult the official documentation:

https://docs.switchagents.ai/llms.txt