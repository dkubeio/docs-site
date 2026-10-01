# Training and Deploying an ML Model on DKubeX

This tutorial walks through the end-to-end machine learning workflow on DKubeX:
training a model from the **Terminal**, tracking and registering it in **MLflow**, and
deploying and testing it in **Model Studio**.

The example predicts insurance charges. The model takes six inputs — age, sex, BMI,
number of children, smoker status, and region — and predicts the insurance charges
(premium) for a policyholder.

Only three DKubeX applications are used in this tutorial: **Terminal**, **MLflow**, and
**Model Studio**.

## Prerequisites

- Access to a DKubeX workspace with the **Terminal**, **MLflow**, and **Model Studio**
  applications enabled.
- An MLflow tracking token. In a DKubeX workspace this is supplied automatically as a file
  (see [Step 2](#step-2-configure-the-environment-variables)).

## The Example

The dataset predicts a policyholder's insurance `charges` from six features. The categorical
columns are already integer-encoded in `pre_processed.csv`, so no preprocessing step is needed
before training.

| Feature | Type | Encoding |
| --- | --- | --- |
| `age` | numeric | — |
| `sex` | categorical | `0` = female, `1` = male |
| `bmi` | numeric | — |
| `children` | numeric | — |
| `smoker` | categorical | `0` = no, `1` = yes |
| `region` | categorical | `0` = southwest, `1` = southeast, `2` = northwest, `3` = northeast |
| `charges` | numeric | target (predicted value) |

## Step 1 — Get the example and set up the environment

Open the **Terminal** application in your workspace. You start in your home directory with a
prompt similar to `admin@workspace-0:~$`.

Clone the example from the `ml-training-example` branch of the `docs-site` repository. This
gives you an `insurance/` folder containing the training script and the dataset:

```bash
git clone --branch ml-training-example --single-branch https://github.com/dkubeio/docs-site.git
```

Create and activate a Python virtual environment:

```bash
uv venv myenv --python 3.11
source myenv/bin/activate
```

Creating the environment reports the Python version and location, for example:

```
Using CPython 3.11.15
Creating virtual environment at: myenv
Activate with: source myenv/bin/activate
```

Once activated, the prompt is prefixed with the environment name, for example
`(myenv) admin@workspace-0:~$`.

Move into the example directory and list its contents:

```bash
cd docs-site/insurance
ls
```

```
deploy.py       deploy_snow.py         pre_processed.csv  predict.sh
preprocess.py   preprocessing_snow.py  train.py           training_snow.py
```

This tutorial uses two of these files: `train.py` (the training script) and
`pre_processed.csv` (the already-encoded dataset).

Install the packages required to run the training script:

```bash
uv pip install mlflow==2.22.4 scikit-learn
```

MLflow is pinned to `2.22.4` for compatibility with the tracking server.

## Step 2 — Configure the environment variables

`train.py` reads three environment variables. Export them before running the script:

```bash
export EXPERIMENT_NAME=ins_demo_exp
export REGISTERED_MODEL_NAME=ins_model
export MLFLOW_TRACKING_TOKEN=$(cat $MLFLOW_TOKEN_PATH)
```

- `EXPERIMENT_NAME` — the MLflow experiment to log to. A run is created under this experiment.
- `REGISTERED_MODEL_NAME` — the name the trained model is registered under in the MLflow Model
  Registry. Each training run adds a new version to this model.
- `MLFLOW_TRACKING_TOKEN` — authenticates the script to MLflow. In a DKubeX workspace the token
  is provided as a file, and its path is available in the `MLFLOW_TOKEN_PATH` environment
  variable. The command above reads that file and sets the token. You can confirm the path with:

  ```bash
  echo $MLFLOW_TOKEN_PATH
  ```

  ```
  /mnt/secrets/mlflow/token
  ```

## Step 3 — Train the model

Run the training script:

```bash
python train.py
```

The script loads the dataset, creates the MLflow experiment, trains the model, logs the metrics
and the model artifact to MLflow, and registers a new model version. Sample output:

```
Loading: ./pre_processed.csv
Creating MLflow experiment: ins_demo_exp
Training started...
R2  : 0.823
MAE : 2726.50
...
Successfully registered model 'ins_model'.
Created version '1' of model 'ins_model'.
...
Model logged successfully
Registered model: ins_model
Training finished: {'r2': 0.8231588285889231, 'mae': 2726.5047352665533}
```

The two evaluation metrics reported are:

- `R2` — the coefficient of determination (higher is better).
- `MAE` — the mean absolute error, in the same units as `charges`.

The model is registered automatically as version `1` of `ins_model`. Running the script again
creates the next version.

## Step 4 — Inspect the run in MLflow

Open the **MLflow** application.

- On the **Experiments** tab, select the `ins_demo_exp` experiment. The training run appears in
  the run list (with a generated run name, for example `overjoyed-jay-387`). Open the run to view
  its parameters, the logged metrics (`r2`, `mae`), and the logged model under **Artifacts**.
- On the **Models** tab, under **Registered Models**, open `ins_model`. The **Versions** section
  lists **Version 1**, which was registered by the training run.

## Step 5 — Deploy the model in Model Studio

Open the **Model Studio** application.

1. In the top navigation bar, go to **ML Registry**.
2. Locate `ins_model` and expand it to see its versions.
3. Click **Deploy** on **Version 1**.
4. In the **Deploy ML Model** dialog (which deploys a model from the MLflow registry via KServe),
   review the fields:
   - **Storage URI** — auto-filled from the selected version (for example,
     `mlflow-artifacts:/3/<run-id>`).
   - **Model Format** — `mlflow`. Auto-detect reads the model to choose the serving runtime
     (an scikit-learn model is served with the sklearn runtime).
   - **Resources** — the available cluster capacity is shown. Accept the defaults, or set CPU and
     memory if you need more.
5. Click **Deploy**.

## Step 6 — Confirm the deployment

In the top navigation bar, go to **ML Models**. The new deployment
`ins_model-v1` appears in the list. Wait until its status is **Ready** with **1/1 replicas**.

## Step 7 — Run inference

In the top navigation bar, go to **Playground**.

1. In the **Model** panel, select the deployed model — `[ML Infer] ins_model-v1` (shown as
   **Running**, served via **kserve**).
2. In **Inference Input (JSON)**, provide one or more records in KServe format. Each record is the
   six features in order: `[age, sex, bmi, children, smoker, region]`.

   ```json
   {
     "instances": [
       [19, 0, 27.9, 0, 1, 0]
     ]
   }
   ```

3. Click **Run Inference**. The **Response** panel shows the predicted charges:

   ```json
   {
     "predictions": [
       19516.150064927057
     ]
   }
   ```

The prediction is the estimated insurance charge for the supplied inputs — in this example, a
19-year-old female (`sex=0`) with a BMI of 27.9, no children, who is a smoker (`smoker=1`), in the
southwest region (`region=0`).
