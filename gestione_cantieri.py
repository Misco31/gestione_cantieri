import streamlit as st
import pandas as pd

# Configurazione per dispositivi mobili
st.set_page_config(page_title="Gestione Cantieri", layout="centered", initial_sidebar_state="collapsed")

# Funzione per caricare i dati dai file CSV
def carica_dati():
    try:
        mezzi_df = pd.read_csv("mezzi.csv", dtype=str)
        cantieri_df = pd.read_csv("cantieri.csv", dtype=str)
        st.write("Dati caricati con successo.")
        return mezzi_df, cantieri_df
    except Exception as e:
        st.error(f"Errore nel caricamento dei file CSV: {e}")
        st.stop()

# Funzione per salvare il file CSV aggiornato
def salva_cantieri(cantieri_df):
    try:
        cantieri_df.to_csv("cantieri.csv", index=False)
        st.write("Dati salvati correttamente.")
    except Exception as e:
        st.error(f"Errore nel salvataggio del file CSV: {e}")

# Funzione per mostrare i mezzi assegnati a un cantiere
def mostra_mezzi_assegnati(cantieri_df, mezzi_df, id_cantiere):
    if "mezzi_assegnati" not in cantieri_df.columns:
        st.error("Colonna 'mezzi_assegnati' non trovata.")
        return pd.DataFrame(columns=["ID", "Nome"])
    mezzi_ids = cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "mezzi_assegnati"].values
    if len(mezzi_ids) == 0 or pd.isna(mezzi_ids[0]) or mezzi_ids[0] == "":
        return pd.DataFrame(columns=["ID", "Nome"])
    mezzi_ids = mezzi_ids[0].split(",")
    mezzi_assegnati = mezzi_df[mezzi_df["ID"].isin(mezzi_ids)]
    return mezzi_assegnati[["ID", "Nome"]]

# Funzione per aggiungere un mezzo a un cantiere
def aggiungi_mezzo(cantieri_df, id_cantiere, id_mezzo):
    try:
        mezzi_ids = cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "mezzi_assegnati"].values[0]
        if pd.isna(mezzi_ids) or mezzi_ids == "":
            mezzi_ids = []
        else:
            mezzi_ids = mezzi_ids.split(",")
        if id_mezzo not in mezzi_ids:
            mezzi_ids.append(id_mezzo)
            cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "mezzi_assegnati"] = ",".join(mezzi_ids)
            salva_cantieri(cantieri_df)
            st.success(f"✅ Mezzo '{id_mezzo}' aggiunto con successo!")
            st.session_state.clear()  # Ricarica la pagina
    except Exception as e:
        st.error(f"Errore durante l'aggiunta del mezzo: {e}")

# Funzione per rimuovere un mezzo da un cantiere
def rimuovi_mezzo(cantieri_df, id_cantiere, id_mezzo):
    try:
        mezzi_ids = cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "mezzi_assegnati"].values[0]
        if pd.isna(mezzi_ids) or mezzi_ids == "":
            return
        mezzi_ids = mezzi_ids.split(",")
        if id_mezzo in mezzi_ids:
            mezzi_ids.remove(id_mezzo)
            cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "mezzi_assegnati"] = ",".join(mezzi_ids)
            salva_cantieri(cantieri_df)
            st.success(f"❌ Mezzo '{id_mezzo}' rimosso con successo!")
            st.session_state.clear()  # Ricarica la pagina
    except Exception as e:
        st.error(f"Errore durante la rimozione del mezzo: {e}")

# Carica i dati
mezzi_df, cantieri_df = carica_dati()

# Verifica che i DataFrame non siano vuoti
if mezzi_df.empty:
    st.warning("Il file 'mezzi.csv' è vuoto. Aggiungi almeno un mezzo.")
    st.stop()

if cantieri_df.empty:
    st.warning("Il file 'cantieri.csv' è vuoto. Aggiungi almeno un cantiere.")
    st.stop()

# Interfaccia Mobile-Friendly
st.title("🚧 Gestione Cantieri e Mezzi 🛠️")

# Selezione del cantiere
cantieri_aperti = cantieri_df[cantieri_df["stato"] == "Aperto"]
cantiere_selezionato = st.selectbox("🏗️ Seleziona il cantiere", cantieri_aperti["id_cantiere"].tolist(), format_func=lambda x: cantieri_df[cantieri_df["id_cantiere"] == x]["nome_cantiere"].values[0])

# Visualizzazione dei mezzi assegnati
st.subheader("🚜 Mezzi Assegnati")
mezzi_assegnati_df = mostra_mezzi_assegnati(cantieri_df, mezzi_df, cantiere_selezionato)
if not mezzi_assegnati_df.empty:
    st.table(mezzi_assegnati_df)
else:
    st.info("Nessun mezzo assegnato a questo cantiere.")

# Aggiunta di un mezzo al cantiere
st.subheader("➕ Aggiungi Mezzo")
categoria_mezzo = st.selectbox("🗂️ Categoria del mezzo", mezzi_df["Categoria"].unique())
mezzi_filtrati = mezzi_df[mezzi_df["Categoria"] == categoria_mezzo]
mezzo_selezionato = st.selectbox("🚜 Seleziona il mezzo", mezzi_filtrati.apply(lambda x: f"{x['ID']} - {x['Nome']}", axis=1).tolist())
id_mezzo = mezzo_selezionato.split(" - ")[0]

if st.button("Aggiungi Mezzo"):
    aggiungi_mezzo(cantieri_df, cantiere_selezionato, id_mezzo)

# Rimozione di un mezzo dal cantiere
st.subheader("➖ Rimuovi Mezzo")
if not mezzi_assegnati_df.empty:
    mezzo_da_rimuovere = st.selectbox("🚜 Seleziona il mezzo da rimuovere", mezzi_assegnati_df.apply(lambda x: f"{x['ID']} - {x['Nome']}", axis=1).tolist())
    id_mezzo_rimuovere = mezzo_da_rimuovere.split(" - ")[0]

    if st.button("Rimuovi Mezzo"):
        rimuovi_mezzo(cantieri_df, cantiere_selezionato, id_mezzo_rimuovere)

