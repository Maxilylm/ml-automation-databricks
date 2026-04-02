---
name: db-deploy
description: "Deploy models and pipelines to Databricks — model serving endpoints, scheduled jobs, or Delta Live Tables pipelines."
aliases: [databricks deploy, databricks serve, databricks endpoint, databricks job, model serving]
extends: ml-automation
user_invocable: true
---

# Databricks Deploy

Deploy ML models and data pipelines to Databricks production infrastructure. Supports real-time model serving endpoints with auto-scaling, scheduled workflow jobs with retry policies, and Delta Live Tables pipelines. Includes smoke testing, inference logging, cost estimation, and rollback instructions.

## When to Use

- You have a registered model in MLflow Model Registry and want to expose it via a real-time serving endpoint.
- You need to schedule a batch inference or ETL job with retry policies and alerting.
- You want to deploy a Delta Live Tables pipeline with data quality expectations to production.
- You need deployment artifacts with smoke tests, cost estimates, and rollback procedures.

## Workflow

1. **Env Check** -- Validate Databricks connection, confirm the target model or pipeline exists, and check workspace permissions for serving/job creation.
2. **Deployment** -- Based on `--type`:
   - **serving** -- Create or update a model serving endpoint with auto-scaling configuration, traffic routing, and inference logging. Run a smoke test request.
   - **job** -- Create a Databricks Workflow job with the specified notebook or Python task, schedule, retry policy, and alerting configuration.
   - **dlt** -- Deploy a Delta Live Tables pipeline with quality expectations, target schema, and cluster policy.

## Report Bus Integration

Emits `databricks_deploy_report.json` containing deployment type, resource ID (endpoint name / job ID / pipeline ID), status, endpoint URL (for serving), schedule (for jobs), smoke test result, and rollback instructions.

## Full Specification

Usage: `/db-deploy [--type serving|job|dlt] [--model <name>]`

Agent: `databricks-deployer`

See `commands/db-deploy.md` for the complete workflow.
