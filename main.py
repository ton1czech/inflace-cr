import streamlit as st
import pandas as pd

st.title("Inflace v ČR")

data = pd.read_csv('https://raw.githubusercontent.com/ton1czech/inflace-cr-dataset/master/inflace.csv')
data['datum'] = data['rok'].astype(str) + '.' + data['měsíc']

st.subheader('Tabulka inflace')
st.dataframe(data)

st.subheader('Vývoj inflace')
st.line_chart(data, x='datum', y='procenta')