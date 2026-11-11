# Getting started

This guide gets you into MLflow and logging your first run in a few minutes.

## Open MLflow

From the DKubeX application catalog, install **MLflow**, then open it. The MLflow UI is
served at `/mlflow` behind DKubeX single sign-on — you'll pass the platform login first,
then land on the MLflow experiments view.

## Point your code at the tracking server

Set the tracking URI to the in-cluster MLflow endpoint before you log anything. From code
running inside the cluster (e.g. a workspace or a job):

```python
import mlflow

mlflow.set_tracking_uri("http://mlflow.dkubex-apps.svc.cluster.local")  # in-cluster
mlflow.set_experiment("my-first-experiment")
```

From outside the cluster, use the gateway URL instead (`https://<platform-host>/mlflow`),
which requires your DKubeX credentials.

## Log your first run

```python
with mlflow.start_run():
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("rmse", 0.31)
    mlflow.log_artifact("model.pkl")
```

Refresh the MLflow UI — your experiment and run appear immediately, with the parameter,
metric, and the stored artifact.

## Where things are stored

- **Tracking store** (runs, params, metrics, tags): the platform-managed database.
- **Artifacts** (models, files, plots): the platform's MinIO bucket.

Both are provisioned for you at install time — no separate setup required.
