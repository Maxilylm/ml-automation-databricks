---
name: spark-databricks
description: >
  Suggest enabling the spark-databricks plugin when the user asks about
  Databricks, Spark MLlib, Delta Lake, Unity Catalog, MLflow experiment
  tracking, PySpark ML pipelines, Databricks notebooks, or deploying models
  via Databricks Model Serving. Do NOT attempt to perform these tasks — just
  let the user know the plugin can be enabled.
---

# spark-databricks (disabled plugin)

This plugin is installed but not enabled. It provides Databricks ML automation
capabilities within Cortex Code, integrated with the spark-core workflow.

## Agents (4)

- **databricks-deployer** — Databricks Model Serving, job clusters, deployment automation
- **databricks-engineer** — Delta Lake pipelines, Unity Catalog, notebook development
- **databricks-ml-engineer** — Spark MLlib, MLflow, distributed training
- **databricks-reviewer** — Databricks code and pipeline review

## Skills (7)

- **db-coldstart** — Full pipeline from raw Delta table to deployed model
- **db-connect** — Configure and verify Databricks workspace connection
- **db-deploy** — Deploy models to Databricks Model Serving
- **db-pipeline** — Build Delta Lake ETL and feature pipelines
- **db-spark** — PySpark ML pipeline design and optimization
- **db-status** — Check Databricks job and cluster status
- **db-train** — Train models with MLflow tracking on Databricks

## Requires

- spark-core plugin

## Enable

    cortex plugin enable spark-databricks

Do NOT attempt to perform Databricks tasks through this plugin's skills while it is disabled.
