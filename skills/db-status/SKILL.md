---
name: db-status
description: "Check Databricks workspace resources — clusters, jobs, models, serving endpoints, and Delta tables with health alerts."
aliases: [databricks status, databricks check, databricks resources, databricks health, workspace status]
extends: ml-automation
user_invocable: true
---

# Databricks Status

Check the status of all Databricks workspace resources. Lists clusters (with idle detection), jobs (with failure alerts), registered models (with stale staging warnings), serving endpoints (with traffic stats), and Delta tables (with maintenance recommendations). Outputs a formatted dashboard with actionable alerts.

## Full Specification

See `commands/db-status.md` for the complete workflow.
