# Workflows

End-to-end walkthroughs for the common MLflow tasks on DKubeX.

## Track a training run

```python
import mlflow

mlflow.set_tracking_uri("http://mlflow.dkubex-apps.svc.cluster.local")
mlflow.set_experiment("churn-model")

with mlflow.start_run(run_name="rf-baseline"):
    mlflow.log_param("n_estimators", 200)
    mlflow.log_param("max_depth", 8)
    # ... train ...
    mlflow.log_metric("auc", 0.87)
    mlflow.sklearn.log_model(model, artifact_path="model")
```

Open the MLflow UI → your `churn-model` experiment → the `rf-baseline` run shows the
params, the AUC metric, and the logged model under Artifacts.

## Register and version a model

1. Open the run, go to **Artifacts**, select the logged `model`.
2. Click **Register Model** → give it a name (e.g. `churn-rf`), or add a version to an
   existing name.
3. Or register from code:
   ```python
   mlflow.register_model("runs:/<run_id>/model", "churn-rf")
   ```

## Promote a version

In **Models → churn-rf**, move the best version to **Staging**, then **Production** (or set
an alias like `@champion`). Downstream consumers reference the stage/alias, so promoting a
new version swaps what they load without code changes.

## Deploy the registered model

Switch to [ModelStudio](../modelstudio/index.md) → ML models → pick `churn-rf` from the
MLflow registry → deploy. ModelStudio serves it via KServe and shows its status; test it
from the Playground.

## Compare runs to pick the best

Select several runs in an experiment and click **Compare** — MLflow lays out their params
and metrics together (and plots metric curves) so you can choose which version to register
and promote.
