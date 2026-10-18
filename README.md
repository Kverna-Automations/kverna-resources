# Kverna resources

Real Kverna workspaces, published as they are. They run on my own setup against public or sample
data, so you (or your agent) can see how [Kverna](https://kverna.com) actually works: the
pipelines it builds, the conversations that built them, the run records behind a result, and
dashboards that keep themselves up to date.

Nothing here is staged for the occasion. It's dogfooding: the same workspaces I use.

## What's here

| Workspace | What it is |
|---|---|
| [`invoice_normalizer/`](invoice_normalizer/) | Invoices in two formats plus daily FX rates, normalised and enriched into one table. Two dashboards that refresh on a schedule. |
| [`claude-tests-agent/`](claude-tests-agent/) | A source capability inventory and a small reproducible probe of Norwegian public data: power prices, NOK/EUR, reservoir levels, SSB metadata. Every figure is tied to a raw file and its SHA-256. |

## A workspace, file by file

| Path | What it holds |
|---|---|
| `kverna.json` | Marks the folder as a Kverna workspace. |
| `pipelines/*.json` | The pipelines: every step, its SQL or Python, and how steps connect. Plain JSON, and exactly what reruns. |
| `conversations/*.json` | The agent conversations that built them, every tool call included. Kverna redacts secrets before saving. |
| `runs/*.json` | Run records: when it ran, the exact pipeline definition that ran (with its hash), and what each step produced. Only the latest run of each pipeline is kept here. |
| `dashboards/<name>/` | A dashboard's spec (`dashboard.json`), its data, its history, and its provenance: which step produced each figure. |
| `audit/` | The agent's tool log. |

## Live dashboards

Published with GitHub Pages from the `gh-pages` branch:
<https://kverna-automations.github.io/kverna-resources/>

That branch is written by Kverna's scheduled pipelines and holds only the published pages. Don't
edit it by hand; the next publish replaces it.

## What's left out

- Older run records. Some pipelines here run every minute, so there are thousands.
- Generated dashboard pages (`index.html`). They're rebuilt on every run and served from `gh-pages`.
- Local log files.

## About the identifiers

Resource names appear as they are: the storage account, the Microsoft tenant, the app IDs. They
identify; they don't grant access. Keys and passwords live in Windows Credential Manager on the
machine that runs Kverna, never in a workspace.
