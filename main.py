import locale

# import matplotlib.pyplot as plt
import mysql.connector

# import numpy as np
import pandas as pd
import plotly.graph_objects as go

# import plotly_express as px
import streamlit as st

# confirguração padrão da pagina
st.set_page_config(
    page_title="Dash Lizzie",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def conexao():
    # conexão com BD Lizzie

    global conexao
    conexao = mysql.connector.connect(
        host="sql496.main-hosting.eu",
        database="u459129097_lizz",
        user="u459129097_visio",
        password="visiosolucaowebliz13",
    )
    conexao.cursor()
    if conexao.is_connected():
        global bancoConectado
        bancoConectado = "Seja bem-vindo ao Dashboard Lizzie!"
        queryPedido = "SELECT * FROM pedidos"
        queryCliente = "SELECT * FROM clientes"
        queryItensPedidos = "SELECT * FROM itens_pedidos"
        queryProduto = "SELECT * FROM produtos"
        queryVendedor = "SELECT * FROM vendedores"

        global dfCliente, dfPedido, dfItensPedidos, dfProduto, dfVendedor

        dfPedido = pd.read_sql(queryPedido, conexao)
        dfCliente = pd.read_sql(queryCliente, conexao)
        dfItensPedidos = pd.read_sql(queryItensPedidos, conexao)
        dfProduto = pd.read_sql(queryProduto, conexao)
        dfVendedor = pd.read_sql(queryVendedor, conexao)


def criar_grafico_distribuicao_status(dfPedido, year, month):
    dfFiltrado = dfPedido.query("Year == @year and Month == @month")
    status_counts = dfFiltrado["status"].value_counts()
    labels = ["Concluído", "Espera", "Cancelado"]
    values = [status_counts.get(4, 0), status_counts.get(2, 0), status_counts.get(3, 0)]

    fig = go.Figure(data=go.Pie(labels=labels, values=values))
    fig.update_layout(title="Distribuição Percentual dos Pedidos por Status")

    return fig


def criar_grafico_evolucao_pedidos(dfPedido, year, month):
    dfFiltrado = dfPedido.query("Year == @year and Month == @month")
    pedidos_por_mes = (
        dfFiltrado.groupby(["Year", "Month"]).size().reset_index(name="Total Pedidos")
    )

    fig = go.Figure(
        data=go.Scatter(
            x=pedidos_por_mes["Month"],
            y=pedidos_por_mes["Total Pedidos"],
            mode="lines+markers",
        )
    )
    fig.update_layout(
        title="Evolução do Total de Pedidos",
        xaxis_title="Mês",
        yaxis_title="Total de Pedidos",
    )

    return fig


def criar_grafico_pedidos_por_vendedor(dfPedido, dfVendedor, year, month):
    dfFiltrado = dfPedido.query("Year == @year and Month == @month")
    pedidos_por_vendedor = dfFiltrado["id_vendedor"].value_counts()
    pedidos_por_vendedor = pedidos_por_vendedor.rename(
        index=dfVendedor.set_index("id_vendedor")["nome_vendedor"]
    )

    fig = go.Figure(
        data=go.Bar(x=pedidos_por_vendedor.index, y=pedidos_por_vendedor.values)
    )
    fig.update_layout(
        title="Quantidade de Pedidos por Vendedor",
        xaxis_title="Vendedor",
        yaxis_title="Quantidade de Pedidos",
    )

    return fig


def criarDash():
    # MENU LATERAL

    # inicio da pagina
    st.header(":bar_chart: Dashboard Lizzie")
    st.text(f"{bancoConectado}")
    st.markdown("---")

    # Tratamento de Dados
    # extrair mes e ano da tabela pedido
    # sessão 02
    # unifica 2 tabelas DFPEDIDO + DFVENDEDOR COM BASE NO ID

    dfPedido["Month"] = (
        dfPedido["data_pedido"].apply(lambda x: x.month).astype("string")
    )
    dfPedido["Year"] = dfPedido["data_pedido"].apply(lambda x: x.year).astype("string")

    # statusformat = dfPedido["status"].replace(
    #     {4: "Concluido", 2: "Espera", 3: "Cancelado"}, inplace=False
    # )

    # verificar tabelas
    # st.dataframe(dfProduto)
    # st.dataframe(dfPedido)

    #################### sidebar ######################33

    valores_unicos_year = dfPedido["Year"].unique()
    default_values_year = list(valores_unicos_year)
    year = st.sidebar.multiselect(
        key=1,
        label="Ano",
        options=dfPedido["Year"].unique(),
        default=default_values_year,
    )

    valores_unicos_moth = dfPedido["Month"].unique()
    default_values_moth = list(valores_unicos_moth)
    month = st.sidebar.multiselect(
        key=2,
        label="Mês",
        options=dfPedido["Month"].unique(),
        default=default_values_moth,
    )

    # status = st.sidebar.multiselect(
    #     key=3,
    #     label="Status",
    #     options=statusformat.unique(),
    #     default=statusformat.unique(),
    # )

    ######## resultado interação sidebar ##############3
    # SOMA TOTAL
    qtdCliente = dfCliente["id_cliente"].count()
    qtdProdutos = dfProduto["id_produto"].count()

    qtdPedidos = dfPedido.query("Year == @year and Month == @month")[
        "id_cliente"
    ].count()

    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    # totalPedidos = dfPedido.query("Year == @year and Month == @moth")
    total = dfPedido.query("Year == @year and Month == @month")["total_pedido"].sum()
    total_formatado = locale.currency(total, grouping=True)

    statusEntregue = (dfPedido["status"].values == 2).sum()

    total_mes = (
        dfPedido.groupby(by="Year")
        .sum(numeric_only=True)[["total_pedido"]]
        .sort_values("Year")
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    ######### resultado exibido aqui
    col1.metric("Quantidade de Clientes", qtdCliente)
    col2.metric("Total R$ Pedidos", total_formatado)
    col3.metric("Pedidos", qtdPedidos)

    grafico_pedidos_por_vendedor = criar_grafico_pedidos_por_vendedor(
        dfPedido, dfVendedor, year, month
    )
    st.plotly_chart(grafico_pedidos_por_vendedor)

    grafico_evolucao_pedidos = criar_grafico_evolucao_pedidos(dfPedido, year, month)
    st.plotly_chart(grafico_evolucao_pedidos)

    # resultado interação sidebar
    grafico_distribuicao_status = criar_grafico_distribuicao_status(
        dfPedido, year, month
    )
    st.plotly_chart(grafico_distribuicao_status)


conexao()
criarDash()
