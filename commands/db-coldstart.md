# /db-coldstart

Full end-to-end Databricks ML workflow. Connects to workspace, loads data into Delta Lake, trains a model with Spark MLlib or MLflow, and deploys to a serving endpoint.

## Usage

```
/db-coldstart <data_source> [--catalog <catalog>] [--schema <schema>] [--target <column>] [--deploy]
```

- `data_source`: path to CSV/Parquet/Delta table, or SQL query
- `--catalog`: Unity Catalog catalog (default: `main`)
- `--schema`: Unity Catalog schema (default: `default`)
- `--target`: target column for supervised learning
- `--deploy`: auto-deploy best model to serving endpoint after training

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` — if missing, copy from core plugin
2. Check if `databricks_utils.py` exists in `src/` — if missing, copy from this plugin's `templates/databricks_utils.py`
3. Verify Databricks connection (run `/db-connect` if not configured)
4. Check cluster is RUNNING — start if TERMINATED
5. Report: connection status, cluster state, runtime version

### Stage 1: Data Ingestion

1. Detect data source type:
   - Local CSV/Parquet: upload to DBFS, read with Spark
   - DBFS path: read directly
   - Delta table: `spark.read.table("catalog.schema.table")`
   - SQL query: `spark.sql(query)`
2. Load into Spark DataFrame
3. Write to Delta table in Unity Catalog: `catalog.schema.raw_<name>`
4. Report: row count, column count, schema, null percentages

### Stage 2: Exploratory Data Analysis

1. Use core `eda-analyst` agent for standard EDA
2. Databricks-specific additions:
   - Delta table history and versioning info
   - Data profile using `dbutils.data.summarize(df)`
   - Partition analysis (if partitioned)
   - File size and format statistics
3. Write EDA results to Delta table: `catalog.schema.eda_<name>`

### Stage 3: Feature Engineering

1. Detect column types and apply transformations:
   - Numeric: `StandardScaler`, `MinMaxScaler`, `Imputer`
   - Categorical: `StringIndexer` + `OneHotEncoder`
   - Text: `Tokenizer` + `HashingTF` or `Word2Vec`
   - Date/timestamp: extract features (year, month, day, hour, dayofweek)
2. Assemble features with `VectorAssembler`
3. Create Spark ML Pipeline with all stages
4. Save feature-engineered data to Delta: `catalog.schema.features_<name>`
5. Register feature table in Feature Store (if available)

### Stage 4: Model Training

1. Split data: train/validation/test (60/20/20)
2. Select algorithms based on task type:
   - Classification: LogisticRegression, RandomForestClassifier, GBTClassifier
   - Regression: LinearRegression, RandomForestRegressor, GBTRegressor
3. Create MLflow experiment
4. For each algorithm:
   - Build Pipeline (preprocessor + model)
   - Configure ParamGrid for hyperparameter search
   - Run CrossValidator (3-fold default)
   - Log parameters, metrics, model to MLflow
5. Compare runs, select best model
6. Report: best model type, best metrics, MLflow experiment URL

### Stage 5: Model Evaluation

1. Evaluate best model on test set:
   - Classification: accuracy, precision, recall, F1, AUC-ROC, confusion matrix
   - Regression: RMSE, MAE, R2, MAPE
2. Feature importance analysis
3. Generate predictions DataFrame
4. Save evaluation results to Delta: `catalog.schema.eval_<name>`
5. Log evaluation metrics to MLflow

### Stage 6: Model Registration

1. Register best model in MLflow Model Registry
2. Add model description and tags
3. Transition to "Staging" stage
4. Log model signature and input example
5. If Unity Catalog: register as `catalog.schema.model_<name>`

### Stage 7: Deployment (if --deploy)

1. Create model serving endpoint (or update existing)
2. Configure auto-scaling (min 1, max 4 instances)
3. Wait for endpoint to reach READY state
4. Run smoke test: send sample prediction request
5. Report: endpoint URL, latency, status

### Stage 8: Report

```python
from ml_utils import save_agent_report
save_agent_report("databricks-ml-engineer", {
    "status": "completed",
    "command": "db-coldstart",
    "delta_tables": created_tables,
    "mlflow_experiment": experiment_url,
    "best_model": {"type": model_type, "metrics": best_metrics},
    "registry": {"name": model_name, "version": model_version},
    "serving_endpoint": endpoint_url,
    "recommendations": recommendations
})
```

Print: summary table with all stages, metrics, and next steps.
