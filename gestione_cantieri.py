import streamlit as st
import pandas as pd

# Configurazione dell'app per dispositivi mobili
st.set_page_config(page_title="Gestione Cantieri", layout="centered", initial_sidebar_state="expanded")

# Funzione per caricare i dati dai file CSV
def carica_dati():
    try:
        mezzi_df = pd.read_csv("mezzi.csv", dtype=str)
        cantieri_df = pd.read_csv("cantieri.csv", dtype=str)
        return mezzi_df, cantieri_df
    except Exception as e:
        st.error(f"Errore nel caricamento dei file CSV: {e}")
        st.stop()

# Funzione per salvare i dati aggiornati
def salva_cantieri(cantieri_df):
    try:
        cantieri_df.to_csv("cantieri.csv", index=False)
    except Exception as e:
        st.error(f"Errore nel salvataggio del file CSV: {e}")

# Funzione per mostrare i mezzi assegnati a un cantiere
def mostra_mezzi_assegnati(cantieri_df, mezzi_df, id_cantiere):
    mezzi_ids = cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "mezzi_assegnati"].values
    if len(mezzi_ids) == 0 or pd.isna(mezzi_ids[0]) or mezzi_ids[0] == "":
        return []
    mezzi_ids = mezzi_ids[0].split(",")
    mezzi_assegnati = mezzi_df[mezzi_df["ID"].isin(mezzi_ids)]
    return mezzi_assegnati[["ID", "Nome"]].to_dict(orient="records")

# Carica i dati
mezzi_df, cantieri_df = carica_dati()

# Verifica che i DataFrame non siano vuoti
if mezzi_df.empty or cantieri_df.empty:
    st.error("I file CSV sono vuoti o non contengono dati validi.")
    st.stop()

# Menu di Navigazione
with st.sidebar:
    selezione_pagina = st.radio("Navigazione", ["Home", "Gestione Mezzi", "Chiusura Cantiere"])

# Pagina Home
if selezione_pagina == "Home":
    st.title("🏗️ Cantieri Attivi")
    cantieri_aperti = cantieri_df[cantieri_df["stato"] == "Aperto"]

    if cantieri_aperti.empty:
        st.info("Non ci sono cantieri attivi.")
    else:
        for _, cantiere in cantieri_aperti.iterrows():
            st.markdown(f"### 📍 Cantiere: **{cantiere['nome_cantiere']}**")
            mezzi_assegnati = mostra_mezzi_assegnati(cantieri_df, mezzi_df, cantiere["id_cantiere"])

            if not mezzi_assegnati:
                st.markdown("*Nessun mezzo assegnato.*")
            else:
                for mezzo in mezzi_assegnati:
                    st.markdown(f"- 🚜 **{mezzo['ID']} - {mezzo['Nome']}**")

            st.markdown("---")

# Pagina Gestione Mezzi
elif selezione_pagina == "Gestione Mezzi":
    st.title("🔄 Spostamento Mezzi")
    mezzo_selezionato = st.selectbox("🚜 Seleziona il mezzo da spostare", mezzi_df["ID"].tolist(), format_func=lambda x: f"{x} - {mezzi_df[mezzi_df['ID'] == x]['Nome'].values[0]}")
    cantiere_attuale = st.selectbox("🏗️ Cantiere Attuale", cantieri_df["id_cantiere"].tolist(), format_func=lambda x: cantieri_df[cantieri_df["id_cantiere"] == x]["nome_cantiere"].values[0])
    cantiere_destinazione = st.selectbox("🏗️ Cantiere Destinazione", cantieri_df["id_cantiere"].tolist(), format_func=lambda x: cantieri_df[cantieri_df["id_cantiere"] == x]["nome_cantiere"].values[0])

    if st.button("Sposta Mezzo"):
        sposta_mezzo(cantieri_df, mezzo_selezionato, cantiere_attuale, cantiere_destinazione)

# Pagina Chiusura Cantiere
elif selezione_pagina == "Chiusura Cantiere":
    st.title("🔒 Chiusura Cantiere")
    cantiere_da_chiudere = st.selectbox("Seleziona il cantiere da chiudere", cantieri_df[cantieri_df["stato"] == "Aperto"]["id_cantiere"].tolist(), format_func=lambda x: cantieri_df[cantieri_df["id_cantiere"] == x]["nome_cantiere"].values[0])
    if st.button("Chiudi Cantiere"):
        cantieri_df.loc[cantieri_df["id_cantiere"] == cantiere_da_chiudere, "stato"] = "Chiuso"
        salva_cantieri(cantieri_df)
        st.success(f"✅ Cantiere '{cantiere_da_chiudere}' chiuso con successo!")

