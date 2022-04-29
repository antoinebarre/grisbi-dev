"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import grisbi

grisbi.get_data_from_Yahoo("GE")
df = grisbi.load_data_from_csv("GE")



st.write("Here's our first attempt at using data to create a table:")
st.write(df)