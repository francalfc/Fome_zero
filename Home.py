#=========================================
# Bibliotecas
#=========================================
import folium
import pandas as pd
import streamlit as st
from PIL import Image
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

#=========================================
# carregamento dos dados
#=========================================
df = pd.read_csv('data.csv')

st.set_page_config(page_title='Home', page_icon='📊', layout='wide')
#=========================================
# Barra lateral
#=========================================
image = Image.open('logo.png')
col1, col2 = st.sidebar.columns([1,5], gap='small')

#cabeçalho
col1.image(image, width=55)
col2.markdown('# Fome Zero')
st.sidebar.markdown("___")

#Filtro multiselect
country_option = st.sidebar.multiselect('Escolha os Países que deseja visualizar os Restaurantes',
                                        df.loc[:,'country']
                                        .unique()
                                        .tolist()
                                        ,default=["Brazil", "England", "South Africa", "Canada", "Australia"])

linhas_selecionadas = df['country'].isin(country_option)
df_aux = df.loc[linhas_selecionadas, :]
st.sidebar.markdown("___")
st.sidebar.markdown('### Powered by Comnunidade DS')

st.markdown('# Fome Zero!')
st.markdown('## O melhor lugar para encontrar seu mais novo Restaurante favorito!')
st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')

#=========================================
# Métricas
#=========================================
with st.container():
    restaurant, country, city, votes, cuisines = st.columns(5)
    
    with restaurant:
        st.metric('Restaurantes Cadastrados', df['restaurant_id'].nunique())
        
    with country:
        st.metric('Países Cadastrados', df['country'].nunique())
        
    with city:
        st.metric('Cidades Cadastradas', df['city'].nunique())
        
    with votes:
        st.metric('Total de avaliações', df['votes'].sum())
        
    with cuisines:
        st.metric('Tipos de Culinárias', df['cuisines'].nunique())
st.markdown("___")

#=========================================
# Mapa
#=========================================
with st.container():
    figure = folium.Figure(width=1920, height=1080)
    map = folium.Map(max_bounds=True).add_to(figure)
    marker_cluster = MarkerCluster().add_to(map)
    
    
    for _, line in df_aux.iterrows():
        
        
        color = f'{line["color_name"]}'
    
        folium.Marker( [line['latitude'], line['longitude']],
                        popup=line[['city','restaurant_id']],
                        icon=folium.Icon(color=color, icon='home', prefix='fa')).add_to(marker_cluster)
        
    folium_static(map, width=1024, height=768)