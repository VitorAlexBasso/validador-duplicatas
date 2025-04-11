import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Duplicatas com Detalhes", layout="centered")

st.title("🔍 Validador de Nomes Duplicados com Detalhes")
st.write("Identifica nomes duplicados (coluna D) e mostra seus respectivos códigos (coluna A).")

uploaded_file = st.file_uploader("📎 Envie sua planilha Excel (.xlsx)", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        st.success("✅ Planilha carregada com sucesso!")

        # Normalização do nome
        df["Nome_normalizado"] = df.iloc[:, 3].astype(str).str.strip().str.upper()  # Coluna D
        df["Código"] = df.iloc[:, 0]  # Coluna A

        # Filtra os nomes que aparecem mais de uma vez
        nomes_duplicados = df[df.duplicated("Nome_normalizado", keep=False)]

        # Resultado final apenas com as colunas desejadas
        resultado = nomes_duplicados[[df.columns[0], df.columns[3]]].rename(columns={
            df.columns[0]: "Código",
            df.columns[3]: "Nome"
        })

        st.subheader("📋 Cadastros Duplicados Encontrados")
        st.dataframe(resultado)

        # Geração do Excel para download
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            resultado.to_excel(writer, index=False, sheet_name="Duplicados")
        output.seek(0)

        st.download_button(
            label="📥 Baixar resultado em Excel",
            data=output,
            file_name="duplicados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Erro ao processar a planilha: {e}")
