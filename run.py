import os
import streamlit.web.cli as stcli
import sys

sys.argv = ["streamlit", "run", "tabtextdiff/app.py"]
sys.exit(stcli.main())
