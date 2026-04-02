---
name: db-coldstart
description: "Full Databricks ML workflow — connect, ingest to Delta Lake, EDA, feature engineering, Spark MLlib/sklearn training with MLflow, model registration, and optional serving deployment."
aliases: [databricks coldstart, databricks workflow, databricks ml pipeline, databricks end to end]
extends: spark
user_invocable: true
---

# Databricks Coldstart

Run the complete Databricks ML lifecycle from data ingestion to deployment. Loads data into Delta Lake, runs EDA, builds Spark MLlib or MLflow-tracked sklearn pipelines, performs hyperparameter tuning with CrossValidator, registers the best model, and optionally deploys to a serving endpoint.

## When to Use

- You have raw data in a Databricks workspace (or accessible storage) and want to go from zero to a trained, registered model in one pass.
- You need an end-to-end pipeline that covers ingestion, EDA, feature engineering, training, and optional deployment on Databricks.
- You want MLflow experiment tracking and Model Registry integration out of the box.
- You are starting a new ML project on Databricks and want a production-grade scaffold with minimal setup.

## Workflow

1. **Env Check** -- Validate Databricks connection, cluster access, Unity Catalog availability, and required libraries (pyspark, mlflow, delta).
2. **Data Ingestion** -- Load data from the specified source into a Delta Lake table. Supports CSV, Parquet, JSON, JDBC, and existing Delta/Unity Catalog tables.
3. **EDA** -- Profile the ingested data: distributions, missing values, correlations, target-variable analysis, and class balance checks.
4. **Feature Engineering** -- Apply automated transformations: encoding, scaling, imputation, datetime extraction, and interaction features. Writes the feature table back to Delta.
5. **Training (MLflow)** -- Train models with Spark MLlib (large data) or scikit-learn (smaller data). Runs hyperparameter tuning via CrossValidator, logs all runs to an MLflow experiment.
6. **Model Registration** -- Register the best model version in the MLflow Model Registry with tags, description, and lineage metadata.
7. **Optional Deploy** -- When `--deploy` is passed, create a real-time serving endpoint or a scheduled batch inference job for the registered model.

## Report Bus Integration

Emits `databricks_coldstart_report.json` containing stage-level status, ingested table path, EDA summary, best model metrics, registered model URI, and deployment endpoint URL (if deployed).

## Full Specification

Usage: `/db-coldstart <data_source> [--catalog <catalog>] [--schema <schema>] [--target <col>] [--deploy]`

Agents: `databricks-engineer`, `databricks-ml-engineer`

See `commands/db-coldstart.md` for the complete workflow.
