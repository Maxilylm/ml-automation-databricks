---
name: db-train
description: "Train ML models on Databricks with Spark MLlib or MLflow-tracked sklearn. Handles feature engineering, hyperparameter tuning, and model registration."
aliases: [databricks train, spark ml, spark mllib, databricks model, mlflow train]
extends: spark
user_invocable: true
---

# Databricks Train

Train machine learning models on Databricks. Automatically selects Spark MLlib (for large datasets) or scikit-learn with MLflow tracking (for smaller datasets). Includes automated feature engineering, hyperparameter search with CrossValidator, experiment tracking, evaluation, and Model Registry registration.

## When to Use

- You have a prepared dataset in Delta Lake and want to train a model with full MLflow experiment tracking.
- You need automatic framework selection based on data size (Spark MLlib for distributed training vs. sklearn for single-node).
- You want hyperparameter tuning, cross-validation, and model registration handled in a single command.
- You are iterating on model performance and want comparable MLflow runs across experiments.

## Workflow

1. **Env Check** -- Validate Databricks connection, confirm MLflow tracking server access, and check cluster compute resources.
2. **Data Profiling** -- Load the target dataset, profile features (types, cardinality, missing rates), detect the task type (classification/regression), and recommend a train/test split strategy.
3. **Training (MLflow)** -- Select the framework (Spark MLlib or sklearn) based on data size and user preference. Build a feature pipeline, run hyperparameter search via CrossValidator or Hyperopt, log all runs to the MLflow experiment, evaluate the best model on held-out data, and register it in the Model Registry.

## Report Bus Integration

Emits `databricks_train_report.json` containing data profile summary, framework used, hyperparameter search space, best model metrics, MLflow run ID, and registered model name/version.

## Full Specification

Usage: `/db-train <data_source> --target <col> [--algorithm <algo>] [--framework spark|sklearn]`

Agent: `databricks-ml-engineer`

See `commands/db-train.md` for the complete workflow.
