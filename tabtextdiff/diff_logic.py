import pandas as pd
import numpy as np
from io import StringIO
import difflib


def load_input(file, text, mode="tabular"):
    from io import StringIO
    import pandas as pd

    if mode == "tabular":
        if file:
            name = file.name.lower()
            if name.endswith(".csv"):
                return pd.read_csv(file)
            elif name.endswith(".xlsx"):
                return pd.read_excel(file)
            elif name.endswith(".txt"):
                return pd.read_csv(file, sep=None, engine="python")
        elif text.strip():
            return pd.read_csv(StringIO(text), sep=None, engine="python")
    elif mode == "text":
        if file:
            return file.read().decode("utf-8")
        elif text.strip():
            return text.strip()

    return None


# Compare two DataFrames
def compute_diff(df1, df2, selected_columns=None):
    if selected_columns:
        df1 = df1[selected_columns]
        df2 = df2[selected_columns]

    if df1.shape != df2.shape or list(df1.columns) != list(df2.columns):
        raise ValueError("DataFrames must have the same shape and columns")

    # Dtype verification
    for col in df1.columns:
        if df1[col].dtype != df2[col].dtype:
            raise ValueError(f"Column '{col}' has mismatched dtypes: {df1[col].dtype} vs {df2[col].dtype}")

    df1.index = df2.index
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
