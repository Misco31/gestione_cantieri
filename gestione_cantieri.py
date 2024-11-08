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

# Funzione per mostrare i mezzi assegnati a un cantiere
def mostra_mezzi_assegnati(cantieri_df, mezzi_df, id_cantiere):
    mezzi_ids = cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "mezzi_assegnati"].values
    if len(mezzi_ids) == 0 or pd.isna(mezzi_ids[0]) or mezzi_ids[0] == "":
        return []
    mezzi_ids = mezzi_ids[0].split(",")
    mezzi_assegnati = mezzi_df[mezzi_df["ID"].isin(mezzi_ids)]
    return mezzi_assegnati[["ID", "Nome"]].to_dict(orient="records")

# Funzione per ottenere l'elenco dei mezzi non assegnati
def mezzi_non_assegnati(cantieri_df, mezzi_df):
    mezzi_assegnati = set()
    for mezzi in cantieri_df["mezzi_assegnati"].dropna():
        mezzi_assegnati.update(mezzi.split(","))
    mezzi_non_assegnati = mezzi_df[~mezzi_df["ID"].isin(mezzi_assegnati)]
    return mezzi_non_assegnati

# Funzione per assegnare un mezzo a un cantiere
def assegna_mezzo(cantieri_df, id_mezzo, id_cantiere):
    mezzi_ids = cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "mezzi_assegnati"].values[0]
    if pd.isna(mezzi_ids) or mezzi_ids == "":
        mezzi_ids = []
    else:
        mezzi_ids = mezzi_ids.split(",")
    if id_mezzo not in mezzi_ids:
        mezzi_ids.append(id_mezzo)
        cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "mezzi_assegnati"] = ",".join(mezzi_ids)
        salva_cantieri(cantieri_df)
        st.success(f"✅ Mezzo '{id_mezzo}' assegnato al cantiere '{id_cantiere}'.")

# Funzione per spostare un mezzo tra cantieri
def sposta_mezzo(cantieri_df, id_mezzo, cantiere_attuale, cantiere_destinazione):
    # Rimuovi il mezzo dal cantiere attuale
    mezzi_ids = cantieri_df.loc[cantieri_df["id_cantiere"] == cantiere_attuale, "mezzi_assegnati"].values[0]
    if pd.isna(mezzi_ids) or mezzi_ids == "":
        mezzi_ids = []
    else:
        mezzi_ids = mezzi_ids.split(",")
    if id_mezzo in mezzi_ids:
        mezzi_ids.remove(id_mezzo)
        cantieri_df.loc[cantieri_df["id_cantiere"] == cantiere_attuale, "mezzi_assegnati"] = ",".join(mezzi_ids)

    # Aggiungi il mezzo al cantiere di destinazione
    assegna_mezzo(cantieri_df, id_mezzo, cantiere_destinazione)
    st.success(f"✅ Mezzo '{id_mezzo}' spostato da '{cantiere_attuale}' a '{cantiere_destinazione}'.")

# Carica i dati
mezzi_df, cantieri_df = carica_dati()

# Menu di Navigazione User-Friendly con pulsanti
st.sidebar.markdown("### 📋 Menu di Navigazione")
if st.sidebar.button("🏠 Home"):
    st.session_state["pagina"] = "Home"
if st.sidebar.button("🔄 Gestione Mezzi"):
    st.session_state["pagina"] = "Gestione Mezzi"
if st.sidebar.button("🏗️ Cantieri"):
    st.session_state["pagina"] = "Cantieri"

# Imposta la pagina iniziale
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "Home"

# Pagina Home
if st.session_state["pagina"] == "Home":
    st.title("🏗️ Cantieri Attivi")
    cantieri_aperti = cantieri_df[cantieri_df["stato"] == "Aperto"]

    if cantieri_aperti.empty:
        st.info("Non ci sono cantieri attivi.")
    else:
        for _, cantiere in cantieri_aperti.iterrows():
            st.markdown(f"📍 **{cantiere['nome_cantiere']}**")
            mezzi_assegnati = mostra_mezzi_assegnati(cantieri_df, mezzi_df, cantiere["id_cantiere"])

            if not mezzi_assegnati:
                st.markdown("*Nessun mezzo assegnato.*")
            else:
                for mezzo in mezzi_assegnati:
                    st.markdown(f"- 🚜 **{mezzo['ID']} - {mezzo['Nome']}**")

            st.markdown("---")

# Pagina Gestione Mezzi
elif st.session_state["pagina"] == "Gestione Mezzi":
    st.title("🔄 Gestione Mezzi")

    st.subheader("🚜 Assegna Mezzi Non Assegnati")
    mezzi_non_assegnati_df = mezzi_non_assegnati(cantieri_df, mezzi_df)
    if mezzi_non_assegnati_df.empty:
        st.info("Tutti i mezzi sono assegnati.")
    else:
        mezzo_da_assegnare = st.selectbox("Seleziona un mezzo non assegnato", mezzi_non_assegnati_df["ID"].tolist())
        cantiere_destinazione = st.selectbox("Assegna a cantiere", cantieri_df["id_cantiere"].tolist())
        if st.button("Assegna Mezzo"):
            assegna_mezzo(cantieri_df, mezzo_da_assegnare, cantiere_destinazione)

    st.subheader("🔁 Sposta Mezzi tra Cantieri")
    mezzo_da_spostare = st.selectbox("Seleziona un mezzo da spostare", mezzi_df["ID"].tolist())
    cantiere_attuale = st.selectbox("Cantiere Attuale", cantieri_df["id_cantiere"].tolist())
    cantiere_destinazione = st.selectbox("Cantiere Destinazione", cantieri_df["id_cantiere"].tolist())
    if st.button("Sposta Mezzo"):
        sposta_mezzo(cantieri_df, mezzo_da_spostare, cantiere_attuale, cantiere_destinazione)

