import streamlit as st
import pandas as pd
import plotly_express as px

# page settings
st.set_page_config(page_title='Inflace v ČR', page_icon=':chart_with_upwards_trend:')

# sidebar
st.sidebar.title('Navigace')
options = st.sidebar.radio('Vyber vizualizaci:', [
    'Hlavní stránka', 
    'Tabulka dat', 
    'Vývoj inflace od roku 2000',
    'Roční vývoj inflace', 
    ])

# load data
df = pd.read_csv('https://raw.githubusercontent.com/ton1czech/inflace-cr-dataset/master/mesicni-inflace.csv')

# table where you can filter data by year and month
def table_filtered():
    st.subheader('Tabulka inflace')

    # append new row to use all data in column
    new_df = pd.DataFrame([['vše', 'vše', '']], columns=df.columns).append(df)

    # split layout to two columns
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox('Filtrovat rok:', new_df['rok'].unique())
    with col2:
        month = st.selectbox('Filtrovat měsíc:',  new_df['měsíc'].unique())
    
    # filter engine
    if year == 'vše' and month == 'vše':
        st.dataframe(df)
    else:
        if year == 'vše' and month:
            new_df = df.loc[(df['měsíc'] == month)]
            st.dataframe(new_df)
        elif year and month == 'vše':
            new_df = df.loc[(df['rok'] == year)]
            st.dataframe(new_df)
        else:
            new_df = df.loc[(df['rok'] == year) & (df['měsíc'] == month)]
            st.dataframe(new_df)

# simple table of inflation data
def table():
    st.subheader('Tabulka inflace')

    st.dataframe(df)

# show inflation % of each month since 2000 till now
def inflation_alltime():
    st.subheader('Vývoj inflace of roku 2000')

    df['datum'] = df['rok'].astype(str) + '.' + df['měsíc']

    fig = px.line(df, x='datum', y='procenta', labels=dict(datum='Rok a měsíc', procenta='%'))

    config = dict({'scrollZoom': True})
    fig.update_layout(
        dragmode='pan',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
        ),
    )

    st.plotly_chart(fig, config=config)

# show inflation in selected year
def inflation_by_year():
    st.subheader('Vývoj inflace (roční)')

    year = st.selectbox('Vyber rok:', df['rok'].unique())

    new_df = df.loc[df['rok'] == year]

    st.line_chart(new_df, x='měsíc', y='procenta')

# sidebar menu functionality
if options == 'Hlavní stránka':
    st.title('Inflace v ČR')

    col1, col2 = st.columns(2)
    with col1:
        table()
    with col2:
        st.markdown('Data jsou z českého statistického úřadu _(www.czso.cz/csu/czso/mira_inflace)_. Zde najdete mnou vytvořené **.csv** datasety: _www.github.com/ton1czech/inflace-cr-dataset_')
    inflation_alltime()
    inflation_by_year()
elif options == 'Tabulka dat':
    table_filtered()
elif options == 'Roční vývoj inflace':
    inflation_by_year()
elif options == 'Vývoj inflace od roku 2000':
    inflation_alltime()