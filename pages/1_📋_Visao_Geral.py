#Import Libraries
from haversine import haversine
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from folium import Popup

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import folium as fl
import numpy as np
import inflection

st.set_page_config(page_title = 'Visao Geral', page_icon = '📋', layout = 'wide')

#===========================================================================================#
#                                        Dicionários                                        #
#===========================================================================================#
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

#===========================================================================================#
#                                       Funções                                             #
#===========================================================================================#

def restaurant_map(df):
    """Função que cria um mapa informando a posição exata de cada um dos restaurantes.

       Input: Dataframe
       Output: None(Implict: Map)
    """
    df = df.sort_values(by='restaurant_id')
    df_aux = (df.loc[:, ["restaurant_name", "address","color", "latitude", "longitude","average_cost_for_two","currency","cuisines","aggregate_rating"]])
    df = df.sort_values(by='restaurant_id')
    df = df.drop_duplicates(subset=['latitude','longitude','restaurant_name'], keep='first')
    map = fl.Map()
    marker_cluster = MarkerCluster().add_to(map)
    for index,dfit in df_aux.iterrows():
        titulo = dfit["restaurant_name"]
        texto_preco = 'Price: {:.2f}({}) para dois'.format(dfit["average_cost_for_two"], dfit["currency"])
        texto_tipo = 'Cuisine type:' + dfit["cuisines"]
        texto_rate = 'Aggregation rate: {}/5.0'.format(dfit["aggregate_rating"])
        popup_html = f'<div><b>{titulo}</b></div><br>{texto_preco}<br>{texto_tipo}<br>{texto_rate}'
        fl.Marker([dfit["latitude"],
                   dfit["longitude"]],
                   popup = Popup(popup_html, max_width=10000),
                   icon=fl.Icon(color=dfit["color"], icon="glyphicon-home")).add_to(marker_cluster)
    folium_static(map,width = 1024,height=600)
    return 

def country_name(country_id):
    """ Função que liga o número ao seu respectivo país(valor) no dicionário countries.

        Input: int
        Output: String
    """
    return COUNTRIES[country_id]

def color_name(color_code):
    """ Função que liga o hexadedimal à sua respectiva cor(valor) no dicionário colors.

        Input: String
        Output: String
    """
    return COLORS[color_code]

def create_price_tye(price_range):
    """ Função que transforma o número a sua classificação verbal entre cheap, normal, expensive e gourmet

        Input: int
        Output: String
    """
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

def rename_columns(dataframe):
    """ Função que transforma os títulos das colunas do dataframe em títulos snake case

        Input: dataframe
        Output: dataframe
    """
    
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

def clean_dataframe(df):
    """ Função que aplica todos os processos de limpezas necessários para esse dataframe

        Limpezas e transformações realizadas:

        1.Criação da coluna country, representando em string o país do country code. 

        2.Criação da coluna color, representando em string a cor do Rating color

        3. Criação da coluna price_tye, representando em string o tipo de preço do Price range

        4. Tranformação de todos os nomes de coluna em snake case

        5. Escolha de apenas um tipo de culinária para cada restaurante

        6. Remoção de NaN da coluna cuisines

        7. Remoção da coluna switch to order menu

        8. Limpando tipos de comidas unicos

        Input: dataframe
        Output: dataframe
    """

    for i in range(len(df['Country Code'])):
        df.loc[i,'Country'] = country_name(df.loc[i,'Country Code'])
        df.loc[i,'Color'] = color_name(df.loc[i,'Rating color'])
        df.loc[i,'Price_tye'] = create_price_tye(df.loc[i,'Price range'])
    df = rename_columns(df)

    df['cuisines'] = df['cuisines'].astype(str)
    df = df.loc[df['cuisines'] != 'nan',:].reset_index(drop=True)
    df = df.loc[df['cuisines'] != 'Drinks Only',:].reset_index(drop=True)
    df = df.loc[df['restaurant_name'] != 'O Mineiro Prime',:].reset_index(drop=True)
    df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])
    df = df.drop('switch_to_order_menu', axis=1)
    df = df.drop_duplicates()
    return df
#================================================================================================================================#
#                                           Começo da Estrutura Lógica do Código                                                 #
#================================================================================================================================#


#Import dataframe
df = pd.read_csv("dataset/zomato.csv")

#Cleaning dataframe
df1 = clean_dataframe(df)



#===========================================================================================#
#                                  Sidebar Streamlit                                        #
#===========================================================================================#



st.sidebar.markdown( '# Filtros do mapa' )
country_option = st.sidebar.multiselect("Escolha de quais países deseja visualizar os restaurantes",["India", "Australia", "Brazil", "Canada", "Indonesia", "New Zeland","Philippines","Qatar",
                                                                  "Singapure","South Africa","Sri Lanka","Turkey","United Arab Emirates","England", "United States of America"],
                                        default = ['Brazil','England','Qatar','South Africa','Canada','Australia'])
st.sidebar.markdown("""---""")
values_rating = st.sidebar.slider("Escolha entre quais notas devem estar os restaurantes", 0.0, 5.0, (0.0, 5.0))
#Country filter map
linhas_selecionadas = df1['country'].isin(country_option)
dfmap= df1.loc[linhas_selecionadas,:]
#Country filter map
linhas_selecionadas = (dfmap['aggregate_rating'] >= values_rating[0]) & (dfmap['aggregate_rating'] <= values_rating[1])
dfmap= dfmap.loc[linhas_selecionadas,:]

st.sidebar.markdown('#### Dados tratados')

# Converter o dataframe para CSV em memória
csv_data = df1.to_csv(sep=',',index=False)

# Adicionar um botão de download
st.sidebar.download_button(
    label="Download",
    data=csv_data.encode('utf-8'),  # Converta os dados para bytes
    file_name="data.csv",
    mime="text/csv",
)

st.sidebar.markdown(" ### Powered by Paulo R. O. Ferreira")



#===========================================================================================#
#                                Layout Streamlit                                           #
#===========================================================================================#

st.markdown('# 📋 Visão Geral ')

with st.container():
    st.markdown('### Métricas gerais e marcos da nossa plataforma:')
    col1,col2,col3,col4,col5= st.columns(5)
    with col1:
        restaurantes = len(df1['restaurant_id'].unique())
        col1.metric("Restaurantes cadastrados", restaurantes)
    with col2:
        countries = len(df1['country'].unique())
        col2.metric("Países cadastrados", countries)
    with col3:
        cities = len(df1['city'].unique())
        col3.metric("Cidades cadastradas", cities)
    with col4:
        total_votes = df1['votes'].sum()
        total_votes = '{:,}'.format(total_votes).replace(',', '.')
        col4.metric("Quantidade total de avaliações", total_votes)
        
    with col5:
        culinarias = len(df1['cuisines'].unique())
        col5.metric("Tipos de Culinárias Oferecidas", culinarias)
        
    st.markdown("""---""")
with st.container():
    st.markdown('### Visão geográfica dos restaurantes:')
    restaurant_map(dfmap)
