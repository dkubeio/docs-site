import os
import pandas as pd

# ---------------------------------
# Locate insurance.csv
# ---------------------------------
MAIN_DIR = os.getenv("DATASET_PATH", "/mnt/input")
csv_path = None

for root, _, files in os.walk(MAIN_DIR):
    if "insurance.csv" in files:
        csv_path = os.path.join(root, "insurance.csv")
        break

if csv_path is None:
    raise FileNotFoundError("insurance.csv not found in the given DATASET_PATH")

print(f"Found dataset: {csv_path}")

# ---------------------------------
# Load data
# ---------------------------------
data = pd.read_csv(csv_path)

# ---------------------------------
# Explicit integer encoding
# ---------------------------------
SEX_MAP = {"female": 0, "male": 1}
SMOKER_MAP = {"no": 0, "yes": 1}
REGION_MAP = {
    "southwest": 0,
    "southeast": 1,
    "northwest": 2,
    "northeast": 3
}

data["sex"] = data["sex"].map(SEX_MAP)
data["smoker"] = data["smoker"].map(SMOKER_MAP)
data["region"] = data["region"].map(REGION_MAP)

# ---------------------------------
# Safety checks
# ---------------------------------
if data[["sex", "smoker", "region"]].isna().any().any():
    raise ValueError("Encoding failed: unseen category found")

# ---------------------------------
# Save preprocessed CSV
# ---------------------------------
output_path = os.path.join(MAIN_DIR, "pre_processed.csv")
data.to_csv(output_path, index=False)

print("Preprocessing completed successfully")
print(f"Output saved at: {output_path}")
print("Final columns:", data.columns.tolist())
