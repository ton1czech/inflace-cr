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
    
    min_percentage, max_percentage = st.select_slider('Filtrovat procenta:', df['procenta'].sort_values().unique(), (df['procenta'].min(axis=0), df['procenta'].max(axis=0)))
    
    # filter engine
    if year == 'vše' and month == 'vše' and min_percentage == df['procenta'].min(axis=0) and max_percentage == df['procenta'].max(axis=0):
        st.dataframe(df)
    elif year != 'vše' and month != 'vše' and (min_percentage != df['procenta'].min(axis=0) or max_percentage != df['procenta'].max(axis=0)):
        new_df = df.loc[(df['rok'] == year) & (df['měsíc'] == month) & (df['procenta'] <= max_percentage) & (df['procenta'] >= min_percentage)]
        st.dataframe(new_df)
    elif year != 'vše' and (min_percentage != df['procenta'].min(axis=0) or max_percentage != df['procenta'].max(axis=0)):
        new_df = df.loc[(df['rok'] == year) & (df['procenta'] <= max_percentage) & (df['procenta'] >= min_percentage)]
        st.dataframe(new_df)
    elif month != 'vše' and (min_percentage != df['procenta'].min(axis=0) or max_percentage != df['procenta'].max(axis=0)):
        new_df = df.loc[(df['měsíc'] == month) & (df['procenta'] <= max_percentage) & (df['procenta'] >= min_percentage)]
        st.dataframe(new_df)
    elif year != 'vše' and month != 'vše':
        new_df = df.loc[(df['rok'] == year) & (df['měsíc'] == month)]
        st.dataframe(new_df)
    elif min_percentage != df['procenta'].min(axis=0) or max_percentage != df['procenta'].max(axis=0):
        new_df = df.loc[(df['procenta'] <= max_percentage) & (df['procenta'] >= min_percentage)]
        st.dataframe(new_df)
    elif year != 'vše':
        new_df = df.loc[(df['rok'] == year)]
        st.dataframe(new_df)
    elif month != 'vše':
        new_df = df.loc[(df['měsíc'] == month)]
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
    st.subheader('Vývoj inflace pro zvolený rok')

    year = st.selectbox('Vyber rok:', df['rok'].unique())

    new_df = df.loc[df['rok'] == year]

    fig = px.line(new_df, x='měsíc', y='procenta', labels=dict(měsíc='Měsíce', procenta='%'), markers=True)

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

# custom styles
styles = """
            <style>
                .css-1dp5vir.e8zbici1 {
                    background: linear-gradient(to right, #667eea, #764ba2);
                }
            </style>
            """
st.markdown(styles, unsafe_allow_html=True)