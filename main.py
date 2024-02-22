import streamlit as st
import pandas as pd
import plotly_express as px
import pydeck as pdk

# Setting the configuration of the screen layout
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Title of the application
st.markdown("<h1 style='text-align: center; color: white;'>EARTHQUAKE</h1>", unsafe_allow_html=True)

# Naming the dataframes of datasets
df1 = pd.read_csv('clean_disaster.csv')
df2 = pd.read_csv('clean_earthquake.csv')

# Putting dashboards into 2 sections or tabs
tab1, tab2 = st.tabs(['Main Dashboard', 'Second Dashboard'])


with tab1:
# 1 - Map
    with st.container():
        st.markdown("<h4 style='text-align: center; color: white;'>V-1 : Location of Earthquakes from 2000 until 2023</h4>", unsafe_allow_html=True)
        col = st.columns(2)

        # Filters
        with col[0]:
            layer_color_red = st.slider('Red of RGB for Scatter Points', 0, 255, 100)
            layer_color_green = st.slider('Green of RGB for Scatter Points', 0, 255, 100)
            layer_color_blue = st.slider('Blue of RGB for Scatter Points', 0, 255, 100)
        
        with col[1]:
            view_pitch = st.slider('Pitch of Map', 0, 180, 0)
            layer_opacity = st.slider('Scatter Points Opacity', 0.0, 1.0, 0.5)
            chart_style = st.selectbox('Map Style', ['Dark',
                                                    'Light',
                                                    'Satellite',
                                                    'Outdoors'])
        
        # Map Chart Style
        if chart_style == 'Dark':
            chart_style = 'mapbox://styles/mapbox/dark-v11'
        elif chart_style == 'Light':
            chart_style = 'mapbox://styles/mapbox/light-v11'
        elif chart_style == 'Satellite':
            chart_style = 'mapbox://styles/mapbox/satellite-v9'
        elif chart_style == 'Outdoors':
            chart_style = 'mapbox://styles/mapbox/outdoors-v12'
        
        view = pdk.ViewState(
            latitude=8.4,
            longitude=11.7,
            zoom=1,
            pitch=view_pitch,
            height = 500,
            width = 1350
        )

        layer = pdk.Layer(
            'ScatterplotLayer',
            data = df2,
            get_position = ['longitude', 'latitude'],
            radius = 90,
            extruded = True,
            opacity = layer_opacity,
            radius_min_pixels = 5,
            radius_max_pixels = 100,
            getFillColor = [layer_color_red, layer_color_green, layer_color_blue]
        )

        st.pydeck_chart(pdk.Deck(
            map_style=chart_style,
            initial_view_state=view,
            layers=layer
        ))

# 2 - Correlation of Factors and Intensities of Earthquakes
    st.markdown("""---""")
    with st.container():
        st.markdown("<h4 style='text-align: center; color: white;'>V-2 : Correlation of Factors and Intensities of Earthquakes</h4>", unsafe_allow_html=True)

        fig1 = px.scatter(df2,
                            x = 'magnitude',
                            y = 'depth',
                            color = 'magnitude')
        st.plotly_chart(fig1, use_container_width=True)
        

# 3 & 4 - Number of Affected People
    st.markdown("""---""")
    with st.container():
        st.markdown("<h4 style='text-align: center; color: white;'>V-3&4 : Number of Affected People</h4>", unsafe_allow_html=True)
        
        selected_variable = st.radio('Y Variable for Left Visualization', ['Number of people injured from earthquakes',
                                                                        'Number of people affected by earthquakes',
                                                                        'Number of people left homeless from earthquakes'
                                                                        ])
        
        col1 = st.columns(2)
        df_compared_entity = pd.DataFrame(df1.groupby(['Entity'])['Number of deaths from earthquakes'].sum())
        df_compared_entity = df_compared_entity.sort_values(['Number of deaths from earthquakes'], ascending=False)
        df_compared_entity = df_compared_entity.iloc[:10]
        fig1 = px.bar(df_compared_entity, y='Number of deaths from earthquakes', color='Number of deaths from earthquakes')
        
        df_selected_entity = pd.DataFrame(df1.groupby(['Entity'])[selected_variable].sum())
        df_selected_entity = df_selected_entity.sort_values([selected_variable], ascending=False)
        df_selected_entity = df_selected_entity.iloc[:10]
        fig2 = px.bar(df_selected_entity, y=selected_variable, color=selected_variable)

        with col1[0]:
            st.plotly_chart(fig1, use_container_width=True)
        with col1[1]:
            st.plotly_chart(fig2, use_container_width=True)

    
