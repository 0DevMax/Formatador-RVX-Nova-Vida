import streamlit as st
import pandas as pd

# Função para limpeza e formatação
def processar_base(base):
    # Filtra registros sem óbito
    base = base.loc[base['obito'] != "S"]
    
    # Seleciona colunas específicas
    base = base[['cpf', 'nome', 'nascimento', 'obito', 'ddd0', 'numeroLinha0', 'whatsapp0', 
                 'ddd1', 'numeroLinha1', 'whatsapp1', 'ddd2', 'numeroLinha2', 'whatsapp2', 
                 'ddd3', 'numeroLinha3', 'whatsapp3']]
    
    # Formata a coluna 'nascimento' para o formato 'YYYY-MM-DD'
    base['nascimento'] = base['nascimento'].astype(str).apply(lambda x: f"{x[:4]}-{x[4:6]}-{x[6:]}")
    
    # Cria colunas de telefone apenas para números com WhatsApp marcado como 'S'
    base['telefone0'] = base.apply(lambda x: f"{int(x['ddd0'])}{int(x['numeroLinha0'])}" if x['whatsapp0'] == 'S' else '', axis=1)
    base['telefone1'] = base.apply(lambda x: f"{int(x['ddd1'])}{int(x['numeroLinha1'])}" if x['whatsapp1'] == 'S' else '', axis=1)
    base['telefone2'] = base.apply(lambda x: f"{int(x['ddd2'])}{int(x['numeroLinha2'])}" if x['whatsapp2'] == 'S' else '', axis=1)
    base['telefone3'] = base.apply(lambda x: f"{int(x['ddd3'])}{int(x['numeroLinha3'])}" if x['whatsapp3'] == 'S' else '', axis=1)
    
    # Mantém colunas de interesse e formata o nome
    base = base[['cpf', 'nome', 'nascimento', 'telefone0', 'telefone1', 'telefone2', 'telefone3']]
    base['nome'] = base['nome'].apply(lambda x: x.title())
    
    return base

# Configura a interface do Streamlit
st.title("Limpeza e Formatação de Arquivo CSV")

# Upload do arquivo
uploaded_file = st.file_uploader("Carregue o arquivo CSV", type="csv")

if uploaded_file is not None:
    # Leitura do CSV
    base = pd.read_csv(uploaded_file, sep=';')
    
    # Processamento da base
    base_limpa = processar_base(base)
    
    # Exibir resultado
    st.write("Arquivo Limpo e Formatado:")
    st.dataframe(base_limpa)
    
    # Baixar o arquivo processado
    csv = base_limpa.to_csv(index=False, sep=';').encode('utf-8')
    st.download_button("Baixar CSV Limpo", data=csv, file_name="arquivo_limpo.csv", mime="text/csv")