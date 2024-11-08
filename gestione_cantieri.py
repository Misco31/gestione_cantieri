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
        st.success("Dati salvati correttamente.")
    except Exception as e:
        st.error(f"Errore durante il salvataggio dei dati: {e}")

# Funzione per spostare un mezzo
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
    st.success(f"✅ Mezzo '{id_mezzo}' spostato correttamente al cantiere '{cantiere_destinazione}'.")

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
    st.success(f"✅ Cantiere '{id_cantiere}' chiuso correttamente.")

# Carica i dati
mezzi_df, cantieri_df = carica_dati()

# Imposta la pagina iniziale se non è già definita
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "Home"

# Menu laterale fisso
with st.sidebar:
    st.title("Menu di Navigazione")
    if st.button("🏠 Home", key="home"):
        st.session_state["pagina"] = "Home"

    if st.button("🔄 Sposta", key="sposta"):
        st.session_state["pagina"] = "Gestione_Mezzi"

    if st.button("🏗️ Aggiungi", key="aggiungi"):
        st.session_state["pagina"] = "Gestione_Cantieri"

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
