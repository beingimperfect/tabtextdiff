import streamlit as st
from tabtextdiff.diff_logic import load_input, compute_diff
import pandas as pd

# Set the page config
st.set_page_config(layout="wide")
st.title("📊 TabTextDiff - Compare DataFrames")

# Create columns for horizontal layout
col1, col2 = st.columns(2)

# File upload in horizontal layout
with col1:
    df1 = load_input(
        st.file_uploader("Upload first file", type=["csv", "xlsx", "txt"], key="file1"),
        st.text_area("Or paste first table", key="text1")
    )

with col2:
    df2 = load_input(
        st.file_uploader("Upload second file", type=["csv", "xlsx", "txt"], key="file2"),
        st.text_area("Or paste second table", key="text2")
    )

# If either file is missing, show an info message
if df1 is None or df2 is None:
    st.info("Upload or paste two data inputs to compare.")
    st.stop()

# Try to compute the diff
try:
    mask, diff_summary = compute_diff(df1, df2)
except ValueError as e:
    st.error(str(e))
    st.stop()

# Function to render the diff side by side
def render_diff(df1, df2, mask):
    df_styled = pd.DataFrame(index=df1.index)
    for col in df1.columns:
        df_styled[(col, "Original")] = df1[col]
        df_styled[(col, "Modified")] = df2[col]

    def style_func(series, col_name, is_original):
        color = "#ffecec" if is_original else "#eaffea"
        return [
            f"background-color: {color}" if mask.at[idx, col_name] else ""
            for idx in series.index
        ]

    styled = df_styled.style
    for col in df1.columns:
        styled = styled.apply(
            style_func, col_name=col, is_original=True,
            subset=[(col, "Original")]
        ).apply(
            style_func, col_name=col, is_original=False,
            subset=[(col, "Modified")]
        )
    return styled

# Display the side-by-side diff
st.subheader("🔍 Side-by-side Diff View")
st.dataframe(render_diff(df1, df2, mask), height=600)

# Show a summary of differences
st.subheader("📝 Change Summary")
st.dataframe(diff_summary)

# Allow the user to download the diff summary as a CSV
st.download_button(
    "📥 Download Change Summary as CSV",
    diff_summary.to_csv(index=False).encode("utf-8"),
    file_name="df_diff_summary.csv",
    mime="text/csv"
)
