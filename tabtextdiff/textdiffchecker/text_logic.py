import difflib
from fuzzywuzzy import fuzz
from typing import List, Tuple
import pandas as pd

import html
# Simple line-by-line diff using difflib
def line_by_line_diff(text1: str, text2: str) -> List[str]:
    differ = difflib.Differ()
    diff = list(differ.compare(text1.splitlines(), text2.splitlines()))
    return diff

def render_side_by_side_diff(text1: str, text2: str) -> str:
    diff = line_by_line_diff(text1, text2)
    left_lines = []
    right_lines = []

    for line in diff:
        tag = line[:2]
        content = html.escape(line[2:])

        if tag == '  ':
            left_lines.append(content)
            right_lines.append(content)
        elif tag == '- ':
            left_lines.append(f"<span style='background-color:#ffecec'>{content}</span>")
            right_lines.append('')
        elif tag == '+ ':
            left_lines.append('')
            right_lines.append(f"<span style='background-color:#eaffea'>{content}</span>")
        elif tag == '? ':
            # Ignore or use for fine-grained highlighting later
            pass

    html_output = """
    <div style="display: flex; font-family: monospace; overflow-x: auto; border:1px solid #ccc;">
        <div style="flex: 1; padding: 0.5rem; border-right: 1px solid #ddd; background: #fdfdfd; white-space: pre; overflow: auto;">
            {}
        </div>
        <div style="flex: 1; padding: 0.5rem; background: #fdfdfd; white-space: pre; overflow: auto;">
            {}
        </div>
    </div>
    """.format('<br>'.join(left_lines), '<br>'.join(right_lines))

    return html_output

def fuzzy_line_matching(text1, text2, threshold=80):
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    max_len = max(len(lines1), len(lines2))

    result = []
    for i in range(max_len):
        line1 = lines1[i] if i < len(lines1) else ""
        line2 = lines2[i] if i < len(lines2) else ""
        score = fuzz.ratio(line1, line2)
        result.append({
            "line_no": i + 1,
            "original": line1,
            "modified": line2,
            "similarity": score
        })

    return result

def highlight_line_differences(line1, line2):
    sm = difflib.SequenceMatcher(None, line1, line2)
    l1_html = ""
    l2_html = ""

    for opcode, a0, a1, b0, b1 in sm.get_opcodes():
        if opcode == "equal":
            l1_html += line1[a0:a1]
            l2_html += line2[b0:b1]
        elif opcode == "replace":
            l1_html += f"<span style='background-color:#ffecec'>{line1[a0:a1]}</span>"
            l2_html += f"<span style='background-color:#eaffea'>{line2[b0:b1]}</span>"
        elif opcode == "delete":
            l1_html += f"<span style='background-color:#ffecec'>{line1[a0:a1]}</span>"
        elif opcode == "insert":
            l2_html += f"<span style='background-color:#eaffea'>{line2[b0:b1]}</span>"

    return l1_html, l2_html

def word_diff_dataframe(text1, text2):
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    max_len = max(len(lines1), len(lines2))

    rows = []
    for i in range(max_len):
        line1 = lines1[i] if i < len(lines1) else ""
        line2 = lines2[i] if i < len(lines2) else ""
        html1, html2 = highlight_line_differences(line1, line2)

        rows.append({
            "Line No": i + 1,
            "Original": html1,
            "Modified": html2
        })

    return pd.DataFrame(rows)