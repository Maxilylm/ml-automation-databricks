---
name: db-pipeline
description: "Build Spark data transformation pipelines. Generates modular ETL/ELT with Delta Lake, Delta Live Tables, or Structured Streaming."
aliases: [databricks pipeline, spark etl, delta live tables, spark streaming, databricks etl]
extends: spark
user_invocable: true
---

# Databricks Pipeline

Build modular, testable data transformation pipelines on Databricks. Supports batch ETL with Delta Lake, Delta Live Tables (DLT) with data quality expectations, and Structured Streaming for real-time ingestion. Generates medallion architecture (bronze/silver/gold) with quality checks.

## When to Use

- You need to build a repeatable ETL/ELT pipeline that reads from one or more sources and writes to Delta Lake tables.
- You want a Delta Live Tables pipeline with declarative data quality expectations and automatic dependency management.
- You need a Structured Streaming pipeline for near-real-time ingestion from Kafka, Event Hubs, or Auto Loader sources.
- You are implementing a medallion architecture and want scaffold code for bronze, silver, and gold layers.

## Workflow

1. **Env Check** -- Validate Databricks connection, target Delta table permissions, and (for DLT) DLT-enabled cluster availability.
2. **Source Analysis** -- Profile the source data: schema inference, row counts, partitioning strategy, and incremental load feasibility.
3. **Pipeline Design** -- Generate the pipeline code. For batch: PySpark with Delta writes and merge/upsert logic. For DLT (`--dlt`): `@dlt.table` decorated functions with `expect` quality rules. For streaming (`--streaming`): Structured Streaming with checkpointing and trigger configuration. Includes scheduling via `--schedule <cron>`.

## Report Bus Integration

Emits `databricks_pipeline_report.json` containing source profile, pipeline type (batch/DLT/streaming), generated code paths, schedule expression, and target table details.

## Full Specification

Usage: `/db-pipeline <source> --target <delta_table> [--schedule <cron>] [--dlt] [--streaming]`

Agent: `databricks-engineer`

See `commands/db-pipeline.md` for the complete workflow.
