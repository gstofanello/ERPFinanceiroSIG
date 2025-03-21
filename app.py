import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import datetime

# Interface Streamlit
def main():
    st.title("ERP Financeiro com Streamlit")
    
    menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    
    if choice == "Clientes":
        st.subheader("Cadastro de Clientes")
        df = pd.read_sql_query("SELECT * FROM clientes", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Pagar":
        st.subheader("Contas a Pagar")
        df = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Receber":
        st.subheader("Contas a Receber")
        df = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        st.dataframe(df)
        
    elif choice == "Lançamentos":
        st.subheader("Lançamentos Financeiros")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        st.dataframe(df)
        
    elif choice == "Relatórios":
        st.subheader("Relatório de Fluxo de Caixa")
        df = pd.read_sql_query("SELECT tipo, COALESCE(SUM(valor), 0) as total FROM lancamentos GROUP BY tipo", conn)
        st.dataframe(df)
        
        # Top 5 Clientes com Maior Receita
        st.subheader("Top 5 Clientes com Maior Receita")
        top_clientes = pd.read_sql_query("""
            SELECT c.nome, COALESCE(SUM(cr.valor), 0) as total_receita 
            FROM contas_receber cr 
            JOIN clientes c ON cr.cliente_id = c.id 
            WHERE cr.status = 'Recebido'
            GROUP BY c.nome 
            ORDER BY total_receita DESC 
            LIMIT 5
        """, conn)
        
        if not top_clientes.empty:
            st.dataframe(top_clientes)
            fig, ax = plt.subplots()
            ax.bar(top_clientes['nome'], top_clientes['total_receita'], color='green')
            ax.set_xlabel("Clientes")
            ax.set_ylabel("Receita Total")
            ax.set_title("Top 5 Clientes com Maior Receita")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        # Comparação Receita vs Despesa
        st.subheader("Comparação Receita vs Despesa")
        receita_despesa = pd.read_sql_query("""
            SELECT tipo, COALESCE(SUM(valor), 0) as total FROM lancamentos
            WHERE data >= DATE('now', 'start of month')
            GROUP BY tipo
        """, conn)
        
        if not receita_despesa.empty:
            st.dataframe(receita_despesa)
            fig, ax = plt.subplots()
            ax.bar(receita_despesa['tipo'], receita_despesa['total'], color=['green', 'red'])
            ax.set_xlabel("Tipo")
            ax.set_ylabel("Valor Total")
            ax.set_title("Receita vs Despesa - Mês Atual")
            st.pyplot(fig)
        
        # Distribuição das Contas a Pagar por Fornecedor
        st.subheader("Distribuição das Contas a Pagar por Fornecedor")
        distribuicao_fornecedores = pd.read_sql_query("""
            SELECT fornecedor, COALESCE(SUM(valor), 0) as total FROM contas_pagar
            WHERE status = 'Pendente'
            GROUP BY fornecedor
            ORDER BY total DESC
        """, conn)
        
        if not distribuicao_fornecedores.empty:
            st.dataframe(distribuicao_fornecedores)
            fig, ax = plt.subplots()
            ax.pie(distribuicao_fornecedores['total'], labels=distribuicao_fornecedores['fornecedor'], autopct='%1.1f%%', startangle=90)
            ax.set_title("Distribuição das Contas a Pagar por Fornecedor")
            st.pyplot(fig)
    
    conn.close()
    
if __name__ == "__main__":
    main()
