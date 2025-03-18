import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração do Streamlit
st.title("ERP Financeiro com Streamlit")
menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios"]
choice = st.sidebar.selectbox("Selecione uma opção", menu)

conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()

if choice == "Relatórios":
    st.subheader("Relatórios Financeiros")
    
    # Fluxo de Caixa por Mês
    st.subheader("Fluxo de Caixa por Mês")
    df_fluxo = pd.read_sql_query("SELECT strftime('%Y-%m', data) as mes, tipo, SUM(valor) as total FROM lancamentos GROUP BY mes, tipo", conn)
    df_pivot = df_fluxo.pivot(index='mes', columns='tipo', values='total').fillna(0)
    st.line_chart(df_pivot)
    
    # Status das Contas a Pagar e Receber
    st.subheader("Status das Contas a Pagar e Receber")
    df_pagar = pd.read_sql_query("SELECT status, SUM(valor) as total FROM contas_pagar GROUP BY status", conn)
    df_receber = pd.read_sql_query("SELECT status, SUM(valor) as total FROM contas_receber GROUP BY status", conn)
    df_status = pd.concat([df_pagar, df_receber])
    fig, ax = plt.subplots()
    sns.barplot(x=df_status['status'], y=df_status['total'], ax=ax)
    st.pyplot(fig)
    
    # Comparação Receita vs Despesa
    st.subheader("Comparação Receita vs Despesa")
    df_comparacao = pd.read_sql_query("SELECT tipo, SUM(valor) as total FROM lancamentos WHERE strftime('%Y-%m', data) = strftime('%Y-%m', 'now') GROUP BY tipo", conn)
    fig, ax = plt.subplots()
    sns.barplot(x=df_comparacao['tipo'], y=df_comparacao['total'], ax=ax)
    st.pyplot(fig)

conn.close()