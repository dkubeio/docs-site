import os
import pandas as pd
from snowflake import connector
from snowflake.connector.pandas_tools import write_pandas
from sklearn import preprocessing as skpreprocessing
# ---------------------------------
# Locate insurance.csv
# ---------------------------------
conn = connector.connect()
cur = conn.cursor()
print("Connected to Snowflake")
cur.execute("SELECT * FROM INSURANCEDATA")
df_version1 = cur.fetch_pandas_all()
print("Version data loaded")

cur.execute("SELECT * FROM INSURANCEDATA LIMIT 1")
row = cur.fetchone()
print(row)

# ---------------------------------
# Load data
# ---------------------------------
for col in ['SEX', 'SMOKER', 'REGION']:
    if df_version1[col].dtype == 'object' or df_version1[col].dtype == 'bool':
        if df_version1[col].dtype == 'bool':
            df_version1[col] = df_version1[col].astype(int)
        else:
            le = skpreprocessing.LabelEncoder()
            df_version1[col] = le.fit_transform(df_version1[col])
        print(f"Completed Label Encoding on {col}")

resultant_table_name = os.getenv("OUT_TABLE_NAME","PREPROCESSED_DATA")
# ---------------------------------
# Save preprocessed CSV
# ---------------------------------
success, nchunks, nrows, _ = write_pandas(
    conn,
    df_version1,
    table_name=f'{resultant_table_name}',       # just the table name
    auto_create_table=True,
    overwrite=True
)
print(f"Temporary table created, success={success}, rows={nrows}")
conn.commit()  
cur.close()
conn.close()
print("Done")
