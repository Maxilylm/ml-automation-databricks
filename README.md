# spark-databricks

Databricks development and ML automation extension for [ml-automation](https://github.com/BLEND360/ml-automation-core).

## Prerequisites

- [ml-automation](https://github.com/BLEND360/ml-automation-core) core plugin (>= v1.8.0)
- Claude Code CLI
- Databricks workspace access (workspace URL + authentication)
- PySpark (local development) or Databricks Runtime (workspace execution)

## Installation

```bash
claude plugin add /path/to/spark-databricks
```

## What's Included

### Agents

| Agent | Purpose | Hooks Into |
|---|---|---|
| `databricks-engineer` | Workspace development — notebooks, Spark jobs, Delta Lake, Unity Catalog | `after-init` |
| `databricks-ml-engineer` | Train and deploy ML models with Spark MLlib, MLflow, Feature Store | `before-deploy` |
| `databricks-reviewer` | Review Spark jobs for performance, cost optimization, best practices | `after-evaluation` |
| `databricks-deployer` | Deploy to model serving endpoints, scheduled jobs, Delta Live Tables | *(direct invocation)* |

### Commands

| Command | Purpose |
|---|---|
| `/db-connect` | Setup Databricks connection (workspace URL, token, cluster) |
| `/db-coldstart` | Full Databricks ML workflow (connect -> data -> train -> deploy) |
| `/db-spark` | Generate PySpark code from natural language |
| `/db-pipeline` | Build Spark data transformation pipeline |
| `/db-train` | Train model with Spark MLlib or MLflow-tracked sklearn |
| `/db-deploy` | Deploy to model serving, scheduled jobs, or Delta Live Tables |
| `/db-status` | Check workspace resources (clusters, jobs, models, endpoints) |

## Getting Started

```bash
# Connect to workspace
/db-connect --workspace https://adb-123.azuredatabricks.net --cluster abc-12345

# Full ML workflow
/db-coldstart data.csv --target label --deploy

# Generate PySpark code
/db-spark "join orders with customers on customer_id and aggregate total spend by month"

# Build ETL pipeline
/db-pipeline bronze_events --target main.analytics.silver_events --dlt

# Train a model
/db-train main.ml.features --target churn --framework spark

# Deploy to serving
/db-deploy --type serving --model churn_predictor --version 3

# Check workspace status
/db-status
```

## How It Integrates

When installed alongside the core plugin:

1. **Automatic routing** -- Tasks mentioning Databricks, Spark, Delta Lake, or MLflow are routed to Databricks agents
2. **Core workflow hooks** -- When running `/team-coldstart`:
   - `databricks-engineer` fires at `after-init` to detect and configure Databricks workspace
   - `databricks-ml-engineer` fires at `before-deploy` to handle Databricks-specific model deployment
   - `databricks-reviewer` fires at `after-evaluation` to review Spark performance
3. **Core agent reuse** -- Commands use eda-analyst, developer, ml-theory-advisor from core

## License

MIT
