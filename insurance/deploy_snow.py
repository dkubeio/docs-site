import os
import pandas as pd
import mlflow
from ray import serve
from fastapi import Request

@serve.deployment
class InsuranceDeployment:
    def __init__(self):
        model_path = os.getenv("MODEL_PATH")
        if not model_path:
            raise ValueError("MODEL_PATH environment variable is missing")

        print(f"Loading MLflow sklearn model from: {model_path}")
        self.model = mlflow.sklearn.load_model(model_path)
        print("Model loaded successfully!")

    async def __call__(self, request: Request):
        try:
            body = await request.json()

            # Extract data properly
            raw_data = body["data"]

            # Convert to DataFrame
            input_df = pd.DataFrame(raw_data)

            # Ensure column names match training exactly
            input_df.columns = [
                "AGE", "SEX", "BMI", "CHILDREN", "SMOKER", "REGION"
            ]

            predictions = self.model.predict(input_df)

            return {
                "predictions": predictions.tolist()
            }

        except Exception as e:
            print("Prediction error:", repr(e))
            return {"error": str(e)}

app = InsuranceDeployment.bind()
