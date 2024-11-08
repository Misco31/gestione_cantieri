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
    st.success(f"✅ Mezzo '{id_mezzo}' spostato correttamente al cantiere '{cantiere_destinazione}'.")
    st.session_state["pagina"] = "Home"

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
        st.session_state["pagina"] = "Home"
    except Exception as e:
        st.error(f"Errore durante l'aggiunta del cantiere: {e}")

# Funzione per chiudere un cantiere
def chiudi_cantiere(cantieri_df, id_cantiere):
    cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "stato"] = "Chiuso"
    salva_cantieri(cantieri_df)
    st.success(f"✅ Cantiere '{id_cantiere}' chiuso correttamente.")
    st.session_state["pagina"] = "Home"

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

# Layout per i bottoni di navigazione con sole icone ingrandite
st.markdown(
    """
    <style>
    .nav-bar {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-bottom: 20px;
    }
    .nav-button {
        font-size: 40px;
        padding: 10px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        background-color: #e0e0e0;
        transition: background-color 0.3s;
    }
    .nav-button:hover {
        background-color: #d0d0d0;
    }
    </style>
    <div class="nav-bar">
        <button class="nav-button" onclick="window.location.href='/?pagina=Home'">🏠</button>
        <button class="nav-button" onclick="window.location.href='/?pagina=Gestione_Mezzi'">🔄</button>
        <button class="nav-button" onclick="window.location.href='/?pagina=Gestione_Cantieri'">🏗️</button>
    </div>
    """,
    unsafe_allow_html=True
)

# Controllo dello stato della pagina
if st.experimental_get_query_params().get("pagina"):
    st.session_state["pagina"] = st.experimental_get_query_params().get("pagina")[0]

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
elif st.session_state["pagina"] == "Gestione_Mezzi":
    st.title("🔄 Sposta Mezzo")
    mezzo_selezionato = st.selectbox("Seleziona Mezzo", mezzi_df["ID"].tolist(), format_func=lambda x: f"{x} - {mezzi_df[mezzi_df['ID'] == x]['Nome'].values[0]}")
    cantiere_destinazione = st.selectbox("Cantiere di Destinazione", cantieri_df["id_cantiere"].tolist(), format_func=lambda x: cantieri_df[cantieri_df["id_cantiere"] == x]["nome_cantiere"].values[0])

    if st.button("Sposta Mezzo"):
        sposta_mezzo(cantieri_df, mezzo_selezionato, cantiere_destinazione)

# Pagina Gestione Cantieri
elif st.session_state["pagina"] == "Gestione_Cantieri":
    st.title("🏗️ Gestione Cantieri")
    nome_nuovo_cantiere = st.text_input("Nome del nuovo cantiere")
    if st.button("Aggiungi Cantiere") and nome_nuovo_cantiere:
        aggiungi_cantiere(cantieri_df, nome_nuovo_cantiere)

    cantiere_da_chiudere = st.selectbox("Seleziona Cantiere da Chiudere", cantieri_df[cantieri_df["stato"] == "Aperto"]["id_cantiere"].tolist(), format_func=lambda x: cantieri_df[cantieri_df["id_cantiere"] == x]["nome_cantiere"].values[0])
    if st.button("Chiudi Cantiere"):
        chiudi_cantiere(cantieri_df, cantiere_da_chiudere)

