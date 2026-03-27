---
name: db-train
description: "Train ML models on Databricks with Spark MLlib or MLflow-tracked sklearn. Handles feature engineering, hyperparameter tuning, and model registration."
aliases: [databricks train, spark ml, spark mllib, databricks model, mlflow train]
extends: ml-automation
user_invocable: true
---

# Databricks Train

Train machine learning models on Databricks. Automatically selects Spark MLlib (for large datasets) or scikit-learn with MLflow tracking (for smaller datasets). Includes automated feature engineering, hyperparameter search with CrossValidator, experiment tracking, evaluation, and Model Registry registration.

## Full Specification

See `commands/db-train.md` for the complete workflow.
