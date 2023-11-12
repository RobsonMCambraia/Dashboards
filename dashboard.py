# Importa as bibliotecas necessárias: Streamlit para a criação de uma interface web,
# Pandas para manipulação de dados, e Plotly Express para visualização de gráficos.
import streamlit as st
import pandas as pd
import plotly.express  as px

# Configuração da página para um layout amplo.
st.set_page_config(layout="wide")

# Lê um arquivo CSV chamado "supermarket_sales.csv", usando ";" como delimitador e "," como separador decimal.
# Converte a coluna "Date" para o tipo de data e ordena o DataFrame pela coluna "Date".
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Cria uma nova coluna "Month" no DataFrame, que contém o ano e o mês da data.
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))

# Cria uma caixa de seleção na barra lateral para escolher um mês.
month = st.sidebar.selectbox("Mês", df["Month"].unique())

# Filtra o DataFrame com base no mês selecionado.
df_filtered = df[df["Month"] == month]

# Divide a página em várias colunas para exibir os gráficos.
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Cria um gráfico de barras de faturamento por dia, com cores diferentes para cada cidade.
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)

# Cria um gráfico de barras horizontais do faturamento por tipo de produto, com cores diferentes para cada cidade.
fig_prodts = px.bar(df_filtered, x="Date", y="Product line", 
                  color="City", 
                  title="Faturamento por tipo de produto",
                  orientation="h")
col2.plotly_chart(fig_prodts, use_container_width=True)

# Calcula o faturamento total por filial e cria um gráfico de barras.
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_filial = px.bar(city_total, x="City", y="Total", 
                    title="Faturamento por filial")
col3.plotly_chart(fig_filial, use_container_width=True)

# Cria um gráfico de pizza do faturamento por tipo de pagamento.
fig_kind = px.pie(df_filtered, values="Total", names="Payment",
                  title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_kind, use_container_width=True)

# Calcula a média das avaliações por filial e cria um gráfico de barras.
rating_total = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(rating_total, x="Rating", y="City",
                  title="Avaliação")
col5.plotly_chart(fig_rating, use_container_width=True)
