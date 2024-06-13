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

st.set_page_config(page_title = 'Visao Países', page_icon = '🌍', layout = 'wide')

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

def graph_mean_by(df,coluna1,coluna2,title_graph,title_x,title_y):
    """Função que faz um grafico de uma media de uma coluna agrupada por uma segunda coluna

        Input: Dataframe, coluna 1, coluna 2,título grafico, título x, título, y
        Output: Gráfico de barra
    """
    cols = [coluna1, coluna2]
    df_aux = df.loc[:,cols].groupby(coluna2).mean().sort_values(by=coluna1,ascending=False).reset_index()
    df_aux[coluna1] = df_aux[coluna1].round(2)
    fig = (px.bar(df_aux, x = coluna2, y = coluna1,
                 text=coluna1,
                 labels={coluna2: title_x, coluna1: title_y},
                 color_discrete_sequence=px.colors.qualitative.Plotly))
    fig.update_layout(title_text=title_graph, title_x=0.5,title_xanchor="center")
    fig.update_layout({ 'yaxis': {'gridcolor': 'rgba(0, 0, 0, 0.1)'}})
    return fig



def graph_count_by(df,coluna1,coluna2,title_graph,title_x,title_y):
    """Função que faz um grafico de uma quantidade de uma coluna agrupada por uma segunda coluna

        Input: Dataframe, coluna 1, coluna 2,título grafico, título x, título, y
        Output: Gráfico de barra
    """
    cols = [coluna1, coluna2]
    df_aux = df.loc[:,cols].groupby(coluna2).nunique().sort_values(by=coluna1,ascending=False).reset_index()
    fig = (px.bar(df_aux, x = coluna2, y = coluna1,
                 text=coluna1,
                 labels={coluna2: title_x, coluna1: title_y},
                 color_discrete_sequence=px.colors.qualitative.Plotly))
    fig.update_layout(title_text=title_graph, title_x=0.5,title_xanchor="center")
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
values_rating = st.sidebar.slider("Escolha entre quais notas devem estar os restaurantes", 0.0, 5.0, (0.0, 5.0))
#Country filter map
linhas_selecionadas = df1['country'].isin(country_option)
df1= df1.loc[linhas_selecionadas,:]
#Country filter map
linhas_selecionadas = (df1['aggregate_rating'] >= values_rating[0]) & (df1['aggregate_rating'] <= values_rating[1])
df1= df1.loc[linhas_selecionadas,:]
st.sidebar.markdown(" ### Powered by Paulo R. O. Ferreira")

#===========================================================================================#
#                                Layout Streamlit                                           #
#===========================================================================================#
with st.container():
    st.markdown( '# 🌎 Visão Países' )
    fig = graph_count_by(df1,'restaurant_id','country','Quantidade de restaurantes por país','Países','Quantidade de restaurantes')
    st.plotly_chart(fig,use_container_width = True)
with st.container():
    fig = graph_count_by(df1,'city','country','Quantidade de cidades por país','Países','Quantidade de cidades')
    st.plotly_chart(fig,use_container_width = True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        fig = graph_mean_by(df1,'votes','country','Quantidade média de avaliações por país','Países','Quantidade de avaliações')
        st.plotly_chart(fig,use_container_width = True)
    with col2:
        fig = graph_mean_by(df1,'average_cost_for_two','country','Custo médio de uma refeição para dois por país','Países','Preço na moeda local')
        st.plotly_chart(fig,use_container_width = True)
    



