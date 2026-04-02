---
name: db-spark
description: "Generate PySpark code from natural language. Produces optimized Spark DataFrame or Spark SQL code with proper conventions."
aliases: [pyspark generate, spark code, spark sql, pyspark help]
extends: spark
user_invocable: true
---

# Databricks Spark

Generate production-ready PySpark code from natural language descriptions. Supports DataFrame API and Spark SQL output, with optional performance optimization hints. Can output as Databricks notebooks or standalone Python scripts.

## When to Use

- You need PySpark or Spark SQL code and want to describe the transformation in plain English instead of writing it from scratch.
- You want optimized Spark code that follows Databricks best practices (broadcast joins, partition pruning, Z-ordering hints).
- You need to quickly scaffold a notebook or script for a one-off data exploration or transformation task.

## Workflow

1. **Env Check** -- Validate Databricks connection and confirm PySpark availability on the target cluster.
2. **Parse Intent** -- Analyze the natural language description to identify source tables, transformations, joins, aggregations, filters, and output format.
3. **Generate Code** -- Produce the PySpark DataFrame API or Spark SQL code. When `--optimize` is passed, add performance annotations (repartition, cache, broadcast hints). Output as a Databricks notebook (`--output notebook`) or standalone Python script (`--output script`).

## Report Bus Integration

Emits `databricks_spark_report.json` containing the parsed intent summary, generated code path, output format, and any optimization hints applied.

## Full Specification

Usage: `/db-spark "<description>" [--output notebook|script] [--sql] [--optimize]`

Agent: `databricks-engineer`

See `commands/db-spark.md` for the complete workflow.
