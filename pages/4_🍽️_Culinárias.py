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

st.set_page_config(page_title = 'Culinárias', page_icon = '🍽️', layout = 'wide')

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

def cuisines_graph(df,num,logical,title_graph):
    """Retorna o top 'num' de melhores ou piores tipos de culinária, a depender do lógical

        Input: Dataframe, int, (1 or 2), string
        Output: Dataframe
    """

    if logical == 1:
        df_aux = (df.loc[:,['aggregate_rating','cuisines']]
                    .groupby('cuisines')
                    .mean().sort_values(by = 'aggregate_rating',ascending = False)).reset_index()
        df_aux['aggregate_rating'] = df_aux['aggregate_rating'].round(2)
    elif logical == 2:
        df_aux = (df.loc[:,['aggregate_rating','cuisines']]
                    .groupby('cuisines')
                    .mean().sort_values(by = 'aggregate_rating',ascending = True)).reset_index()
        df_aux['aggregate_rating'] = df_aux['aggregate_rating'].round(2)  
    fig = (px.bar(df_aux.head(num), x = 'cuisines', y = 'aggregate_rating',
                 text='aggregate_rating',
                 labels={'aggregate_rating': 'Média das avaliações', 'cuisines': 'Tipos de culinária'},
                 color_discrete_sequence=px.colors.qualitative.Plotly))
    fig.update_layout(title_text=title_graph, title_x=0.5, title_xanchor="center")
    fig.update_layout({ 'yaxis': {'gridcolor': 'rgba(0, 0, 0, 0.1)'}})
    return fig


def top_restaurants(df,num):
    """Retorna o top 'num' restaurantes mais ordenados por maior média de avaliação e  mais antigo

        Input: Dataframe, int
        Output: Dataframe
    """
    
    df_aux = (df.loc[:,['restaurant_id','restaurant_name','country','city','cuisines','average_cost_for_two','aggregate_rating','votes']]
                .sort_values(by=['aggregate_rating','restaurant_id'],ascending=[False,True]))
    df_aux['restaurant_id'] = df_aux['restaurant_id'].astype(str)
    df_aux = df_aux.head(num)
    return df_aux



def melhor_restaurant(df,culinaria):
    """ Função que recebe um Dataframa e um tipo de culinaria e realiza as seguintes operações

        Etapas:

        1. Filtra o dataframe para exibir apenas aquele tipo de culinaria
        2. Ordena o dataframe com as melhores notas e como critério de desempate os mais avaliados
        3. Retira informações sobre o melhor restaurante seguindo esses criterios
        4. Retorna os textos formatados para se utilizar no metric

        Input: Dataframe, String
        Output: String1, String2, String3
    """
    
    df_aux = df.loc[df['cuisines'] == culinaria,:].sort_values(by=['aggregate_rating','votes'],ascending=[False,False])
    retorno1 = '{} : {}'.format(culinaria,df_aux.iloc[0,1]) 
    retorno2 = '{}/5.0'.format(df_aux.iloc[0,16])
    retorno3 = 'Pais: {} \n\nCidade: {}\n\nMédia do prato para dois: {}({})'.format(df_aux.iloc[0,20],df_aux.iloc[0,3],df_aux.iloc[0,10],df_aux.iloc[0,11])
    return retorno1, retorno2, retorno3


def retorna_5(df):
    df_aux = df.loc[:,['votes','cuisines']].groupby('cuisines').sum().sort_values(by='votes',ascending=False).reset_index()
    lista = [df_aux.iloc[0,0],df_aux.iloc[1,0],df_aux.iloc[2,0],df_aux.iloc[3,0],df_aux.iloc[4,0]]
    return lista

    
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



st.sidebar.markdown("""---""")
st.sidebar.markdown( '# Filtros' )
country_option = st.sidebar.multiselect("Escolha entre quais países deseja analisar",df1['country'].unique(),
                                        default = ['Brazil','England','Qatar','South Africa','Canada','Australia'])


num_rest = st.sidebar.slider("Escolha a quantidade de restaurantes que deseja analisar", 0, 20, 10)

cuisines_option = st.sidebar.multiselect("Escolha os tipos de culinária",df1["cuisines"].unique(),
                                        default = ['Italian','Arabian','Japanese','BBQ','Brazilian','American'])
#Criação do dataframe que ira ser aplicado os filtros
df2 = df1.copy()

#Country filter 
linhas_selecionadas = df2['country'].isin(country_option)
df2= df2.loc[linhas_selecionadas,:]

#Cuisines filter
linhas_selecionadas = df2['cuisines'].isin(cuisines_option)
df3 = df2.loc[linhas_selecionadas,:]

st.sidebar.markdown(" ### Powered by Paulo R. O. Ferreira")

#===========================================================================================#
#                                Layout Streamlit                                           #
#===========================================================================================#

with st.container():
    st.markdown( '# 🍽️ Visão Tipos de culinária' )
    st.markdown('## Melhor restaurante dos principais tipos de culinária')
    lista = retorna_5(df2)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        label_text,value_text,help_text = melhor_restaurant(df1,lista[0])
        col1.metric(label_text, value_text, help=help_text)
    with col2:
        label_text,value_text,help_text = melhor_restaurant(df1,lista[1])
        col2.metric(label_text, value_text, help=help_text)
    with col3:
        label_text,value_text,help_text = melhor_restaurant(df1,lista[2])
        col3.metric(label_text, value_text, help=help_text)
    with col4:
        label_text,value_text,help_text = melhor_restaurant(df1,lista[3])
        col4.metric(label_text, value_text, help=help_text)
    with col5:
        label_text,value_text,help_text = melhor_restaurant(df1,lista[4])
        col5.metric(label_text, value_text, help=help_text)
with st.container():
        st.markdown('## Top {} melhores restaurantes'.format(num_rest))
        df_top = top_restaurants(df3,num_rest)
        st.dataframe(df_top)
with st.container():
    col1,col2= st.columns(2)
    with col1:
        fig = cuisines_graph(df2,num_rest,1,'Top {} melhores tipos de culinária'.format(num_rest))
        st.plotly_chart(fig,use_container_width = True)
    with col2:
        fig = cuisines_graph(df2,num_rest,2,'Top {} piores tipos de culinária'.format(num_rest))
        st.plotly_chart(fig,use_container_width = True)
        

    
