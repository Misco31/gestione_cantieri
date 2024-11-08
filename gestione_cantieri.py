import streamlit as st
import pandas as pd

# Simulazione di dati per i cantieri e i mezzi
cantieri = pd.DataFrame({
    "id_cantiere": [1, 2, 3],
    "nome_cantiere": ["Cantiere Centro", "Cantiere Nord", "Cantiere Sud"],
})

mezzi = pd.DataFrame({
    "id_mezzo": [101, 102, 103, 104],
    "nome_mezzo": ["Escavatore 1", "Pala Gommata", "Autocarro 1", "Rullo Compattatore"],
})

# Database temporaneo per assegnazione mezzi ai cantieri
assegnazioni = {
    1: [101, 102],
    2: [103],
    3: []
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

# Interfaccia Streamlit
st.title("Gestione Cantieri e Mezzi")

# Selezione del cantiere
cantiere_selezionato = st.selectbox("Seleziona il cantiere", cantieri["id_cantiere"].tolist(), format_func=lambda x: cantieri[cantieri["id_cantiere"] == x]["nome_cantiere"].values[0])

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
mezzo_da_rimuovere = st.selectbox("Seleziona il mezzo da rimuovere", mezzi_assegnati_df["id_mezzo"].tolist() if not mezzi_assegnati_df.empty else [], format_func=lambda x: mezzi[mezzi["id_mezzo"] == x]["nome_mezzo"].values[0])
if st.button("Rimuovi Mezzo"):
    rimuovi_mezzo(cantiere_selezionato, mezzo_da_rimuovere)
    st.success("Mezzo rimosso con successo!")

# Aggiornamento visualizzazione
st.experimental_rerun()
