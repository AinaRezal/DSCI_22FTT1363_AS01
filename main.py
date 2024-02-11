import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import plotly_express as px
import pydeck as pdk

st.set_page_config(layout="wide")
st.title('Earthquake')

df1 = pd.read_csv('clean_disaster.csv')
df2 = pd.read_csv('clean_earthquake.csv')
bar = st.sidebar

# First Visualization - Map
st.subheader('Location of Earthquakes from 2000 until 2023')

view = pdk.ViewState(
    latitude=8.4,
    longitude=11.7,
    zoom=1,
    pitch=0,
    height = 500,
    width = 1350
)

layer = pdk.Layer(
    'ScatterplotLayer',
    data = df2,
    get_position = ['longitude', 'latitude'],
    radius = 90,
    extruded = True,
    opacity = 0.5,
    radius_min_pixels = 5,
    radius_max_pixels = 100,
    getFillColor = [255, 68, 51]
)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v11',
    initial_view_state=view,
    layers=layer
))

# Second and Third Visualization - Bar Chart regarding number of people
st.markdown("""---""")
st.subheader('Number of Affected People')
st.caption('< Refer to sidebar to choose two different variables for comparisons')
col1 = st.columns(2)

with st.form('First Form'):
    st.sidebar.text('> 2ND AND 3RD VISUALIZATION')
    y_var_1 = st.sidebar.selectbox('Y Variable for Visualization 1', ['Number of deaths from earthquakes',
                                                                    'Number of people injured from earthquakes',
                                                                    'Number of people affected by earthquakes',
                                                                    'Number of people left homeless from earthquakes'
                                                                    ])
    y_var_2 = st.sidebar.selectbox('Y Variable for Visualization 2', ['Number of deaths from earthquakes',
                                                                    'Number of people injured from earthquakes',
                                                                    'Number of people affected by earthquakes',
                                                                    'Number of people left homeless from earthquakes'
                                                                    ])
    click1 = st.form_submit_button('Show Vis 2 and 3')
    st.markdown("""---""")
    
if click1:
    df_1 = pd.DataFrame(df1.groupby(['Entity'])[y_var_1].sum())
    df_1 = df_1.sort_values([y_var_1], ascending=False)
    df_1 = df_1.iloc[:10]
    fig1 = px.bar(df_1,
                    y=y_var_1)
    
    df_2 = pd.DataFrame(df1.groupby(['Entity'])[y_var_2].sum())
    df_2 = df_2.sort_values([y_var_2], ascending=False)
    df_2 = df_2.iloc[:10]
    fig2 = px.bar(df_2,
                    y=y_var_2)
    
    col1[0].plotly_chart(fig1)
    col1[1].plotly_chart(fig2)
    
# Fourth Visualization - cdi and mmi
st.markdown("""---""")
st.subheader('Correlation of intensities and tsunamis by earthquake')

with st.form('Second Form'):
    st.sidebar.text('> 4TH VISUALIZATION')
    x_variable = st.sidebar.selectbox('X Variable', ['cdi',
                                                     'mmi'
                                                     ])
    y_variable = st.sidebar.selectbox('Y Variable', ['cdi',
                                                     'mmi'
                                                     ])
    click2 = st.form_submit_button('Show Vis 4')
    st.markdown("""---""")
    
if click2:
    fig3 = px.scatter(df2,
                      x=x_variable,
                      y=y_variable)
    st.plotly_chart(fig3)