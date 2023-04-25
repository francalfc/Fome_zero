import pandas as pd
import streamlit as st
import plotly.express as px

#=========================================
# carregamento dos dados
#=========================================
df = pd.read_csv('data.csv')

st.set_page_config(page_title='Citys', page_icon='🏙️', layout='wide')
#=========================================
# Barra lateral
#=========================================

st.sidebar.markdown("___")

#Filtro multiselect
st.sidebar.header('Filtros')
country_option = st.sidebar.multiselect('Escolha os Países que deseja visualizar os Restaurantes',
                                        df.loc[:,'country']
                                        .unique()
                                        .tolist()
                                        ,default=["Brazil", "England", "South Africa", "Canada", "Australia"])

linhas_selecionadas = df['country'].isin(country_option)
df_aux = df.loc[linhas_selecionadas, :]
st.sidebar.markdown("___")

#==================================================================
st.markdown('#  🏙️ Visão Cidades')

with st.container():
    df_aux = (df.loc[linhas_selecionadas ,['city','country' ,'restaurant_id']]
                .groupby(['country','city'])
                .count()
                .sort_values(['restaurant_id', 'city'],ascending=[False,True])
                .reset_index().head(10))

    fig = px.bar(df_aux, x='city', y='restaurant_id', text_auto='restaurant_id', color='country',
                 title='Top 10 cidades com mais Restaurantes na Base de dados',
                 labels={'city': 'Cidade',
                         'restaurant_id': 'Qtd Restaurante',
                         'country': 'País'})
    st.plotly_chart(fig, use_container_width=True)
st.markdown('___')

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(' ###### Top 7 Cidade com Restaurantes com média de avaliação maior que 4.0')
        lines = (df["aggregate_rating"] > 4) & (df['country'].isin(country_option)) 
        df_aux = (df.loc[lines, ['country', 'city','restaurant_id']]
                    .groupby(['country', 'city'])
                    .count()
                    .sort_values(['restaurant_id', 'city'], ascending=[False, True])
                    .reset_index() ) 
                  
        fig = px.bar(df_aux.head(7), x='city', y='restaurant_id', text_auto='restaurant_id', color='country',
                     labels={'city': 'Cidades',
                       'restaurant_id': 'Qtd. Restaurantes',
                       'country': 'Países'})
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown(' ###### Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5')
        lines = (df["aggregate_rating"] < 2.5 ) & (df['country'].isin(country_option)) 
        df_aux = (df.loc[lines, ['country', 'city','restaurant_id']]
                    .groupby(['country', 'city'])
                    .count()
                    .sort_values(['restaurant_id', 'city'], ascending=[False, True])
                    .reset_index() ).head(7)
                  
        fig = px.bar(df_aux, x='city', y='restaurant_id', text_auto='restaurant_id', color='country',
                     labels={'city': 'Cidades',
                       'restaurant_id': 'Qtd. Restaurantes',
                       'country': 'Países'})
        st.plotly_chart(fig, use_container_width=True)

st.markdown('___')

with st.container():
    st.markdown("###### Top 10 das cidades que tem restaurantes com culinária distinta")
    df_aux = (df.loc[linhas_selecionadas, ['cuisines','country', 'city' ]]
                .groupby(['country','city'])
                .nunique()
                .sort_values(['cuisines','city'], ascending=([False,True]))
                .reset_index()).head(10)
    
    fig = px.bar(df_aux, x='city', y='cuisines', text_auto='cuisines', color='country',
                 labels={'city': 'Cidades',
                         'cuisines': 'Qtd. Tipos de culinária',
                         'country': 'Países'})
    st.plotly_chart(fig, use_container_width=True)
    