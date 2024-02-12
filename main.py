import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import plotly_express as px
import pydeck as pdk

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: white;'>EARTHQUAKE</h1>", unsafe_allow_html=True)

df1 = pd.read_csv('clean_disaster.csv')
df2 = pd.read_csv('clean_earthquake.csv')
tab1, tab2 = st.tabs(['Dashboard 1', 'Dashboard 2'])

with tab1:
    with st.sidebar:
        st.title("MAIN DASHBOARD'S FILTERS")

# 1 - Map
    with st.container():
        st.markdown("<h4 style='text-align: center; color: white;'>Location of Earthquakes from 2000 until 2023</h4>", unsafe_allow_html=True)

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

# 2 - Correlation of Factors and Intensities of Earthquakes
    st.markdown("""---""")
    with st.container():
        st.markdown("<h4 style='text-align: center; color: white;'>Correlation of Factors and Intensities of Earthquakes</h4>", unsafe_allow_html=True)

        with st.form('First Form'):
            st.sidebar.subheader('SELECTION OF VARIABLES FOR V-2')
            x_variable = st.sidebar.selectbox('X Variable', ['cdi',
                                                            'mmi',
                                                            'depth',
                                                            'magnitude'
                                                            ])
            y_variable = st.sidebar.selectbox('Y Variable', ['cdi',
                                                            'mmi',
                                                            'depth',
                                                            'magnitude'
                                                            ])
            click2 = st.form_submit_button('Show Visualization')
            
        if click2:
            fig3 = px.scatter(df2,
                            x=x_variable,
                            y=y_variable)
            st.plotly_chart(fig3, use_container_width=True)

# 3 - 
    st.markdown("""---""")
    with st.container():
        st.markdown("<h4 style='text-align: center; color: white;'>Number of Affected People</h4>", unsafe_allow_html=True)
        col1 = st.columns(2)

        with st.form('Second Form'):
            with st.sidebar:
                st.markdown("""---""")
            st.sidebar.subheader('SELECTION OF VARIABLES FOR V-3 AND V-4')
            y_var_1 = st.sidebar.radio('Y Variable for Left Visualization', ['Number of deaths from earthquakes',
                                                                            'Number of people injured from earthquakes',
                                                                            'Number of people affected by earthquakes',
                                                                            'Number of people left homeless from earthquakes'
                                                                            ])
            y_var_2 = st.sidebar.radio('Y Variable for Right Visualization', ['Number of deaths from earthquakes',
                                                                            'Number of people injured from earthquakes',
                                                                            'Number of people affected by earthquakes',
                                                                            'Number of people left homeless from earthquakes'
                                                                            ])
            click1 = st.form_submit_button('Show Visualization')
            
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
            
            col1[0].plotly_chart(fig1, use_container_width=True)
            col1[1].plotly_chart(fig2, use_container_width=True)
    
# 4 - 
    st.markdown("""---""")
    with st.container():
        st.markdown("<h4 style='text-align: center; color: white;'>Reliability of Instruments</h4>", unsafe_allow_html=True)
        
        with st.form('Third Form'):
            with st.sidebar:
                st.markdown("""---""")
            st.sidebar.subheader('SELECTION OF VARIABLES FOR V-5')
            xVar = st.sidebar.selectbox('X Variable', ['gap',
                                                    'sig',
                                                    'dmin',
                                                    'nst'])
            yVar = st.sidebar.selectbox('Y Variable', ['gap',
                                                    'sig',
                                                    'dmin',
                                                    'nst'])
            button_4 = st.form_submit_button('Show Visualization')
            
            if button_4:
                fig3 = px.bar(df2, x=xVar, y=yVar)
                st.plotly_chart(fig3, use_container_width=True)
                
# 5 - Number of people, according to years and chosen country for comparison
    st.markdown("""---""")
    with st.container():
        st.markdown("<h4 style='text-align: center; color: white;'>Timeline of Earthquakes Throughout the Years</h4>", unsafe_allow_html=True)
        
        with st.form('Fourth Form'):
            with st.sidebar:
                st.markdown("""---""")
            st.sidebar.subheader('SELECTION OF VARIABLES FOR V-6')
            x_var = st.sidebar.selectbox('Country', df1['Entity'].unique())
            y_var = st.sidebar.radio('Variable', ['Number of deaths from earthquakes',
                                                'Number of people injured from earthquakes',
                                                'Number of people affected by earthquakes',
                                                'Number of people left homeless from earthquakes'
                                                ])
            button_5 = st.form_submit_button('Show Visualization')
            
            if button_5:
                df_vis6 = df1[df1['Entity'] == x_var]
                fig4 = px.line(df_vis6, x=df_vis6['Year'], y=y_var)
                st.plotly_chart(fig4, use_container_width=True)