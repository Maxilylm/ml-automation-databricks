# /db-train

Train a model on Databricks using Spark MLlib or MLflow-tracked scikit-learn. Handles feature engineering, hyperparameter tuning, experiment tracking, and model registration.

## Usage

```
/db-train <data_source> --target <column> [--algorithm <algo>] [--framework spark|sklearn] [--experiment <name>]
```

- `data_source`: Delta table, DBFS path, or Spark DataFrame reference
- `--target`: target column for prediction
- `--algorithm`: specific algorithm (auto-selects if omitted)
- `--framework`: Spark MLlib or scikit-learn with MLflow tracking (default: auto-detect based on data size)
- `--experiment`: MLflow experiment name (default: `/db-train/<timestamp>`)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` — if missing, copy from core plugin
2. Check if `databricks_utils.py` exists in `src/` — if missing, copy from this plugin's `templates/databricks_utils.py`
3. Verify Databricks connection and cluster state
4. Check MLflow tracking URI configuration
5. Validate data source accessibility
6. Report: environment status, data source info

### Stage 1: Data Loading and Profiling

1. Load data into Spark DataFrame
2. Profile dataset:
   - Row count, column count
   - Target column analysis (class distribution or value range)
   - Feature types (numeric, categorical, text, date)
   - Missing value percentages
   - Correlation matrix for numeric features
3. Determine task type: classification vs. regression
4. Framework recommendation:
   - Data > 1M rows or wide features: recommend Spark MLlib
   - Data < 1M rows: recommend sklearn with MLflow (faster iteration)
5. Report: data profile, task type, framework recommendation

### Stage 2: Feature Engineering

1. Automatic feature pipeline:
   - Numeric: `Imputer` -> `StandardScaler`
   - Categorical: `StringIndexer` -> `OneHotEncoder`
   - Date: extract temporal features
   - Text: `Tokenizer` -> `CountVectorizer` (or TF-IDF)
   - High-cardinality categorical: frequency encoding or target encoding
2. Feature selection:
   - Drop zero-variance columns
   - Drop high-correlation duplicates (>0.95)
   - Chi-squared test for categorical features (classification)
3. Assemble with `VectorAssembler`
4. Report: feature pipeline stages, selected features

### Stage 3: Model Training

1. Create MLflow experiment (or use existing)
2. Enable autologging: `mlflow.pyspark.ml.autolog()` or `mlflow.sklearn.autolog()`
3. Define candidate algorithms:
   - **Classification**: LogisticRegression, RandomForestClassifier, GBTClassifier, (sklearn: XGBoost, LightGBM)
   - **Regression**: LinearRegression, RandomForestRegressor, GBTRegressor, (sklearn: XGBoost, LightGBM)
4. For each candidate:
   - Define hyperparameter grid
   - Run CrossValidator (Spark) or cross_val_score (sklearn)
   - Log all parameters, metrics, and artifacts to MLflow
5. Best model selection based on primary metric:
   - Classification: AUC-ROC (binary) or F1-weighted (multiclass)
   - Regression: RMSE
6. Report: per-algorithm results, best model, MLflow experiment URL

### Stage 4: Model Evaluation

1. Evaluate best model on held-out test set
2. Metrics:
   - Classification: accuracy, precision, recall, F1, AUC-ROC, log-loss, confusion matrix
   - Regression: RMSE, MAE, R2, MAPE, residual analysis
3. Feature importance (if tree-based or linear)
4. SHAP values (if sklearn framework and data fits in memory)
5. Save evaluation artifacts to MLflow
6. Report: full metrics table, feature importance ranking

### Stage 5: Model Registration

1. Register best model in MLflow Model Registry:
   ```python
   mlflow.register_model(f"runs:/{best_run_id}/model", model_name)
   ```
2. Add description, tags, and input signature
3. Transition to "Staging" stage
4. If Unity Catalog enabled: register to `catalog.schema.model_<name>`
5. Report: model name, version, registry URL

### Stage 6: Report

```python
from ml_utils import save_agent_report
save_agent_report("databricks-ml-engineer", {
    "status": "completed",
    "command": "db-train",
    "task_type": task_type,
    "framework": framework,
    "best_model": {"algorithm": algo, "metrics": metrics},
    "mlflow_experiment": experiment_url,
    "registry": {"name": model_name, "version": version},
    "feature_importance": top_features,
    "recommendations": recommendations
})
```

Print: training summary, best model metrics, MLflow experiment link, next steps.
