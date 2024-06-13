#Import de bibliotecas
import streamlit as st
from PIL import Image


###########################################################################
#                   Configurações de pagina e layout html                 #
###########################################################################

st.set_page_config(
    page_title="Página Inicial",
    page_icon="📠",
    layout = 'wide'
)



#Image_path = 'C:\\Users\\User\\Documents\\repos\\ftc_python\\logo.prng'
image = Image.open('logo.png')
st.sidebar.image(image, width = 40)
st.sidebar.markdown( '# Fome Zero!' )
st.sidebar.markdown(' ## O Melhor lugar para encontrar seu mais novo restaurante favorito! ')
st.sidebar.markdown("""---""")
st.sidebar.markdown(' ## Powered by Paulo R. O. Ferreira ')


st.write("Fome Zero Dashboard")

st.markdown("""
            O Dashboard foi construído para rastrear as principais métricas sobre os países, as cidades e os tipos de culinária.
            ## Como usar esse dashboard?

            - Visão Geral:
                - Principais marcas da empresa, a visão geográfica dos restaurantes e os dados tratados.
            - Visão dos Países:
                - Indicadores gerais por países 
            - Visão das Cidades:
                - Indicadores sobre as principais cidades do banco de dados
            - Visão tipos de culinária:
                - Dados baseados nos principais tipos de culinária contidos no banco de dados

                
            ### Por ajuda, procure:
                - Email: ferreirapaulo.oliv@gmail.com
                - Discord: @itscape
            """)