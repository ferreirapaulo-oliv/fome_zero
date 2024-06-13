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

st.set_page_config(page_title = 'Cidades', page_icon = '🏙️', layout = 'wide')

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

def graph_count_by_filter(df, title_graph, title_x, title_y,coluna_filtro,logica,valor):
    """Função que faz um grafico de uma quantidade de uma coluna agrupada por cidade e por pais e
       possui a opção de limitar a busca.

        Input: Dataframe, coluna 1, coluna 2, título grafico, título x, título, y
        Output: Gráfico de barra
    """

    if logica == 1:
        linhas_selecionadas = df[coluna_filtro] >= valor
        df_aux= df.loc[linhas_selecionadas,:]
    if logica == 2:
        linhas_selecionadas = df[coluna_filtro] <= valor
        df_aux= df.loc[linhas_selecionadas,:]
    

    
    cols = ['restaurant_id', 'city', 'country']
    df_aux = df_aux.loc[:, cols].groupby(['country', 'city']).nunique().sort_values(by='restaurant_id', ascending=False).reset_index()
    df_aux = df_aux.groupby('city').first().reset_index().sort_values(by='restaurant_id', ascending=False).head(7)
    fig = px.bar(df_aux, x='city', y='restaurant_id',
                 text='restaurant_id',
                 color='country',  
                 labels={'city': title_x, 'restaurant_id': title_y, 'country': 'Países'},  
                 color_discrete_sequence=px.colors.qualitative.Plotly)  
    fig.update_layout(title_text=title_graph, title_x=0.5, title_xanchor="center")
    fig.update_layout({ 'yaxis': {'gridcolor': 'rgba(0, 0, 0, 0.1)'}})
    return fig



def graph_count_by(df, coluna, title_graph, title_x, title_y):
    """Função que faz um grafico de uma quantidade de uma coluna agrupada por cidade e por pais

        Input: Dataframe, coluna 1, coluna 2, título grafico, título x, título, y
        Output: Gráfico de barra
    """
    
    cols = [coluna, 'city', 'country']
    df_aux = df.loc[:, cols].groupby(['country', 'city']).nunique().sort_values(by=coluna, ascending=False).reset_index()
    df_aux = df_aux.groupby('city').first().reset_index().sort_values(by=coluna, ascending=False).head(10)
    fig = px.bar(df_aux, x='city', y=coluna,
                 text=coluna,
                 color='country',  
                 labels={'city': title_x, coluna: title_y, 'country': 'Países'},  
                 color_discrete_sequence=px.colors.qualitative.Plotly)  
    fig.update_layout(title_text=title_graph, title_x=0.5, title_xanchor="center")
    fig.update_layout({ 'yaxis': {'gridcolor': 'rgba(0, 0, 0, 0.1)'}})
    return fig
    

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
#Download dataframe
#df1.to_csv("data.csv", index=False)

#===========================================================================================#
#                                  Sidebar Streamlit                                        #
#===========================================================================================#



st.sidebar.markdown( '# Filtros' )
country_option = st.sidebar.multiselect("Escolha entre quais países deseja analisar",["India", "Australia", "Brazil", "Canada", "Indonesia", "New Zeland","Philippines","Qatar",
                                                                  "Singapure","South Africa","Sri Lanka","Turkey","United Arab Emirates","England", "United States of America"],
                                        default = ['Brazil','England','Qatar','South Africa','Canada','Australia'])
st.sidebar.markdown("""---""")

#Country filter map
linhas_selecionadas = df1['country'].isin(country_option)
df1= df1.loc[linhas_selecionadas,:]

st.sidebar.markdown(" ### Powered by Paulo R. O. Ferreira")

#===========================================================================================#
#                                Layout Streamlit                                           #
#===========================================================================================#
with st.container():
    st.markdown( '# 🏙️ Visão Cidades' )
    fig = graph_count_by(df1,'restaurant_id','Top 10 cidades com mais restaurantes registrados','Cidades','Quantidade de restaurantes')
    st.plotly_chart(fig,use_container_width = True)
with st.container():
    col1,col2 = st.columns(2)
    with col1:

        fig = graph_count_by_filter(df1,'Top 7 cidades com mais restaurantes com avaliação acima de 4','Cidades','Quantidade de restaurantes','aggregate_rating',1,4)
        st.plotly_chart(fig,use_container_width = True)
    with col2:
        fig = graph_count_by_filter(df1,'Top 7 cidades com mais restaurantes com avaliação abaixo de 2.5','Cidades','Quantidade de restaurantes','aggregate_rating',2,2.5)
        st.plotly_chart(fig,use_container_width = True)
with st.container():
    fig = graph_count_by(df1,'cuisines','Top 10 cidades com mais restaurantes com culinárias distintas','Cidades','Quantidade de restaurantes')
    st.plotly_chart(fig,use_container_width = True)