# 5 - Reliability of Instruments
    st.markdown("""---""")
    with st.container():
        st.markdown("<h4 style='text-align: center; color: white;'>V-5 : Reliability of Instruments</h4>", unsafe_allow_html=True)
        
        selected_indication = st.selectbox('Y Variable', ['gap',
                                                            'dmin',
                                                            'nst',
                                                            'alert',
                                                            'mmi'
                                                            ])
            
        fig3 = px.scatter(df2, x='sig', y=selected_indication)
        st.plotly_chart(fig3, use_container_width=True)
                
# 6&7 - Number of people, according to years and chosen country for comparison
    st.markdown("""---""")
    with st.container():
        st.markdown("<h4 style='text-align: center; color: white;'>V-6&7 : Comparison of Each Entity's Earthquake Timeline</h4>", unsafe_allow_html=True)
        col2 = st.columns(2)
        
        with st.form('Fourth Form'):
            x_var1 = st.selectbox('First Entity', df1['Entity'].unique())
            x_var2 = st.selectbox('Second Entity', df1['Entity'].unique())
            y_var = st.radio('Variable', ['Number of deaths from earthquakes',
                                                'Number of people injured from earthquakes',
                                                'Number of people affected by earthquakes',
                                                'Number of people left homeless from earthquakes'
                                                ])
            button_5 = st.form_submit_button('Show Visualization')
            
            if button_5:
                df_vis6a = df1[df1['Entity'] == x_var1]
                df_vis6b = df1[df1['Entity'] == x_var2]
                fig4 = px.line(df_vis6a, x=df_vis6a['Year'], y=y_var)
                fig5 = px.line(df_vis6b, x=df_vis6b['Year'], y=y_var)
                
                col2[0].plotly_chart(fig4, use_container_width=True)
                col2[1].plotly_chart(fig5, use_container_width=True)





# Second Dashboard                
with tab2:
    with st.sidebar:
        st.title("SECOND DASHBOARD'S FILTERS")
        st.markdown("""---""")
        with st.expander('V-8 : Selection of Variables'):
                entities = st.selectbox('Choice of Entity', df1['Entity'].unique())
                choice = st.radio('Select One', ['Total number of people affected by earthquakes per 100,000',
                                                        'Total economic damages from earthquakes'])    

    with st.container():
        col3 = st.columns(2)   
        
        
# 8 - Grouped Bar Chart    
        with col3[0]:
            st.markdown("<h4 style='text-align: center; color: white;'>V-8 : Average Magnitude For Each Alert Level</h4>", unsafe_allow_html=True)
        fig6 = px.histogram(df2,
                      x='tsunami',
                      y='magnitude',
                      histfunc='avg',
                      color='alert',
                      barmode='group')
        col3[0].plotly_chart(fig6)
        
# 9 - Pie Chart for each country depending on economic damages or number of affected people
        with col3[1]:
            st.markdown("<h4 style='text-align: center; color: white;'>V-9 : Each Country's Damages or Number of Affected People</h4>", unsafe_allow_html=True)
        
        colors = ['CadetBlue', 'BurlyWood', 'DarkBlue', 'DarkMagenta', 'DarkRed', 'DarkSlateBlue']
        df_vis7 = df1[df1['Entity'] == entities]
        fig7 = px.pie(df_vis7,
                      values = choice,
                      names = 'Year',
                      color = 'Year')
        fig7.update_traces(marker=dict(colors=colors))
        col3[1].plotly_chart(fig7)
    
# 10 - Bar Graph for magtype
    with st.container():
        col4 = st.columns(2)
        
    with col4[0]:
        st.markdown("<h4 style='text-align: center; color: white;'>V-10 : Calculation of Magnitude Using Methods</h4>", unsafe_allow_html=True)
    
    fig8 = px.bar(df2,
                  x = 'magType',
                  color='magType')
    col4[0].plotly_chart(fig8)
    
# 11 - 
    with col4[1]:
        st.markdown("<h4 style='text-align: center; color: white;'>V-11 : Test</h4>", unsafe_allow_html=True)
        
# 12 -
    with st.container():
        st.markdown("<h4 style='text-align: center; color: white;'>V-12 : Tests</h4>", unsafe_allow_html=True)