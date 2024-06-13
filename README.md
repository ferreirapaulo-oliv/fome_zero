# 1. Contexto do Problema de Negócio

A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.

O CEO Guerra também foi recém contratado e precisa entender melhor o negócio
para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a
Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da
empresa e que sejam gerados dashboards, a partir dessas análises, para responder
às seguintes perguntas:

## Geral

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

## Pais

1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4
registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária
distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem
entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam
reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações
registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?

## Cidade

1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de
4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de
2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária
distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que
aceitam pedidos online?

## Restaurantes

1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas
pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor
média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que
possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os
restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que
possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América
possuem um valor médio de prato para duas pessoas maior que as churrascarias
americanas (BBQ)?

# Tipos de Culinária

1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas
pessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos
online e fazem entregas?

# Objetivo

O CEO pediu que fosse gerado um dashboard que permitisse que ele
visualizasse as principais informações das perguntas que ele fez. O CEO precisa
dessas informações o mais rápido possível, uma vez que ele também é novo na
empresa e irá utilizá-las para entender melhor a empresa Fome Zero para conseguir
tomar decisões mais assertivas.

Seu trabalho é utilizar os dados que a empresa Fome Zero possui  e criar o dashboard solicitado.

# 2. Premissas assumidas para análise

1. Não temos informação quanto ao tempo em que o banco de dados foi formado
2. Marketplace é o modelo de negócio assumido
3. As 4 principais visões de negócio foram: Geral, dos países, das cidades e dos tipos de culinária

# 3. Estratégia de solução

O dashboard estratégico foi desenvolvido utilizando as principais métricas analisadas nos 4 tipos de visões do modelo de negócio da empresa.

1. Visão geral do estado atual do marketplace
2. Visão da situação atual dos países
3. Visão da situação atual das cidades
4. Visão da situação atual dos tipos de culinária

Cada visão possui as seguintes métricas apresentadas

1. Visão geral do estado atual do marketplace
    1. Quantidade de restaurantes cadastrados
    2. Países cadastrados
    3. Cidades cadastradas
    4. Quantidade de avaliações feitas
    5. Tipos de culinárias oferecidos
    6. Mapa com a localização dos restaurantes
2. Visão da situação atual dos países
    1. Quantidade de restaurantes por país
    2. Quantidade de cidades por país
    3. Quantidade média de avaliações por país
    4. Preço médio de uma refeição para dois na moeda local
3. Visão da situação atual das cidades
    1. Top 10 cidades com mais restaurantes
    2. Top 7 cidades com mais restaurantes acima de 4.0
    3. Top 7 cidades com mais restaurantes abaixo de 2.5
    4. Top 10 cidades com mais restaurantes com culinárias distintas 
4. Visão da situação atual dos tipos de culinária
    1. Melhor restaurante dos 5 tipos de culinária mais avaliados
    2. Top 10 melhores restaurantes
    3. Top 10 melhores tipos de culinária
    4. Top 10 piores tipos de culinária

# 4. Top 3 insights dos dados

1. Cerca de 45% dos restaurantes registrados são da Índia
2. Das 10 cidades com mais tipos de culinária distintos 3 são dos Estados Unidos da América
3. Dos 10 melhores tipos de culinária 6 são de origem asiática.

# 5. O produto final do projeto

Painel online, hospedado em uma cloud e disponível para qualquer dispositivo que tenha acesso a internet.

O painel pode ser acessado através clicando em: [Painel Streamlit](https://ferreirapaulo-fome-zero.streamlit.app)

# 6. Conclusão

O objetivo final desse projeto é criar um conjunto de gráficos e métricas de avaliações que exibam da melhor forma possível a visão atual da empresa para o novo CEO.

# 7. Próximos passos

1. Criar um dashboard mais estratégico que ajude a empresa a como se posicionar melhor em decisões futuras.
2. Criar novos filtros
3. Adicionar novas visões de negócio.
