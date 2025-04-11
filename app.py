import streamlit as st
import pandas as pd

st.set_page_config(page_title="Validador de Duplicatas", layout="centered")

st.title("🔍 Validador de Nomes e CNPJs Duplicados")
st.write("Faça o upload de uma planilha `.xlsx` para detectar **nomes e CNPJs duplicados**.")

uploaded_file = st.file_uploader("📎 Envie sua planilha Excel (.xlsx)", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        st.success("✅ Planilha carregada com sucesso!")

        df["Nome_normalizado"] = df["Nome"].astype(str).str.strip().str.upper()
        nomes_duplicados = df[df.duplicated("Nome_normalizado", keep=False)]

        df["CNPJ_normalizado"] = df["CPF/CNPJ"].astype(str).str.replace(r"\\D", "", regex=True)
        cnpjs_duplicados = df[df["CNPJ_normalizado"].duplicated(keep=False) & df["CNPJ_normalizado"].str.len() > 0]

        st.subheader("📛 Nomes Duplicados")
        st.dataframe(nomes_duplicados[["Nome", "CPF/CNPJ"]].drop_duplicates())

        st.subheader("🔢 CNPJs Duplicados")
        st.dataframe(cnpjs_duplicados[["Nome", "CPF/CNPJ"]].drop_duplicates())

        resultado_final = pd.concat([
            nomes_duplicados[["Nome", "CPF/CNPJ"]],
            cnpjs_duplicados[["Nome", "CPF/CNPJ"]]
        ]).drop_duplicates()

        csv = resultado_final.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Baixar resultados em CSV", csv, "duplicatas.csv", "text/csv")

    except Exception as e:
        st.error(f"Erro ao processar a planilha: {e}")
