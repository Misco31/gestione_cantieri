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

# Funzione per salvare i dati aggiornati
def salva_cantieri(cantieri_df):
    try:
        cantieri_df.to_csv("cantieri.csv", index=False)
    except Exception as e:
        st.error(f"Errore nel salvataggio del file CSV: {e}")

# Funzione per cambiare pagina
def naviga(pagina):
    st.session_state["pagina"] = pagina

# Carica i dati
mezzi_df, cantieri_df = carica_dati()

# Verifica se i dataframe sono vuoti
if cantieri_df.empty:
    st.warning("Il file 'cantieri.csv' è vuoto o non contiene dati validi.")
    st.stop()

if mezzi_df.empty:
    st.warning("Il file 'mezzi.csv' è vuoto o non contiene dati validi.")
    st.stop()

# Imposta la pagina iniziale se non è già definita
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "Home"

# Menu laterale fisso
with st.sidebar:
    st.title("Menu di Navigazione")
    if st.button("🏠 Home", key="home"):
        naviga("Home")

    if st.button("🔄 Sposta", key="sposta"):
        naviga("Gestione_Mezzi")

    if st.button("🏗️ Aggiungi", key="aggiungi"):
        naviga("Gestione_Cantieri")

# Controllo dello stato della pagina
pagina = st.session_state.get("pagina", "Home")

# Pagina Home
if pagina == "Home":
    st.title("🏗️ Cantieri Attivi")
    cantieri_aperti = cantieri_df[cantieri_df["stato"] == "Aperto"]

    if cantieri_aperti.empty:
        st.info("Non ci sono cantieri attivi.")
    else:
        for _, cantiere in cantieri_aperti.iterrows():
            st.markdown(f"📍 **{cantiere['nome_cantiere']}**")
            mezzi_assegnati = cantiere["mezzi_assegnati"]
            if pd.isna(mezzi_assegnati) or mezzi_assegnati == "":
                st.markdown("*Nessun mezzo assegnato.*")
            else:
                mezzi_assegnati = mezzi_assegnati.split(",")
                for mezzo_id in mezzi_assegnati:
                    nome_mezzo = mezzi_df[mezzi_df["ID"] == mezzo_id]["Nome"].values[0]
                    st.markdown(f"- 🚜 **{mezzo_id} - {nome_mezzo}**")

# Pagina Gestione Mezzi
elif pagina == "Gestione_Mezzi":
    st.title("🔄 Sposta Mezzo")
    mezzo_selezionato = st.selectbox("Seleziona Mezzo", mezzi_df["ID"].tolist(), format_func=lambda x: f"{x} - {mezzi_df[mezzi_df['ID'] == x]['Nome'].values[0]}")
    cantiere_destinazione = st.selectbox("Cantiere di Destinazione", cantieri_df["id_cantiere"].tolist(), format_func=lambda x: cantieri_df[cantieri_df["id_cantiere"] == x]["nome_cantiere"].values[0])

    if st.button("Sposta Mezzo"):
        sposta_mezzo(cantieri_df, mezzo_selezionato, cantiere_destinazione)

# Pagina Gestione Cantieri
elif pagina == "Gestione_Cantieri":
    st.title("🏗️ Gestione Cantieri")
    nome_nuovo_cantiere = st.text_input("Nome del nuovo cantiere")
    if st.button("Aggiungi Cantiere") and nome_nuovo_cantiere:
        aggiungi_cantiere(cantieri_df, nome_nuovo_cantiere)

    cantiere_da_chiudere = st.selectbox("Seleziona Cantiere da Chiudere", cantieri_df[cantieri_df["stato"] == "Aperto"]["id_cantiere"].tolist(), format_func=lambda x: cantieri_df[cantieri_df["id_cantiere"] == x]["nome_cantiere"].values[0])
    if st.button("Chiudi Cantiere"):
        chiudi_cantiere(cantieri_df, cantiere_da_chiudere)
