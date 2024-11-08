import streamlit as st
import pandas as pd

# Configurazione dell'app per dispositivi mobili
st.set_page_config(page_title="Gestione Cantieri", layout="centered")

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

# Layout per i bottoni di navigazione
st.markdown(
    """
    <style>
    .nav-bar {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 20px;
    }
    .nav-button {
        font-size: 18px;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s;
        background-color: #e0e0e0;
    }
    .nav-button:hover {
        background-color: #d0d0d0;
    }
    </style>
    <div class="nav-bar">
        <button class="nav-button" onclick="window.location.href='/?pagina=Home'">🏠 Home</button>
        <button class="nav-button" onclick="window.location.href='/?pagina=Gestione_Mezzi'">🔄 Sposta</button>
        <button class="nav-button" onclick="window.location.href='/?pagina=Gestione_Cantieri'">🏗️ Aggiungi</button>
    </div>
    """,
    unsafe_allow_html=True
)

# Controllo dello stato della pagina
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "Home"

if st.experimental_get_query_params().get("pagina"):
    st.session_state["pagina"] = st.experimental_get_query_params().get("pagina")[0]

# Pagina Home
if st.session_state["pagina"] == "Home":
    st.title("🏗️ Cantieri Attivi")
    st.write("Benvenuto nella pagina Home.")

# Pagina Gestione Mezzi
elif st.session_state["pagina"] == "Gestione_Mezzi":
    st.title("🔄 Sposta Mezzo")
    st.write("Benvenuto nella pagina di gestione dei mezzi.")

# Pagina Gestione Cantieri
elif st.session_state["pagina"] == "Gestione_Cantieri":
    st.title("🏗️ Gestione Cantieri")
    st.write("Benvenuto nella pagina di gestione dei cantieri.")
