---
name: hermes-tweet
description: Use when installing or operating Hermes Tweet, the Hermes Agent X/Twitter plugin for social discovery, tweet reads, and approval-gated actions through Xquik.
---

# Hermes Tweet

Hermes Tweet adds X/Twitter workflows to Hermes Agent. It exposes three tool groups:

- Explore the bundled route catalog without network access.
- Read public X/Twitter data when `XQUIK_API_KEY` is configured.
- Execute write actions only when `HERMES_TWEET_ENABLE_ACTIONS=true` is explicitly set.

## Install

Install the Hermes Agent runtime plugin from its source repository:

```bash
hermes plugins install Xquik-dev/hermes-tweet
```

Set the required read credential before using networked read tools:

```bash
export XQUIK_API_KEY=...
```

Enable write actions only for workflows that have clear user approval and rollback expectations:

```bash
export HERMES_TWEET_ENABLE_ACTIONS=true
```

## Workflow

1. Search the bundled endpoint catalog first for the needed X/Twitter route.
2. Read data through `tweet_read` only after confirming `XQUIK_API_KEY` is present.
3. Keep write flows behind explicit approval and the `HERMES_TWEET_ENABLE_ACTIONS=true` gate.
4. Treat returned JSON as the source of truth and avoid inventing account, tweet, or action state.
5. Never log, paste, or commit API keys.

## Fit

Use Hermes Tweet for social listening, support triage, giveaway audits, and controlled publishing workflows that need Hermes Agent plus X/Twitter data.
