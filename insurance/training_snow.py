import os
import time
import ray
import pandas as pd
import mlflow
import mlflow.sklearn

from ray import get_runtime_context
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.ensemble import HistGradientBoostingRegressor
from snowflake import connector
from snowflake.connector.pandas_tools import write_pandas


# -------------------------------------------------
# Ray task
# -------------------------------------------------
@ray.remote
def train_and_log_model():
    # -----------------------------
    # Config
    ## connecting with Snowflake
    conn = connector.connect()
    cur = conn.cursor()
    print("Connected to Snowflake")
    table_name = os.getenv("SNOWFLAKE_TABLE", "PREPROCESSED_DATA")
    MLFLOW_EXPERIMENT_NAME = os.getenv("PROJECT_NAME", "Default")
    USER = os.getenv("USER", "unknown")
    cur.execute(f"SELECT * FROM {table_name}")
    data = cur.fetch_pandas_all()
    print("Version data loaded")
    MAX_ITER = int(os.getenv("EPOCHS", 100))
    LEARNING_RATE = float(os.getenv("LEARNING_RATE", 0.05))
    # -----------------------------
    # MLflow experiment
    # -----------------------------
    if MLFLOW_EXPERIMENT_NAME:
        exp = mlflow.get_experiment_by_name(MLFLOW_EXPERIMENT_NAME)
        if not exp:
            print("Creating MLflow experiment:", MLFLOW_EXPERIMENT_NAME)
            mlflow.create_experiment(MLFLOW_EXPERIMENT_NAME)
        mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
    else:
        mlflow.set_experiment("Default")

    # -----------------------------
    # Features / target
    # -----------------------------
    X = data.drop("CHARGES", axis=1)
    y = data["CHARGES"]

    # -----------------------------
    # Train / test split
    # -----------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=1211
    )

    # -----------------------------
    # Ray runtime metadata
    # -----------------------------
    runtime_ctx = get_runtime_context()
    job_id = runtime_ctx.get_job_id()
    cluster = os.environ.get("HOSTNAME", "raycluster").split("-")[0]

    print("cluster:", cluster)
    print("job_id :", job_id)

    tags = {
        "experiment_name": MLFLOW_EXPERIMENT_NAME,
        "job_id": job_id,
        "ray cluster": cluster
    }

    # -----------------------------
    # Model
    # -----------------------------
    model = HistGradientBoostingRegressor(
        max_depth=6,
        learning_rate=LEARNING_RATE,
        max_iter=MAX_ITER,
        random_state=1211
    )

    # -----------------------------
    # Train + log to MLflow
    # -----------------------------
    start_time = time.time()

    with mlflow.start_run():
        mlflow.set_tags(tags)

        mlflow.log_params({
            "max_depth": 6,
            "learning_rate": LEARNING_RATE,
            "max_iter": MAX_ITER
        })

        print("Training started...")
        model.fit(X_train, y_train)

        # Evaluation
        preds = model.predict(X_test)
        r2 = r2_score(y_test, preds)
        mae = mean_absolute_error(y_test, preds)

        print("Evaluation results")
        print(f"R2  : {r2:.3f}")
        print(f"MAE : {mae:.2f}")

        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric(
            "training_time_sec",
            time.time() - start_time
        )

        # Log model
        mlflow.sklearn.log_model(
            model,
            artifact_path="model"
        )

    print("Model logged successfully")
    print("Go to MLflow UI → Run → Artifacts → model")

    return {"r2": r2, "mae": mae}


ray.init(address="auto")

result_ref = train_and_log_model.remote()
result = ray.get(result_ref)

print("Training finished:", result)
