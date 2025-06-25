import pandas as pd
import numpy as np
from io import StringIO
import difflib

# Load input from file or text area
def load_input(file, text):
    if file:
        name = file.name.lower()
        if name.endswith(".csv"):
            return pd.read_csv(file)
        elif name.endswith(".xlsx"):
            return pd.read_excel(file)
        elif name.endswith(".txt"):
            return pd.read_csv(file, sep=None, engine="python")  # In case it's CSV in a .txt file
    elif text.strip():
        return pd.read_csv(StringIO(text), sep=None, engine="python")
    return None

# Compare two DataFrames
def compute_diff(df1, df2):
    if df1.shape != df2.shape or list(df1.columns) != list(df2.columns):
        raise ValueError("DataFrames must have the same shape and columns")

    df1.index = df2.index  # Align index

    mask = ~df1.fillna("NaN").eq(df2.fillna("NaN"))

    diff_summary = pd.DataFrame([
        {
            "index": df1.index[i],
            "column": df1.columns[j],
            "original": df1.iat[i, j],
            "modified": df2.iat[i, j]
        }
        for i, j in zip(*np.where(mask.values))
    ])

    return mask, diff_summary

# Function to compare plain text
def compare_text(text1, text2):
    differ = difflib.Differ()
    diff = differ.compare(text1.splitlines(), text2.splitlines())
    return '\n'.join(diff)
