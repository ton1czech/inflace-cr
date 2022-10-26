import streamlit as st
import pandas as pd

st.set_page_config(page_title="Inflace v ČR", page_icon=":chart_with_upwards_trend:")

st.title("Inflace v ČR")

data = pd.read_csv('https://raw.githubusercontent.com/ton1czech/inflace-cr-dataset/master/inflace.csv')

st.subheader("Tabulka inflace")
st.dataframe(data)

data['datum'] = data['rok'].astype(str) + '.' + data['měsíc']

st.subheader("Vývoj inflace")
st.line_chart(data, x='datum', y='procenta')