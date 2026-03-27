---
name: db-coldstart
description: "Full Databricks ML workflow — connect, ingest to Delta Lake, EDA, feature engineering, Spark MLlib/sklearn training with MLflow, model registration, and optional serving deployment."
aliases: [databricks coldstart, databricks workflow, databricks ml pipeline, databricks end to end]
extends: ml-automation
user_invocable: true
---

# Databricks Coldstart

Run the complete Databricks ML lifecycle from data ingestion to deployment. Loads data into Delta Lake, runs EDA, builds Spark MLlib or MLflow-tracked sklearn pipelines, performs hyperparameter tuning with CrossValidator, registers the best model, and optionally deploys to a serving endpoint.

## Full Specification

See `commands/db-coldstart.md` for the complete workflow.
