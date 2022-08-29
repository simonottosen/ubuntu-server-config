# simple_streamlit_app.py
"""
A simple streamlit app
"""

import numpy as np
import pandas as pd
import streamlit as st

st.title("Simple Streamlit App")

st.write("Here's our first attempt at using data to create a table:")
st.write(
    pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})
)
