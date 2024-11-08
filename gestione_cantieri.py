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
        st.success(f"✅ Cantiere '{nome}' aggiunto con successo!")
    except Exception as e:
        st.error(f"Errore durante l'aggiunta del cantiere: {e}")

# Funzione per chiudere un cantiere
def chiudi_cantiere(cantieri_df, id_cantiere):
    cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "stato"] = "Chiuso"
    salva_cantieri(cantieri_df)
    st.success(f"✅ Cantiere '{id_cantiere}' chiuso con successo!")

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
elif st.session_state["pagina"] == "Gestione Mezzi":
    st.title("🔄 Sposta Mezzo")
    mezzo_selezionato = st.selectbox("Seleziona Mezzo", mezzi_df["ID"].tolist(), format_func=lambda x: f"{x} - {mezzi_df[mezzi_df['ID'] == x]['Nome'].values[0]}")
    cantiere_destinazione = st.selectbox("Cantiere di Destinazione", cantieri_df["id_cantiere"].tolist(), format_func=lambda x: cantieri_df[cantieri_df["id_cantiere"] == x]["nome_cantiere"].values[0])

    if st.button("Sposta Mezzo"):
        sposta_mezzo(cantieri_df, mezzo_selezionato, cantiere_destinazione)

# Pagina Gestione Cantieri
elif st.session_state["pagina"] == "Gestione Cantieri":
    st.title("🏗️ Gestione Cantieri")

    # Aggiungi un nuovo cantiere
    nome_nuovo_cantiere = st.text_input("Nome del nuovo cantiere")
    if st.button("Aggiungi Cantiere") and nome_nuovo_cantiere:
        aggiungi_cantiere(cantieri_df, nome_nuovo_cantiere)

    # Chiudi un cantiere esistente
    cantiere_da_chiudere = st.selectbox("Seleziona Cantiere da Chiudere", cantieri_df[cantieri_df["stato"] == "Aperto"]["id_cantiere"].tolist(), format_func=lambda x: cantieri_df[cantieri_df["id_cantiere"] == x]["nome_cantiere"].values[0])
    if st.button("Chiudi Cantiere"):
        chiudi_cantiere(cantieri_df, cantiere_da_chiudere)

