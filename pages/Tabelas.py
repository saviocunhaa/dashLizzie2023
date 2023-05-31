# import mysql.connector
import streamlit as st

import Home

# confirguração padrão da pagina
st.set_page_config(
    page_title="Dash Lizzie",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def criarDash(dfCliente, dfPedido, dfItensPedidos, dfProduto, dfVendedor):
    # inicio da pagina

    global bancoConectado
    bancoConectado = "Seja bem-vindo ao Dashboard Lizzie!"
    st.header(":bar_chart: Dashboard Lizzie")
    st.text(bancoConectado)
    st.markdown("---")
    st.header("🗃️ Tabela Cliente")
    st.dataframe(dfCliente)
    st.markdown("---")
    st.header("✅ Tabela Pedidos")
    st.dataframe(dfPedido)
    st.markdown("---")
    st.header("👕👗🩲 Tabela Produtos")
    st.dataframe(dfProduto)


# Chame a função conexaoOk() para obter os dataframes

dfCliente, dfPedido, dfItensPedidos, dfProduto, dfVendedor = Home.conexaoOk()
# Passe os dataframes como argumentos para a função criarDash()
criarDash(dfCliente, dfPedido, dfItensPedidos, dfProduto, dfVendedor)
