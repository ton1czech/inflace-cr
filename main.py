from re import MULTILINE
import streamlit as st
import pandas as pd

# page settings
st.set_page_config(page_title="Inflace v ČR", page_icon=":chart_with_upwards_trend:")
st.title("Inflace v ČR")

# sidebar
st.sidebar.title("Navigace")
options = st.sidebar.radio("Vyber vizualizaci:", [
    'Hlavní stránka', 
    'Tabulka dat', 
    'Roční vývoj inflace', 
    'Měsíční vývoj inflace'
    ])

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

if options == 'Hlavní stránka':
    col1, col2 = st.columns(2)
    with col1:
        table()
    with col2:
        st.markdown("Data jsou z českého statistického úřadu _(www.czso.cz/csu/czso/mira_inflace)_. Zde najdete mnou vytvořené **.csv** datasety: _www.github.com/ton1czech/inflace-cr-dataset_")
    inflation_by_month()
    inflation_by_year()
elif options == 'Tabulka dat':
    table()
elif options == 'Roční vývoj inflace':
    inflation_by_year()
elif options == 'Měsíční vývoj inflace':
    inflation_by_month()