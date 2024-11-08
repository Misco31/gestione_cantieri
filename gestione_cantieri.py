import streamlit as st
import pandas as pd

# Funzione per caricare i dati dai file CSV
def carica_dati():
    try:
        mezzi_df = pd.read_csv("mezzi.csv")
        cantieri_df = pd.read_csv("cantieri.csv")
        return mezzi_df, cantieri_df
    except Exception as e:
        st.error(f"Errore nel caricamento dei file CSV: {e}")
        st.stop()

# Funzione per salvare il file CSV aggiornato
def salva_cantieri(cantieri_df):
    cantieri_df.to_csv("cantieri.csv", index=False)

# Funzione per mostrare i mezzi assegnati a un cantiere
def mostra_mezzi_assegnati(cantieri_df, mezzi_df, id_cantiere):
    mezzi_ids = cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "mezzi_assegnati"].values
    if len(mezzi_ids) == 0 or pd.isna(mezzi_ids[0]) or mezzi_ids[0] == "":
        return pd.DataFrame(columns=["ID", "Nome", "Categoria"])
    mezzi_ids = mezzi_ids[0].split(",")
    return mezzi_df[mezzi_df["ID"].isin(mezzi_ids)]

# Funzione per aggiungere un mezzo a un cantiere
def aggiungi_mezzo(cantieri_df, id_cantiere, id_mezzo):
    mezzi_ids = cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "mezzi_assegnati"].values[0]
    if pd.isna(mezzi_ids) or mezzi_ids == "":
        mezzi_ids = []
    else:
        mezzi_ids = mezzi_ids.split(",")
    if id_mezzo not in mezzi_ids:
        mezzi_ids.append(id_mezzo)
        cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "mezzi_assegnati"] = ",".join(mezzi_ids)
        salva_cantieri(cantieri_df)

# Funzione per rimuovere un mezzo da un cantiere
def rimuovi_mezzo(cantieri_df, id_cantiere, id_mezzo):
    mezzi_ids = cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "mezzi_assegnati"].values[0]
    if pd.isna(mezzi_ids) or mezzi_ids == "":
        return
    mezzi_ids = mezzi_ids.split(",")
    if id_mezzo in mezzi_ids:
        mezzi_ids.remove(id_mezzo)
        cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "mezzi_assegnati"] = ",".join(mezzi_ids)
        salva_cantieri(cantieri_df)

# Funzione per chiudere un cantiere
def chiudi_cantiere(cantieri_df, id_cantiere):
    cantieri_df.loc[cantieri_df["id_cantiere"] == id_cantiere, "stato"] = "Chiuso"
    salva_cantieri(cantieri_df)

# Funzione per aggiungere un nuovo cantiere
def aggiungi_cantiere(cantieri_df, nome):
    nuovo_id = cantieri_df["id_cantiere"].max() + 1 if not cantieri_df.empty else 1
    cantieri_df.loc[len(cantieri_df)] = [nuovo_id, nome, "Aperto", ""]
    salva_cantieri(cantieri_df)

# Carica i dati
mezzi_df, cantieri_df = carica_dati()

# Verifica che i DataFrame non siano vuoti
if mezzi_df.empty:
    st.warning("Il file 'mezzi.csv' è vuoto. Aggiungi almeno un mezzo.")
    st.stop()

if cantieri_df.empty:
    st.warning("Il file 'cantieri.csv' è vuoto. Aggiungi almeno un cantiere.")
    st.stop()

# Interfaccia Streamlit
st.title("Gestione Cantieri e Mezzi")

# Filtra i cantieri aperti
cantieri_aperti = cantieri_df[cantieri_df["stato"] == "Aperto"]
if cantieri_aperti.empty:
    st.warning("Non ci sono cantieri aperti.")
    st.stop()

cantiere_selezionato = st.selectbox("Seleziona il cantiere", cantieri_aperti["id_cantiere"].tolist(), format_func=lambda x: cantieri_df[cantieri_df["id_cantiere"] == x]["nome_cantiere"].values[0])

st.header(f"Cantiere: {cantieri_df[cantieri_df['id_cantiere'] == cantiere_selezionato]['nome_cantiere'].values[0]}")

# Visualizzazione dei mezzi assegnati
st.subheader("Mezzi Assegnati")
mezzi_assegnati_df = mostra_mezzi_assegnati(cantieri_df, mezzi_df, cantiere_selezionato)
st.table(mezzi_assegnati_df)

# Aggiunta di un mezzo al cantiere
st.subheader("Aggiungi Mezzo")
categoria_mezzo = st.selectbox("Seleziona la categoria del mezzo", mezzi_df["Categoria"].unique())
mezzi_filtrati = mezzi_df[mezzi_df["Categoria"] == categoria_mezzo]
mezzo_da_aggiungere = st.selectbox("Seleziona il mezzo da aggiungere", mezzi_filtrati["ID"].tolist(), format_func=lambda x: mezzi_df[mezzi_df["ID"] == x]["Nome"].values[0])
if st.button("Aggiungi Mezzo"):
    aggiungi_mezzo(cantieri_df, cantiere_selezionato, mezzo_da_aggiungere)
    st.success("Mezzo aggiunto con successo!")

# Rimozione di un mezzo dal cantiere
st.subheader("Rimuovi Mezzo")
if not mezzi_assegnati_df.empty:
    mezzo_da_rimuovere = st.selectbox("Seleziona il mezzo da rimuovere", mezzi_assegnati_df["ID"].tolist(), format_func=lambda x: mezzi_df[mezzi_df["ID"] == x]["Nome"].values[0])
    if st.button("Rimuovi Mezzo"):
        rimuovi_mezzo(cantieri_df, cantiere_selezionato, mezzo_da_rimuovere)
        st.success("Mezzo rimosso con successo!")
else:
    st.warning("Non ci sono mezzi assegnati da rimuovere.")

# Opzione per chiudere il cantiere
if st.button("Chiudi Cantiere"):
    chiudi_cantiere(cantieri_df, cantiere_selezionato)
    st.success("Cantiere chiuso con successo!")

# Aggiunta di un nuovo cantiere
st.subheader("Aggiungi Nuovo Cantiere")
nome_nuovo_cantiere = st.text_input("Nome del nuovo cantiere")
if st.button("Aggiungi Cantiere") and nome_nuovo_cantiere:
    aggiungi_cantiere(cantieri_df, nome_nuovo_cantiere)
    st.success(f"Cantiere '{nome_nuovo_cantiere}' aggiunto con successo!")

