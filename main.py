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
        st.markdown("<h4 style='text-align: center; color: white;'>V-1 : Location of Earthquakes from 2001 until 2023</h4>", unsafe_allow_html=True)
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

        mag_slider = st.slider('Magnitude of Earthquake', 6.5, 9.0, 6.5, step=0.1)
        if mag_slider:
            df_magnitude = df2[df2['magnitude'] <= mag_slider]
        fig1 = px.scatter(df_magnitude,
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
                                                            'mmi'
                                                            ])
        
        fig3 = px.scatter(df2, x='sig',
                          y=selected_indication, 
                          color = 'alert',
                          color_discrete_map={
                              'unknown' : 'blue',
                              'green' : 'green',
                              'yellow' : 'yellow',
                              'orange' : 'orange',
                              'red' : 'red'
                          })
        st.plotly_chart(fig3, use_container_width=True)
                
# 6&7 - Number of people, according to years and chosen country for comparison
    st.markdown("""---""")
    with st.container():
        st.markdown("<h4 style='text-align: center; color: white;'>V-6&7 : Comparison of Each Entity's Earthquake Timeline</h4>", unsafe_allow_html=True)
        
        x_var1 = st.selectbox('First Entity', df1['Entity'].unique())
        x_var2 = st.selectbox('Second Entity', df1['Entity'].unique())
        x_var3 = st.selectbox('Third Entity', df1['Entity'].unique())
        x_var4 = st.selectbox('Fourth Entity', df1['Entity'].unique())
        y_var = st.radio('Variable', ['Number of deaths from earthquakes',
                                            'Number of people injured from earthquakes',
                                            'Number of people affected by earthquakes',
                                            'Number of people left homeless from earthquakes'
                                            ])
        
        df_first_entity = df1[df1['Entity']==x_var1]
        df_second_entity = df1[df1['Entity']==x_var2]
        df_third_entity = df1[df1['Entity']==x_var3]
        df_fourth_entity = df1[df1['Entity']==x_var4]
        combined_df = [df_first_entity, df_second_entity, df_third_entity, df_fourth_entity]
        result_df = pd.concat(combined_df)
        fig5 = px.line(result_df,
                       x='Year',
                       y=y_var,
                       color = 'Entity',
                       color_discrete_map={
                           x_var1 : 'blue',
                           x_var2 : 'red',
                           x_var3 : 'green',
                           x_var4 : 'yellow'
                       })
        st.plotly_chart(fig5, use_container_width=True)
        








# Second Dashboard                
with tab2:
    with st.sidebar:
        st.title("SECOND DASHBOARD'S FILTERS")
        st.markdown("""---""")
        
        with st.expander('V-8 : Selection of Variables'):
            selected_function = st.radio('Select histogram function', ['Count',
                                                                       'Sum',
                                                                       'Average',
                                                                       'Minimum',
                                                                       'Maximum'])
            if selected_function == 'Count':
                selected_function = 'count'
            elif selected_function == 'Sum':
                selected_function = 'sum'
            elif selected_function == 'Average':
                selected_function = 'avg'
            elif selected_function == 'Minimum':
                selected_function = 'min'
            elif selected_function == 'Maximum':
                selected_function = 'max'
            
                
        with st.expander('V-9 : Selection of Variables'):
            entities = st.selectbox('Choice of Entity', df1['Entity'].unique())
            choice = st.radio('Select One', ['Total number of people affected by earthquakes per 100,000',
                                                    'Total economic damages from earthquakes'])
        
        with st.expander('V-10 : Magnitude Type'):
            selected_variable = st.radio('Select Y variable', ['cdi',
                                                                'mmi',
                                                                'sig'])
            
        with st.expander('V-11 : Selection of Year'):
            selected_year = st.select_slider('Year', [1960,
                                                      1970,
                                                      1980,
                                                      1990,
                                                      2000,
                                                      2010])
                
        with st.expander('V-12 : Selection of Tsunami Occurence'):
            selected_tsunami = st.selectbox('Occurence of Tsunami', ['Tsunami',
                                                                     'No Tsunami'])
            if selected_tsunami == 'Tsunami':
                selected_tsunami = df2[df2['tsunami']==1]
            elif selected_tsunami == 'No Tsunami':
                selected_tsunami = df2[df2['tsunami']==0]
                

# 8 - Grouped Bar Chart                
    with st.container():
        col3 = st.columns(2)   
        
        with col3[0]:
            st.markdown("<h4 style='text-align: center; color: white;'>V-8 : Occurence of Tsunami Depending on Magnitude and Alert Level</h4>", unsafe_allow_html=True)
        fig6 = px.histogram(df2,
                      x='tsunami',
                      y='magnitude',
                      histfunc=selected_function,
                      color='alert',
                      barmode='group')
        col3[0].plotly_chart(fig6)

        
# 9 - Pie Chart for each country depending on economic damages or number of affected people
        with col3[1]:
            st.markdown("<h4 style='text-align: center; color: white;'>V-9 : Each Entity's Damages or Number of Affected People</h4>", unsafe_allow_html=True)
        
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
            st.markdown("<h4 style='text-align: center; color: white;'>V-10 : Total Number of Earthquakes According to Timeline</h4>", unsafe_allow_html=True)
    
        fig8 = px.bar(df2,
                    x = 'magType',
                    y = selected_variable,
                    color='alert')
        col4[0].plotly_chart(fig8)

    
# 11 - Bubble chart
    with col4[1]:
        st.markdown("<h4 style='text-align: center; color: white;'>V-11 : Injury and Death Rates</h4>", unsafe_allow_html=True)
        
        fig9 = px.scatter(df1[df1['Year']==selected_year],
                          x = 'Death rates from earthquakes',
                          y = 'Injury rates from earthquakes',
                          size = 'Total number of people affected by earthquakes per 100,000',
                          color = 'Entity',
                          log_x=True,
                          size_max=50)
        col4[1].plotly_chart(fig9)

        
# 12 - Recorded Tsunamis in the World
    with st.container():
        st.markdown("<h4 style='text-align: center; color: white;'>V-12 : Recorded Tsunamis in the World</h4>", unsafe_allow_html=True)
    
    map_view = pdk.ViewState(
        latitude=8.4,
        longitude=11.7,
        zoom=1,
        pitch=0,
        height = 500,
        width = 1350
    )

    map_layer = pdk.Layer(
        'ScatterplotLayer',
        data = selected_tsunami,
        get_position = ['longitude', 'latitude'],
        radius = 90,
        extruded = True,
        opacity = 0.8,
        radius_min_pixels = 5,
        radius_max_pixels = 100,
        getFillColor = [29, 174, 93]
    )

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v11',
        initial_view_state=map_view,
        layers=map_layer
    ))