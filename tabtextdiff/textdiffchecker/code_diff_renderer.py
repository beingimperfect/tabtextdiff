# """
# code_diff_renderer.py

# A module to compare Python code semantically using tokenization.
# Highlights changes in functionally relevant tokens, ignoring whitespace and formatting.
# """

# import tokenize
# from io import StringIO
# from difflib import SequenceMatcher
# import keyword

# def tokenize_python_code(code):
#     """
#     Tokenize Python code into a list of (type, string) tokens, skipping whitespace and comments.
#     """
#     tokens = []
#     try:
#         for tok in tokenize.generate_tokens(StringIO(code).readline):
#             tok_type, tok_string = tok.type, tok.string
#             if tok_type in [tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE, tokenize.NL]:
#                 continue  # Skip formatting tokens
#             if tok_type == tokenize.COMMENT:
#                 continue  # Skip comments
#             tokens.append((tokenize.tok_name[tok_type], tok_string))
#     except tokenize.TokenError:
#         pass
#     return tokens

# def compare_token_lists(tokens1, tokens2):
#     """
#     Compare two lists of tokens and return a list of differences with minimal formatting.
#     """
#     matcher = SequenceMatcher(None, tokens1, tokens2)
#     diffs = []

#     for tag, i1, i2, j1, j2 in matcher.get_opcodes():
#         if tag == 'equal':
#             for tok in tokens1[i1:i2]:
#                 diffs.append((" ", tok))
#         elif tag == 'replace':
#             for tok in tokens1[i1:i2]:
#                 diffs.append(("-", tok))
#             for tok in tokens2[j1:j2]:
#                 diffs.append(("+", tok))
#         elif tag == 'delete':
#             for tok in tokens1[i1:i2]:
#                 diffs.append(("-", tok))
#         elif tag == 'insert':
#             for tok in tokens2[j1:j2]:
#                 diffs.append(("+", tok))

#     return diffs

# def format_token_diff(diffs):
#     """
#     Format the token diff result into readable HTML.
#     """
#     html = "<div style='font-family:monospace; white-space:pre-wrap'>"
#     for tag, (tok_type, tok_string) in diffs:
#         style = ""
#         if tag == "-":
#             style = "background-color:#ffecec;"
#         elif tag == "+":
#             style = "background-color:#eaffea;"
#         elif tok_type == "NAME" and keyword.iskeyword(tok_string):
#             style = "font-weight:bold; color:#008;"
#         html += f"<span style='{style}'>{tok_string}</span>"
#         if tok_type == "STRING" or tok_type == "NUMBER":
#             html += " "
#     html += "</div>"
#     return html

# def render_code_diff(code1, code2):
#     """
#     Entry function to get diff view of two Python code blocks.
#     Returns HTML with highlights.
#     """
#     tokens1 = tokenize_python_code(code1)
#     tokens2 = tokenize_python_code(code2)
#     diffs = compare_token_lists(tokens1, tokens2)
#     return format_token_diff(diffs)

# # Example usage in Streamlit:
# # import streamlit as st
# # from code_diff_renderer import render_code_diff
# # html = render_code_diff(code1_text, code2_text)
# # st.markdown(html, unsafe_allow_html=True)

#####################################################################################33

# import difflib
# import tokenize
# import io
# from html import escape


# def tokenize_python_code(code):
#     tokens = []
#     for tok in tokenize.generate_tokens(io.StringIO(code).readline):
#         tokens.append(tok.string)
#     return tokens


# def highlight_diff_tokens(a_tokens, b_tokens):
#     matcher = difflib.SequenceMatcher(None, a_tokens, b_tokens)
#     a_result = []
#     b_result = []

#     for op, a1, a2, b1, b2 in matcher.get_opcodes():
#         if op == 'equal':
#             a_result.extend([escape(tok) for tok in a_tokens[a1:a2]])
#             b_result.extend([escape(tok) for tok in b_tokens[b1:b2]])
#         elif op in ('replace', 'delete'):
#             a_result.extend([f"<span style='background-color:#ffd6d6'>{escape(tok)}</span>" for tok in a_tokens[a1:a2]])
#         else:
#             a_result.extend([escape(tok) for tok in a_tokens[a1:a2]])

#         if op in ('replace', 'insert'):
#             b_result.extend([f"<span style='background-color:#d6f5d6'>{escape(tok)}</span>" for tok in b_tokens[b1:b2]])
#         else:
#             b_result.extend([escape(tok) for tok in b_tokens[b1:b2]])

#     return ' '.join(a_result), ' '.join(b_result)


# def render_code_diff(code_a, code_b):
#     a_tokens = tokenize_python_code(code_a)
#     b_tokens = tokenize_python_code(code_b)

#     highlighted_a, highlighted_b = highlight_diff_tokens(a_tokens, b_tokens)

#     html = f"""
#     <div style="display:flex; gap:20px; font-family:monospace">
#         <div style="width:50%; background:#f7f7f7; padding:10px;">{highlighted_a}</div>
#         <div style="width:50%; background:#f7f7f7; padding:10px;">{highlighted_b}</div>
#     </div>
#     """
#     return html


##############################################################

from difflib import SequenceMatcher
import html

def render_code_diff(code1, code2):
    """
    Compare code1 and code2 line-by-line.
    Returns HTML with highlighted differences while preserving full spacing and formatting.
    """
    code1_lines = code1.splitlines()
    code2_lines = code2.splitlines()

    max_lines = max(len(code1_lines), len(code2_lines))
    html_lines = ["<div style='display: flex; font-family: monospace; overflow-x: auto;'>"]
    html_line1 = ["<div style='flex: 1; padding: 4px; border-right: 1px solid #ccc; background:#f8f8f8;'>"]
    html_line2 = ["<div style='flex: 1; padding: 4px;'>"]

    for i in range(max_lines):
        line1 = code1_lines[i] if i < len(code1_lines) else ""
        line2 = code2_lines[i] if i < len(code2_lines) else ""

        highlighted1 = _highlight_line_diff(line1, line2, "-")
        highlighted2 = _highlight_line_diff(line2, line1, "+")

        html_line1.append(f"<pre style='margin:0'>{highlighted1}</pre>")
        html_line2.append(f"<pre style='margin:0'>{highlighted2}</pre>")

    html_line1.append("</div>")
    html_line2.append("</div>")

    html_line1 = "\n".join(html_line1)
    html_line2 = "\n".join(html_line2)

    html_lines.append(html_line1)
    html_lines.append(html_line2)

    html_lines.append("</div>")
    return "\n".join(html_lines)

def _highlight_line_diff(line1, line2, tag):
    """
    Highlight character-level differences between line1 and line2.
    `tag` is '-' (left/original) or '+' (right/modified) to control color.
    """
    matcher = SequenceMatcher(None, line1, line2)
    result = ""
    for op, i1, i2, _, _ in matcher.get_opcodes():
        part = html.escape(line1[i1:i2])
        if op == 'equal':
            result += part
        else:
            color = "#ffecec" if tag == "-" else "#eaffea"
            result += f"<span style='background-color:{color}'>{part}</span>"
    return result
