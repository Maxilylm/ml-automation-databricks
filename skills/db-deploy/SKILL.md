---
name: db-deploy
description: "Deploy models and pipelines to Databricks — model serving endpoints, scheduled jobs, or Delta Live Tables pipelines."
aliases: [databricks deploy, databricks serve, databricks endpoint, databricks job, model serving]
extends: ml-automation
user_invocable: true
---

# Databricks Deploy

Deploy ML models and data pipelines to Databricks production infrastructure. Supports real-time model serving endpoints with auto-scaling, scheduled workflow jobs with retry policies, and Delta Live Tables pipelines. Includes smoke testing, inference logging, cost estimation, and rollback instructions.

## Full Specification

See `commands/db-deploy.md` for the complete workflow.
