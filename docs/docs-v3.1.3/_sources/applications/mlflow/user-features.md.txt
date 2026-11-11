# Core features

The MLflow UI is organized around experiments, runs, models, and artifacts.

## Experiments

An **experiment** groups related runs (e.g. all attempts at one model). Create experiments
from code (`mlflow.set_experiment("name")`) or the UI, and browse them from the left nav.

## Runs

Each **run** is one execution of your training code. For every run MLflow captures:

- **Parameters** — inputs you logged (`log_param`), e.g. hyperparameters.
- **Metrics** — numeric results (`log_metric`), optionally over steps so you get curves.
- **Tags** — arbitrary key/values for organization and search.
- **Artifacts** — files you logged (`log_artifact` / `log_model`): the model, plots, data.

Select multiple runs and **Compare** to see params/metrics side by side and pick the best.

## Models (registry)

Promote a good run's model into the **Model Registry**:

- **Register** a model to give it a name and a first version.
- **Version** it — each re-register creates a new version under the same name.
- **Stage / alias** versions (Staging, Production, Archived, or custom aliases) to mark
  which one downstream systems should use.

## Artifacts

Artifacts (the model files, plots, and any files you logged) are stored in the platform's
MinIO bucket and are downloadable from the run's **Artifacts** tab. Logged models include
their flavor metadata so they can be served later.

## Deploying registered models

Models in the registry can be deployed from [ModelStudio](../modelstudio/index.md): pick a
registered ML model and ModelStudio serves it via KServe — no manual packaging.
