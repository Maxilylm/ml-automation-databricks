---
name: db-connect
description: "Setup Databricks workspace connection. Configures authentication (PAT, OAuth, Service Principal), validates cluster access, and stores connection profile."
aliases: [databricks connect, databricks auth, databricks login, databricks setup]
extends: ml-automation
user_invocable: true
---

# Databricks Connect

Configure and validate a Databricks workspace connection. Supports Personal Access Token, OAuth, Service Principal, and Azure CLI authentication methods. Validates cluster access, checks Unity Catalog availability, and generates project configuration files.

## When to Use

- You are setting up a new project that needs Databricks access and want to configure authentication once.
- You need to verify that your Databricks workspace, token, and cluster are reachable before running other db-* commands.
- You want to switch between Databricks workspaces or authentication profiles.

## Workflow

1. **Env Check** -- Detect existing Databricks configuration from environment variables (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`), `~/.databrickscfg`, or project-level `config/databricks_config.json`.
2. **Authentication Setup** -- Configure the chosen auth method (PAT, OAuth, Service Principal, or Azure CLI). Validate the token against the workspace REST API, confirm cluster connectivity, check Unity Catalog access, and write the connection profile to the project config directory.

## Report Bus Integration

Emits `databricks_connect_report.json` containing workspace URL, auth method, cluster ID, cluster state, Unity Catalog availability flag, and validation status.

## Full Specification

Usage: `/db-connect [--workspace <url>] [--token <pat>] [--cluster <id>]`

Agent: `databricks-engineer`

See `commands/db-connect.md` for the complete workflow.
