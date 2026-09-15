# Deploying an ML Model

Deploy a classic machine learning model (scikit-learn, XGBoost, LightGBM, TensorFlow, PyTorch, ONNX, or
an MLflow model) on DKubeX. ML models are served through **KServe**, from the **ML Registry** in Model
Studio.

:::{note}
The **ML Registry** and **ML Models** pages appear only when KServe is enabled on the platform.
:::

## Prerequisites

- Access to **Model Studio** with KServe enabled.
- A model to deploy — either registered in **MLflow**, or a text-based **HuggingFace ML** model.

## Find a model

1. In Model Studio, open **ML Registry**.
2. Choose the source tab:
   - **MLflow** — your registered models and their versions/stages (None, Staging, Production,
     Archived). All MLflow flavors are supported.
   - **HuggingFace ML** — HuggingFace models filtered to ML tasks. Only **text-based pipeline tasks** are
     supported; vision, audio, tabular, and multimodal models show **Coming Soon** and cannot be
     deployed yet.

## Deploy the model

1. Select the model and open its deploy form.
2. Set:
   | Field | Set to |
   |---|---|
   | **Model Name** | Auto-filled; edit if needed. |
   | **Model Format** | `sklearn`, `xgboost`, `lightgbm`, `tensorflow`, `pytorch`, `onnx`, `mlflow`, or `huggingface`. Leave as `mlflow` to auto-detect the flavor from the model's `MLmodel` file. |
   | **Source** | `mlflow` or `huggingface`. |
   | **Replicas** | Min and Max. |
   | **CPU / Memory** | Request and Limit. |
   | **GPU** *(optional)* | Check **Request GPU**, then choose the GPU type and count (only shown when the cluster has GPU nodes). |
3. Deploy. DKubeX selects the matching KServe runtime automatically (for example `sklearn` →
   `kserve-sklearnserver`, `mlflow` → `kserve-mlserver`).
4. Open **ML Models** and wait for the model to become **Running**. It is served as a KServe
   `InferenceService`.

You can delete models you own from the **ML Models** page.

## Related

- For training a model and deploying it end to end, see the
  [MLOps tutorial](../mlops/training-and-deploying-an-ml-model-on-dkubex.md).
