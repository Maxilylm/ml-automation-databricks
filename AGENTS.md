# spark-databricks — Cortex Code Extension

Databricks ML automation. Spark MLlib, Delta Lake, Unity Catalog, MLflow integration, and Databricks deployment. Requires spark-core installed.

## Available Agents

| Agent | When to use |
|---|---|
| `databricks-engineer` | User wants to write PySpark code, manage Delta Lake tables, configure Unity Catalog, or build Spark pipelines |
| `databricks-ml-engineer` | User wants to train with Spark MLlib, use MLflow tracking, or run distributed ML on Databricks |
| `databricks-deployer` | User wants to deploy models via MLflow Model Serving, create Databricks Jobs, or schedule workflows |
| `databricks-reviewer` | User wants query optimization, Delta Lake best practices, or cost review |

## Available Skills

| Skill | Trigger |
|---|---|
| `/db-connect` | "connect to Databricks", "configure Databricks credentials", "test Databricks connection" |
| `/db-coldstart` | "full Databricks ML workflow", "end to end on Databricks", "Databricks coldstart" |
| `/db-spark` | "PySpark code", "Spark DataFrame operations", "optimize Spark job", "Delta table" |
| `/db-pipeline` | "Databricks pipeline", "Delta Live Tables", "Spark streaming pipeline" |
| `/db-train` | "train with MLlib", "distributed training on Databricks", "MLflow experiment" |
| `/db-deploy` | "deploy on Databricks", "MLflow Model Serving", "Databricks Job", "schedule workflow" |
| `/db-status` | "Databricks resource status", "list MLflow runs", "check Delta tables" |

## Routing

- PySpark, Delta Lake, Unity Catalog → `databricks-engineer`
- MLlib, MLflow, distributed ML → `databricks-ml-engineer`
- Model serving, Jobs, workflows → `databricks-deployer`
- Optimization, best practices → `databricks-reviewer`
- Fallback → spark-core orchestrator
