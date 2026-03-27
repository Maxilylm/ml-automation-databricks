---
name: db-pipeline
description: "Build Spark data transformation pipelines. Generates modular ETL/ELT with Delta Lake, Delta Live Tables, or Structured Streaming."
aliases: [databricks pipeline, spark etl, delta live tables, spark streaming, databricks etl]
extends: ml-automation
user_invocable: true
---

# Databricks Pipeline

Build modular, testable data transformation pipelines on Databricks. Supports batch ETL with Delta Lake, Delta Live Tables (DLT) with data quality expectations, and Structured Streaming for real-time ingestion. Generates medallion architecture (bronze/silver/gold) with quality checks.

## Full Specification

See `commands/db-pipeline.md` for the complete workflow.
