---
name: db-status
description: "Check Databricks workspace resources — clusters, jobs, models, serving endpoints, and Delta tables with health alerts."
aliases: [databricks status, databricks check, databricks resources, databricks health, workspace status]
extends: ml-automation
user_invocable: true
---

# Databricks Status

Check the status of all Databricks workspace resources. Lists clusters (with idle detection), jobs (with failure alerts), registered models (with stale staging warnings), serving endpoints (with traffic stats), and Delta tables (with maintenance recommendations). Outputs a formatted dashboard with actionable alerts.

## When to Use

- You want a quick health check of your Databricks workspace before starting work.
- You need to identify idle clusters, failing jobs, or stale model versions that require attention.
- You are troubleshooting and want a consolidated view of all workspace resources in one place.

## Workflow

1. **Env Check** -- Validate Databricks connection and API token permissions.
2. **Query Resources** -- Call the Databricks REST API for the requested resource types (`--resource` flag). Aggregate cluster states, job run histories, registered model versions, serving endpoint health, and Delta table statistics. Format results as a dashboard with actionable alerts (idle clusters, consecutive job failures, models stuck in staging).

## Report Bus Integration

Emits `databricks_status_report.json` containing per-resource-type listings, health alerts, and a summary dashboard with counts and action items.

## Full Specification

Usage: `/db-status [--resource clusters|jobs|models|endpoints|tables|all]`

See `commands/db-status.md` for the complete workflow.
