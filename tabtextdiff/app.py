import streamlit as st
from tabtextdiff.diff_logic import load_input, compute_diff
import pandas as pd
from tabtextdiff.textdiffchecker.text_logic import line_by_line_diff, fuzzy_line_matching, word_diff_dataframe, render_side_by_side_diff
from tabtextdiff.textdiffchecker.text_utils import read_text_file
from tabtextdiff.textdiffchecker.code_diff_renderer import render_code_diff

# Set the page config
st.set_page_config(layout="wide")
st.title("📊 TabTextDiff - Compare DataFrames")

if "comparison_mode" not in st.session_state:
    st.session_state.comparison_mode = "Tabular"

def on_mode_change():
    # Reset inputs on mode change
    st.session_state.text1 = ""
    st.session_state.text2 = ""


# comparison_mode = st.radio(
#     "Choose Comparison Mode",
#     ["Tabular", "Plain Text"],
#     index=0,
#     key="comparison_mode",
#     on_change=on_mode_change,
#     horizontal=True
# )
 
comparison_mode = st.radio(
    "Choose Comparison Mode",
    ["Tabular", "Plain Text"],
    index=0,
    horizontal=True,
    key="comparison_mode_selector"
)

# File upload in horizontal layout
mode_key = "tabular" if st.session_state.comparison_mode == "Tabular" else "text"

# if mode_key != st.session_state.comparison_mode:
#     st.session_state.comparison_mode = mode_key
#     st.experimental_rerun()

if st.session_state.comparison_mode == "Tabular":
    allowed_types = ["csv", "xlsx", "txt"]
    placeholder = "Paste CSV/Excel-like tabular data here..."
    input_mode = "tabular"
else:
    allowed_types = ["txt"]
    placeholder = "Paste plain text content here..."
    input_mode = "text"


col1, col2 = st.columns(2)

# Use completely separate UI blocks per mode
if comparison_mode == "Tabular":
    with col1:
        input1 = load_input(
            st.file_uploader("Upload first file", type=["csv", "xlsx", "txt"], key="file1_tabular"),
            st.text_area("Or paste first table", key="text1_tabular"),
            mode="tabular"
        )
    with col2:
        input2 = load_input(
            st.file_uploader("Upload second file", type=["csv", "xlsx", "txt"], key="file2_tabular"),
            st.text_area("Or paste second table", key="text2_tabular"),
            mode="tabular"
        )
elif comparison_mode == "Plain Text":
    with col1:
        input1 = load_input(
            st.file_uploader("Upload first file", type=["txt"], key="file1_text"),
            st.text_area("Or paste first text", key="text1_text"),
            mode="text"
        )
    with col2:
        input2 = load_input(
            st.file_uploader("Upload second file", type=["txt"], key="file2_text"),
            st.text_area("Or paste second text", key="text2_text"),
            mode="text"
        )

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

try:
    if input1 is None or input2 is None:
        st.info("Please provide two inputs to compare.")
        st.stop()

    if comparison_mode.lower() == "tabular":
        mask, diff_summary = compute_diff(input1, input2)
        st.subheader("🔍 Side-by-side Diff View")
        st.dataframe(render_diff(input1, input2, mask), height=600)
        st.subheader("📝 Change Summary")
        st.dataframe(diff_summary)
        st.download_button(
            "📥 Download Change Summary as CSV",
            diff_summary.to_csv(index=False).encode("utf-8"),
            file_name="df_diff_summary.csv",
            mime="text/csv"
        )
    else:
        st.subheader("🔍 Line-by-Line Text Diff")

        # diff = line_by_line_diff(input1, input2)
        # st.code("\n".join(diff), language="diff")
        # threshold = 80

        # matches = fuzzy_line_matching(input1, input2, threshold=threshold)
    
        # st.subheader("🔍 Side-by-Side Fuzzy Line Comparison")

        # # Convert to DataFrame for display
        # df_diff = pd.DataFrame(matches)

        # def highlight_diff(row):
        #     score = row["similarity"]
        #     if score == 100:
        #         return ["background-color: #eaffea"] * 4  # green for perfect match
        #     elif score >= threshold:
        #         return ["background-color: #fff8e1"] * 4  # yellow for fuzzy match
        #     else:
        #         return ["background-color: #ffecec"] * 4  # red for low match

        # st.dataframe(df_diff.style.apply(highlight_diff, axis=1), height=600)

        # df = word_diff_dataframe(input1, input2)

        # st.markdown("### 🧠 Word-Level Diff (Highlighted)")

        # for _, row in df.iterrows():
        #     st.markdown(f"""
        #     <div style="display: flex; flex-direction: row; justify-content: space-between; border-bottom: 1px solid #ccc; padding: 4px 0;">
        #         <div style="width: 48%; font-family: monospace;">{row['Original']}</div>
        #         <div style="width: 48%; font-family: monospace;">{row['Modified']}</div>
        #     </div>
        #     """, unsafe_allow_html=True)
        # diff_html = render_code_diff(input1, input2)

        # print(diff_html)

        # st.markdown(diff_html, unsafe_allow_html=True)

        diff_html = render_side_by_side_diff(input1, input2)
        # st.code("\n".join(diff), language="diff")
        st.markdown(diff_html, unsafe_allow_html=True)



except ValueError as e:
    st.error(str(e))
    st.stop()





# try:
#     # Determine mode: text or DataFrame
#     if isinstance(df1, pd.DataFrame) and isinstance(df2, pd.DataFrame):
#         # proceed with tabular comparison
#         mask, diff_summary = compute_diff(df1, df2)
#         # Display the side-by-side diff
#         st.subheader("🔍 Side-by-side Diff View")
#         st.dataframe(render_diff(df1, df2, mask), height=600)

#         # Show a summary of differences
#         st.subheader("📝 Change Summary")
#         st.dataframe(diff_summary)

#         # Allow the user to download the diff summary as a CSV
#         st.download_button(
#             "📥 Download Change Summary as CSV",
#             diff_summary.to_csv(index=False).encode("utf-8"),
#             file_name="df_diff_summary.csv",
#             mime="text/csv"
#         )
#     elif isinstance(df1, str) and isinstance(df2, str):
#         # proceed with text diff
#         diff_result = line_by_line_diff(df1, df2)
#         st.code("\n".join(diff_result), language="diff")
#     else:
#         st.error("Both inputs must be either tabular data or plain text.")
#         st.stop()
# except ValueError as e:
#     st.error(str(e))
#     st.stop()
