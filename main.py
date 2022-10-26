import streamlit as st
import pandas as pd
import numpy as np

st.title("Inflace v ČR")

data = pd.read_csv('https://raw.githubusercontent.com/ton1czech/inflace-cr-dataset/master/inflace.csv', index_col='rok')

st.subheader('Tabulka inflace')
st.write(data)