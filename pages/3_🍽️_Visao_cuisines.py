import pandas as pd
import streamlit as st
import plotly.express as px

#=========================================
# carregamento dos dados
#=========================================
df = pd.read_csv('data.csv')

st.set_page_config(page_title='Cuisines', page_icon='🍽️', layout='wide')
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

qtd_restaurant = st.sidebar.slider ('Selecione a quantidade de Restaurantes que deseja visualizar', 1, 20, 10)
st.sidebar.markdown('___')

cuisines_option = st.sidebar.multiselect('Escolha os tipos de culinária', df.loc[:, 'cuisines'].unique().tolist(),
                                         default=['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'American'])


#==================================================================
cuisines = {"Italian": "", "American": "", "Arabian": "", "Japanese": "", "Brazilian": ""}
cols = ["restaurant_id", "restaurant_name", "country", "city", "cuisines", "average_cost_for_two", "currency",
    "aggregate_rating",
    "votes"]
for key in cuisines.keys():
    lines = df["cuisines"] == key    
    cuisines[key] = (
        df.loc[lines, cols]
        .sort_values(["aggregate_rating", "restaurant_id"], ascending=[False, True])
        .iloc[0, :]
        .to_dict() )
#cuisines

st.markdown('#  🍽️ Visão tipos de Culinárias')
st.markdown('##  Melhores Restaurantes do principais tipos Culinários')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label=f'Italiana: {cuisines["Italian"]["restaurant_name"]}',
            value=f'{cuisines["Italian"]["aggregate_rating"]}/5.0',
            help=f"""
            País: {cuisines["Italian"]['country']}\n
            Cidade: {cuisines["Italian"]['city']}\n
            Média Prato para dois: {cuisines["Italian"]['average_cost_for_two']} ({cuisines["Italian"]['currency']})
            """,)
    with col2:
        st.metric(
            label=f'Americana: {cuisines["American"]["restaurant_name"]}',
            value=f'{cuisines["American"]["aggregate_rating"]}/5.0',
            help=f"""
            País: {cuisines["American"]['country']}\n
            Cidade: {cuisines["American"]['city']}\n
            Média Prato para dois: {cuisines["American"]['average_cost_for_two']} ({cuisines["American"]['currency']})
            """ )
    with col3:
        st.metric(
            label=f'Árabe: {cuisines["Arabian"]["restaurant_name"]}',
            value=f'{cuisines["Arabian"]["aggregate_rating"]}/5.0',
            help=f"""
            País: {cuisines["Arabian"]['country']}\n
            Cidade: {cuisines["Arabian"]['city']}\n
            Média Prato para dois: {cuisines["Arabian"]['average_cost_for_two']} ({cuisines["Arabian"]['currency']})
            """,
        )
    with col4:
        st.metric(
            label=f'Japonesa: {cuisines["Japanese"]["restaurant_name"]}',
            value=f'{cuisines["Japanese"]["aggregate_rating"]}/5.0',
            help=f"""
            País: {cuisines["Japanese"]['country']}\n
            Cidade: {cuisines["Japanese"]['city']}\n
            Média Prato para dois: {cuisines["Japanese"]['average_cost_for_two']} ({cuisines["Japanese"]['currency']})
            """,
        )
    with col5:
         st.metric(
            label=f'Brasileira: {cuisines["Brazilian"]["restaurant_name"]}',
            value=f'{cuisines["Brazilian"]["aggregate_rating"]}/5.0',
            help=f"""
            País: {cuisines["Brazilian"]['country']}\n
            Cidade: {cuisines["Brazilian"]['city']}\n
            Média Prato para dois: {cuisines["Brazilian"]['average_cost_for_two']} ({cuisines["Brazilian"]['currency']})
            """,
        )
    
st.markdown('___')

with st.container():
    st.markdown(f'## Top {qtd_restaurant} Restaurantes')
    lines = (df['cuisines'].isin(cuisines_option)) & (df['country'].isin(country_option))
    cols = ['restaurant_id', 'restaurant_name', 'country', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'votes']
    df_top = df.loc[lines, cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).reset_index(drop=True)
    st.dataframe(df_top.head(qtd_restaurant))
st.markdown('___')
    
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown (f'###### Top {qtd_restaurant} tipos de culinárias')
        
        lines = df['country'].isin(country_option)
        df_best = (df.loc[lines, ['aggregate_rating', 'cuisines']].groupby('cuisines')
                                                                  .mean().sort_values('aggregate_rating', ascending=False).head(qtd_restaurant).reset_index())
        
        fig = px.bar(df_best, x='cuisines', y='aggregate_rating', text_auto='.2f',
                     labels={'cuisines' : 'Tipo de culinária',
                             'aggregate_rating' : 'Média das avaliações'} )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown(f'###### Top {qtd_restaurant} tipos de culinárias')
        line = df['country'].isin(country_option)
        
        df_worst = (df.loc[line, ['aggregate_rating', 'cuisines']]
                     .groupby('cuisines')
                     .mean().sort_values('aggregate_rating', ascending=True)
                     .reset_index().head(qtd_restaurant))
        
        fig = px.bar(df_worst.head(qtd_restaurant),  x='cuisines', y='aggregate_rating', text_auto='.2f',
                     labels={'cuisines' : 'Tipo de culinária',
                             'aggregate_rating' : 'Média das avaliações'})
        
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.dataframe(df)
