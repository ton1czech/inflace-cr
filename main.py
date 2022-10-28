import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# page settings
st.set_page_config(page_title='Inflace v ČR', page_icon=':chart_with_upwards_trend:', layout='wide')

# plotly config
px_cfg = {'scrollZoom': True}

# plotly options for charts
px_optios = {
    'dragmode': 'pan',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'xaxis': {
        'showgrid': False
    },
    'yaxis': {
        'showgrid': False,
        'zeroline': False
    }
}

# sidebar navigation
with st.sidebar:
    options = option_menu(
        menu_title=None,
        options=[
            'Hlavní stránka', 
            'Tabulka dat', 
            'Vývoj inflace od roku 2000',
            'Roční vývoj inflace', 
            'Inflace/Průměrná mzda'
        ],
        icons=[
            'house',
            'file-spreadsheet',
            'graph-up',
            'graph-up',
            'arrow-down-up'
        ],
        styles={
            "nav-link": {
                "font-size": "13px"
            }
        }
    )

# load data
df = pd.read_csv('https://raw.githubusercontent.com/ton1czech/inflace-cr-dataset/master/mesicni-inflace.csv')
rocni_df = pd.read_csv('https://raw.githubusercontent.com/ton1czech/inflace-cr-dataset/master/rocni-inflace.csv')
prumerna_mzda_df = pd.read_csv('https://raw.githubusercontent.com/ton1czech/prumerna-mzda-cr-dataset/master/prumerna-mzda.csv')

# home page
def home():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('''
            #### Projekt jsem vytvořil za účelem zjištění informací o inflaci v České republice, jelikož v poslední době stoupá velice rychlým tempem.  
            #### Dále jsem se chtěl naučit používat technologie sloužící právě k datové vizualizaci.  
            #### Pro zobrazení dalších vizualizací zvolte jednu z možností v postranní nabídce.
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown('''
            Všechna data jsou získána z ČSÚ  
            _(www.czso.cz/csu/czso/mira_inflace)_.  
            <br>
            Zde najdete mnou vytvořené **.csv** datasety:  
            _www.github.com/ton1czech/inflace-cr-dataset_  
            _www.github.com/ton1czech/prumerna-mzda-cr-dataset_
        ''', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        inflation_alltime()
    with col2:
        table()
    
    
# table where you can filter data by year and month
def table_filtered():
    # append new row to use all data in column
    new_df = pd.DataFrame([['vše', 'vše', '']], columns=df.columns).append(df)

    # split layout into two columns
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
    st.dataframe(df)

# show inflation % of each month since 2000 till now
def inflation_alltime(show_header=True):
    new_df = df.copy()
    new_df['datum'] = new_df['rok'].astype(str) + '.' + new_df['měsíc']

    fig = px.line(
        new_df, 
        x='datum', 
        y='procenta', 
        title='Vývoj inflace od roku 2000' if show_header else None, 
        labels={
            'datum': 'Rok a měsíc', 
            'procenta': '%'
        }
    )

    fig.update_layout(
        px_optios
    )

    st.plotly_chart(fig, config=px_cfg, use_container_width=True)

# show inflation in selected year
def inflation_by_year():
    year = st.select_slider('Vyber rok:', df['rok'].unique(), df['rok'].max(axis=0))

    new_df = df.loc[df['rok'] == year]

    fig = px.line(
        new_df, 
        x='měsíc', 
        y='procenta', 
        labels={
            'měsíc': 'Měsíce', 
            'procenta': '%'
        },
        markers=True
    )

    fig.update_layout(
        px_optios
    )

    st.plotly_chart(fig, config=px_cfg, use_container_width=True)

# continuity between inflation and median salary
def inflation_median_salary():
    trace1 = go.Bar(
        x=rocni_df['rok'],
        y=rocni_df['procenta'],
        name='míra inflace (%)',
    )

    trace2 = go.Line(
        x=prumerna_mzda_df['rok'],
        y=prumerna_mzda_df['částka'],
        name='průměrná mzda (Kč)',
        line={'width': 5},
        yaxis='y2'
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(trace1)
    fig.add_trace(trace2, secondary_y=True)

    fig.update_layout(
        px_optios
    )
    fig.for_each_xaxis(lambda x: x.update(showgrid=False))
    fig.for_each_yaxis(lambda x: x.update(showgrid=False))
    fig['layout']['xaxis']['title']='Rok'
    fig['layout']['yaxis']['title']='%'
    fig['layout']['yaxis2']['title']='Kč'

    st.plotly_chart(fig, config=px_cfg, use_container_width=True)

# sidebar menu functionality
match options:
    case 'Hlavní stránka':
        st.title('Inflace v ČR')
        home()
    case 'Tabulka dat':
        st.title('Tabulka inflace')
        table_filtered()
    case 'Vývoj inflace od roku 2000':
        st.title('Vývoj inflace od roku 2000')
        inflation_alltime(show_header=False)
    case 'Roční vývoj inflace':
        st.title('Vývoj inflace pro zvolený rok')
        inflation_by_year()
    case 'Inflace/Průměrná mzda':
        st.title('Spojitost mezi inflací a minimální mzdou')
        inflation_median_salary()

# custom styles
with open('./styles/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)