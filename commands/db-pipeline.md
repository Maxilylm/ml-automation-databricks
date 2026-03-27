# /db-pipeline

Build a Spark data transformation pipeline. Generates a modular, testable ETL/ELT pipeline with Delta Lake integration.

## Usage

```
/db-pipeline <source> --target <delta_table> [--schedule <cron>] [--dlt] [--streaming]
```

- `source`: input data source (Delta table, DBFS path, SQL query, JDBC connection)
- `--target`: output Delta table name (catalog.schema.table)
- `--schedule`: cron expression for scheduled execution
- `--dlt`: generate Delta Live Tables pipeline instead of standard ETL
- `--streaming`: generate Structured Streaming pipeline

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` — if missing, copy from core plugin
2. Check if `databricks_utils.py` exists in `src/` — if missing, copy from this plugin's `templates/databricks_utils.py`
3. Verify Databricks connection
4. Validate source exists and is accessible
5. Report: source schema, row count estimate, target table status

### Stage 1: Source Analysis

1. Read source schema and sample data (first 1000 rows)
2. Profile data:
   - Column types and null percentages
   - Cardinality of categorical columns
   - Value distributions for numeric columns
   - Date range for temporal columns
3. Detect data quality issues:
   - Duplicate rows
   - Inconsistent formats (dates, phone numbers, etc.)
   - Outliers in numeric columns
4. Report: source profile summary

### Stage 2: Transformation Design

1. Based on source analysis, generate transformation logic:
   - Schema standardization (column renaming, type casting)
   - Null handling (impute, drop, flag)
   - Deduplication strategy
   - Data quality filters
   - Derived columns (calculations, lookups, enrichments)
   - Partition column selection
2. If `--dlt`: define pipeline as Delta Live Tables:
   ```python
   import dlt

   @dlt.table(comment="Bronze: raw ingestion")
   def bronze_table():
       return spark.read.format("delta").table(source)

   @dlt.table(comment="Silver: cleaned and enriched")
   @dlt.expect_or_drop("valid_id", "id IS NOT NULL")
   def silver_table():
       return dlt.read("bronze_table").transform(...)

   @dlt.table(comment="Gold: aggregated for analytics")
   def gold_table():
       return dlt.read("silver_table").groupBy(...).agg(...)
   ```
3. If `--streaming`: generate Structured Streaming:
   ```python
   df = spark.readStream.format("delta").table(source)
   # ... transformations ...
   df.writeStream.format("delta").outputMode("append") \
     .option("checkpointLocation", checkpoint_path) \
     .toTable(target)
   ```

### Stage 3: Pipeline Generation

1. Generate modular pipeline code:
   - `src/pipelines/<name>/extract.py` — source reading
   - `src/pipelines/<name>/transform.py` — transformation logic
   - `src/pipelines/<name>/load.py` — Delta table writing
   - `src/pipelines/<name>/pipeline.py` — orchestrator
   - `src/pipelines/<name>/config.py` — pipeline configuration
2. Generate tests:
   - `tests/test_<name>_transform.py` — unit tests for transformations
   - `tests/test_<name>_pipeline.py` — integration test
3. Generate pipeline configuration:
   ```json
   {
     "name": "<pipeline_name>",
     "source": "<source>",
     "target": "<target>",
     "mode": "batch|streaming|dlt",
     "partition_by": ["<column>"],
     "schedule": "<cron>",
     "merge_key": ["<column>"],
     "quality_checks": [...]
   }
   ```

### Stage 4: Scheduling (if --schedule)

1. Generate Databricks job definition:
   - Task: run pipeline notebook or script
   - Trigger: cron schedule
   - Cluster: job cluster (auto-terminated)
   - Retries: 2 attempts with 5-minute delay
   - Alerts: email on failure
2. Print job creation instructions (or create via API if connected)

### Stage 5: Report

```python
from ml_utils import save_agent_report
save_agent_report("databricks-engineer", {
    "status": "completed",
    "command": "db-pipeline",
    "source": source,
    "target": target,
    "mode": mode,
    "generated_files": generated_files,
    "transformations": transformation_summary,
    "quality_checks": quality_checks,
    "schedule": schedule
})
```

Print: pipeline architecture, generated files, transformation summary, scheduling details.
