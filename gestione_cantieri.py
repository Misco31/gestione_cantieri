import streamlit as st
import pandas as pd

# Configurazione dell'app per dispositivi mobili
st.set_page_config(page_title="Gestione Cantieri", layout="wide")

# Funzione per caricare i dati dai file CSV
def carica_dati():
    try:
        mezzi_df = pd.read_csv("mezzi.csv", dtype=str)
        cantieri_df = pd.read_csv("cantieri.csv", dtype=str)
        return mezzi_df, cantieri_df
    except Exception as e:
        st.error(f"Errore nel caricamento dei file CSV: {e}")
        st.stop()

# Funzione per salvare i dati aggiornati nei file CSV
def salva_cantieri(cantieri_df):
    try:
        cantieri_df.to_csv("cantieri.csv", index=False)
    except Exception as e:
        st.error(f"Errore durante il salvataggio del file CSV: {e}")

# Funzione per salvare i dati dei mezzi
def salva_mezzi(mezzi_df):
    try:
        mezzi_df.to_csv("mezzi.csv", index=False)
    except Exception as e:
        st.error(f"Errore durante il salvataggio del file CSV: {e}")

# Funzione per spostare un mezzo al cantiere di destinazione
def sposta_mezzo(cantieri_df, id_mezzo, cantiere_destinazione):
    for index, row in cantieri_df.iterrows():
        mezzi_ids = row["mezzi_assegnati"]
        if pd.isna(mezzi_ids) or mezzi_ids == "":
            mezzi_ids = []
        else:
            mezzi_ids = mezzi_ids.split(",")

        if id_mezzo in mezzi_ids:
            mezzi_ids.remove(id_mezzo)
            cantieri_df.at[index, "mezzi_assegnati"] = ",".join(mezzi_ids)

    mezzi_ids = cantieri_df.loc[cantieri_df["id_cantiere"] == cantiere_destinazione, "mezzi_assegnati"].values[0]
    if pd.isna(mezzi_ids) or mezzi_ids == "":
        mezzi_ids = []
    else:
        mezzi_ids = mezzi_ids.split(",")

    if id_mezzo not in mezzi_ids:
        mezzi_ids.append(id_mezzo)
        cantieri_df.loc[cantieri_df["id_cantiere"] == cantiere_destinazione, "mezzi_assegnati"] = ",".join(mezzi_ids)

    salva_cantieri(cantieri_df)
    nome_cantiere = cantieri_df.loc[cantieri_df["id_cantiere"] == cantiere_destinazione, "nome_cantiere"].values[0]
    st.success(f"✅ Mezzo '{id_mezzo}' spostato correttamente al cantiere '{nome_cantiere}'.")

# Funzione per aggiungere un nuovo cantiere
def aggiungi_cantiere(cantieri_df, nome):
    try:
        nuovo_id = int(cantieri_df["id_cantiere"].max()) + 1 if not cantieri_df.empty else 1
        nuovo_cantiere = pd.DataFrame([{
            "id_cantiere": nuovo_id,
            "nome_cantiere": nome,
            "stato": "Aperto",
            "mezzi_assegnati": ""
        }])
        cantieri_df = pd.concat([cantieri_df, nuovo_cantiere], ignore_index=True)
        salva_cantieri(cantieri_df)
        st.success(f"✅ Cantiere '{nome}' aggiunto correttamente.")
    except Exception as e:
        st.error(f"Errore durante l'aggiunta del cantiere: {e}")

# Funzione per chiudere un cantiere
def chiudi_cantiere(cantieri_df, id_cantiere):
    cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "stato"] = "Chiuso"
    salva_cantieri(cantieri_df)
    nome_cantiere = cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "nome_cantiere"].values[0]
    st.success(f"✅ Cantiere '{nome_cantiere}' chiuso correttamente.")

# Carica i dati direttamente dai file CSV
mezzi_df, cantieri_df = carica_dati()

# Menu laterale fisso
with st.sidebar:
    st.title("Menu di Navigazione")
    if st.button("🏠 Home"):
        st.session_state["pagina"] = "Home"

    if st.button("🔄 Sposta"):
        st.session_state["pagina"] = "Gestione_Mezzi"

    if st.button("🏗️ Aggiungi"):
        st.session_state["pagina"] = "Gestione_Cantieri"

# Controllo dello stato della pagina
pagina = st.session_state.get("pagina", "Home")

# Pagina Home
if pagina == "Home":
    st.title("🚜 Elenco Mezzi per Categoria")
    categorie = mezzi_df["Categoria"].unique()
    for categoria in categorie:
        st.header(f"Categoria: {categoria}")
        mezzi_categoria = mezzi_df[mezzi_df["Categoria"] == categoria]
        for _, mezzo in mezzi_categoria.iterrows():
            id_mezzo = mezzo["ID"]
            nome_mezzo = mezzo["Nome"]
            cantiere_associato = "Non assegnato"
            for _, cantiere in cantieri_df.iterrows():
                if id_mezzo in cantiere["mezzi_assegnati"].split(","):
                    cantiere_associato = cantiere["nome_cantiere"]
                    break
            st.markdown(f"**🆔 {id_mezzo} - {nome_mezzo}**")
            st.markdown(f"- Cantiere: **{cantiere_associato}**")

# Ora tutte le modifiche sono salvate direttamente nei file CSV.

