import streamlit as st
import pandas as pd

# Database temporaneo per i cantieri e i mezzi
cantieri = pd.DataFrame({
    "id_cantiere": [1, 2, 3],
    "nome_cantiere": ["Cantiere Centro", "Cantiere Nord", "Cantiere Sud"],
    "stato": ["Aperto", "Aperto", "Aperto"],
})

mezzi = pd.DataFrame({
    "id_mezzo": [101, 102, 103, 104],
    "nome_mezzo": ["Escavatore 1", "Pala Gommata", "Autocarro 1", "Rullo Compattatore"],
})

# Database temporaneo per assegnazione mezzi ai cantieri
assegnazioni = {
    1: [101, 102],  # Mezzi assegnati al Cantiere Centro
    2: [103],       # Mezzi assegnati al Cantiere Nord
    3: []           # Nessun mezzo assegnato al Cantiere Sud
}

# Funzione per visualizzare la lista dei mezzi assegnati
def mostra_mezzi_assegnati(id_cantiere):
    mezzi_assegnati = [mezzo for mezzo in mezzi.itertuples() if mezzo.id_mezzo in assegnazioni[id_cantiere]]
    return pd.DataFrame(mezzi_assegnati, columns=["id_mezzo", "nome_mezzo"])

# Funzione per aggiungere un mezzo al cantiere
def aggiungi_mezzo(id_cantiere, id_mezzo):
    if id_mezzo not in assegnazioni[id_cantiere]:
        assegnazioni[id_cantiere].append(id_mezzo)

# Funzione per rimuovere un mezzo dal cantiere
def rimuovi_mezzo(id_cantiere, id_mezzo):
    if id_mezzo in assegnazioni[id_cantiere]:
        assegnazioni[id_cantiere].remove(id_mezzo)

# Funzione per aggiungere un nuovo cantiere
def aggiungi_cantiere(nome):
    nuovo_id = cantieri["id_cantiere"].max() + 1
    cantieri.loc[len(cantieri)] = [nuovo_id, nome, "Aperto"]
    assegnazioni[nuovo_id] = []

# Funzione per chiudere un cantiere
def chiudi_cantiere(id_cantiere):
    cantieri.loc[cantieri["id_cantiere"] == id_cantiere, "stato"] = "Chiuso"

# Interfaccia Streamlit
st.title("Gestione Cantieri e Mezzi")

# Selezione del cantiere
cantieri_aperti = cantieri[cantieri["stato"] == "Aperto"]
cantiere_selezionato = st.selectbox("Seleziona il cantiere", cantieri_aperti["id_cantiere"].tolist(), format_func=lambda x: cantieri[cantieri["id_cantiere"] == x]["nome_cantiere"].values[0])

st.header(f"Cantiere: {cantieri[cantieri['id_cantiere'] == cantiere_selezionato]['nome_cantiere'].values[0]}")

# Visualizzazione dei mezzi assegnati
st.subheader("Mezzi Assegnati")
mezzi_assegnati_df = mostra_mezzi_assegnati(cantiere_selezionato)
st.table(mezzi_assegnati_df)

# Aggiunta di un mezzo al cantiere
st.subheader("Aggiungi Mezzo")
mezzo_da_aggiungere = st.selectbox("Seleziona il mezzo da aggiungere", mezzi["id_mezzo"].tolist(), format_func=lambda x: mezzi[mezzi["id_mezzo"] == x]["nome_mezzo"].values[0])
if st.button("Aggiungi Mezzo"):
    aggiungi_mezzo(cantiere_selezionato, mezzo_da_aggiungere)
    st.success("Mezzo aggiunto con successo!")

# Rimozione di un mezzo dal cantiere
st.subheader("Rimuovi Mezzo")
if not mezzi_assegnati_df.empty:
    mezzo_da_rimuovere = st.selectbox("Seleziona il mezzo da rimuovere", mezzi_assegnati_df["id_mezzo"].tolist(), format_func=lambda x: mezzi[mezzi["id_mezzo"] == x]["nome_mezzo"].values[0])
    if st.button("Rimuovi Mezzo"):
        rimuovi_mezzo(cantiere_selezionato, mezzo_da_rimuovere)
        st.success("Mezzo rimosso con successo!")
else:
    st.warning("Non ci sono mezzi assegnati da rimuovere.")

# Opzione per chiudere il cantiere
if st.button("Chiudi Cantiere"):
    chiudi_cantiere(cantiere_selezionato)
    st.success("Cantiere chiuso con successo!")

# Aggiunta di un nuovo cantiere
st.subheader("Aggiungi Nuovo Cantiere")
nome_nuovo_cantiere = st.text_input("Nome del nuovo cantiere")
if st.button("Aggiungi Cantiere") and nome_nuovo_cantiere:
    aggiungi_cantiere(nome_nuovo_cantiere)
    st.success(f"Cantiere '{nome_nuovo_cantiere}' aggiunto con successo!")

# Aggiornamento visualizzazione
st.experimental_rerun()

