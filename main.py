import streamlit as st
import pandas as pd

# page settings
st.set_page_config(page_title="Inflace v ČR", page_icon=":chart_with_upwards_trend:")
st.title("Inflace v ČR")

# sidebar
st.sidebar.title("Navigace")
options = st.sidebar.radio("Vyber vizualizaci:", ['Tabulka dat', 'Roční vývoj inflace', 'Měsíční vývoj inflace'])

# load data
data_monthly = pd.read_csv('https://raw.githubusercontent.com/ton1czech/inflace-cr-dataset/master/mesicni-inflace.csv')
data_yearly = pd.read_csv('https://raw.githubusercontent.com/ton1czech/inflace-cr-dataset/master/rocni-inflace.csv')

def table():
    st.subheader("Tabulka inflace")
    st.dataframe(data_monthly)

def inflation_by_month():
    data_monthly['datum'] = data_monthly['rok'].astype(str) + '.' + data_monthly['měsíc']
    st.subheader("Vývoj inflace (měsíční)")
    st.line_chart(data_monthly, x='datum', y='procenta')

def inflation_by_year():
    st.subheader("Vývoj inflace (roční)")
    st.line_chart(data_yearly, x='rok', y='procenta')

table()
inflation_by_month()
inflation_by_year()