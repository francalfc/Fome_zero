import pandas as pd
import streamlit as st
import plotly.express as px

#=========================================
# carregamento dos dados
#=========================================
df = pd.read_csv('data.csv')

st.set_page_config(page_title='Countrys', page_icon='🌍', layout='wide')
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
st.markdown('#  🌍 Visão Países')

with st.container():
    
    df_aux = df.loc[linhas_selecionadas, ['restaurant_id', 'country']].groupby('country').count().reset_index()

    fig = px.bar(df_aux, x='country', y='restaurant_id', text_auto='restaurant_id',
                 title='Quantidade de Restaurantes Registrados por País',
                 labels={'country': 'Países',
                         'restaurant_id': 'Qtd. Restaurantes'})
    st.plotly_chart(fig, use_container_width=True)
st.markdown('___')

with st.container():
    df_aux = (df.loc[linhas_selecionadas, ['city', 'country']].groupby('country')
                                                             .nunique()
                                                             .sort_values('city', ascending=False)
                                                             .reset_index())

    fig = px.bar(df_aux, x='country', y='city', text_auto='city',
                 title='Quantidade de Cidades Registrados por País',
                 labels={'country': 'Países',
                         'city': 'Qtd. de cidades'})
    st.plotly_chart(fig, use_container_width=True)
st.markdown('___')
    
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        df_aux = (df.loc[linhas_selecionadas, ['votes', 'country']].groupby('country')
                                                                   .mean()
                                                                   .sort_values('votes',ascending=False)
                                                                   .round(2)
                                                                   .reset_index())

        fig = px.bar(df_aux, x='country', y='votes', text_auto='.2f',
                     title='Média de Avaliações feitas por Pais',
                     labels={'country': 'Países',
                             'votes': 'Qtd. de Avaliações'})
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        df_aux = (df.loc[linhas_selecionadas, ['average_cost_for_two', 'country']].groupby('country')
                                                                                  .mean()
                                                                                  .round(2)
                                                                                  .sort_values('average_cost_for_two',ascending=False)
                                                                                  .reset_index())
                                   
        fig = px.bar(df_aux, x='country', y='average_cost_for_two',text_auto='.2f',
                    title='Média de preço de um prato para duas pessoas por país (Moeda Local)',
                     labels={'country': 'Países',
                             'average_cost_for_two': 'Média de Preço do prato para duas pessoas '})
        st.plotly_chart(fig, use_container_width=True)