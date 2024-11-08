import streamlit as st
import pandas as pd

# Configurazione dell'app per dispositivi mobili
st.set_page_config(page_title="Gestione Cantieri", layout="centered", initial_sidebar_state="collapsed")

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

# Funzione per spostare un mezzo al cantiere di destinazione
def sposta_mezzo(cantieri_df, id_mezzo, cantiere_destinazione):
    # Rimuovi il mezzo da tutti i cantieri
    for index, row in cantieri_df.iterrows():
        mezzi_ids = row["mezzi_assegnati"]
        if pd.isna(mezzi_ids) or mezzi_ids == "":
            mezzi_ids = []
        else:
            mezzi_ids = mezzi_ids.split(",")

        if id_mezzo in mezzi_ids:
            mezzi_ids.remove(id_mezzo)
            cantieri_df.at[index, "mezzi_assegnati"] = ",".join(mezzi_ids)

    # Aggiungi il mezzo al cantiere di destinazione
    mezzi_ids = cantieri_df.loc[cantieri_df["id_cantiere"] == cantiere_destinazione, "mezzi_assegnati"].values[0]
    if pd.isna(mezzi_ids) or mezzi_ids == "":
        mezzi_ids = []
    else:
        mezzi_ids = mezzi_ids.split(",")

    if id_mezzo not in mezzi_ids:
        mezzi_ids.append(id_mezzo)
        cantieri_df.loc[cantieri_df["id_cantiere"] == cantiere_destinazione, "mezzi_assegnati"] = ",".join(mezzi_ids)

    salva_cantieri(cantieri_df)
    st.success(f"✅ Mezzo '{id_mezzo}' spostato al cantiere '{cantiere_destinazione}'.")
    st.session_state.clear()

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
        st.session_state.clear()
    except Exception as e:
        st.error(f"Errore durante l'aggiunta del cantiere: {e}")

# Carica i dati
mezzi_df, cantieri_df = carica_dati()

# Menu di Navigazione
st.sidebar.markdown("### 📋 Menu di Navigazione")
if st.sidebar.button("🏠 Home"):
    st.session_state["pagina"] = "Home"
if st.sidebar.button("🔄 Gestione Mezzi"):
    st.session_state["pagina"] = "Gestione Mezzi"
if st.sidebar.button("🏗️ Gestione Cantieri"):
    st.session_state["pagina"] = "Gestione Cantieri"

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "Home"

# Pagina Home
if st.session_state["pagina"] == "Home":
    st.title("🏗️ Cantieri Attivi")
    cantieri_aperti = cantieri_df[cantieri_df["stato"] == "Aperto"]

    if cantieri_aperti.empty:
        st.info("Non ci 

