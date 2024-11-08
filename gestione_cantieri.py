import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Autenticazione con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)

# Apri i fogli Google Sheets
spreadsheet = client.open("Gestione Cantieri")  # Inserisci il nome del tuo file Google Sheets
mezzi_sheet = spreadsheet.worksheet("mezzi")
cantieri_sheet = spreadsheet.worksheet("cantieri")

# Funzione per caricare i dati dai Google Sheets
def carica_dati():
    mezzi_df = pd.DataFrame(mezzi_sheet.get_all_records())
    cantieri_df = pd.DataFrame(cantieri_sheet.get_all_records())
    return mezzi_df, cantieri_df

# Funzione per salvare i dati nei Google Sheets
def salva_dati(mezzi_df, cantieri_df):
    mezzi_sheet.update([mezzi_df.columns.values.tolist()] + mezzi_df.values.tolist())
    cantieri_sheet.update([cantieri_df.columns.values.tolist()] + cantieri_df.values.tolist())

# Carica i dati dai fogli Google Sheets
mezzi_df, cantieri_df = carica_dati()

# Interfaccia Streamlit
st.title("Gestione Cantieri")

# Visualizza i dati
st.write("Mezzi:", mezzi_df)
st.write("Cantieri:", cantieri_df)

# Modifica i dati e salva
if st.button("Modifica Nome Mezzo"):
    if not mezzi_df.empty:
        mezzi_df.loc[0, "Nome"] = "Modificato"
        salva_dati(mezzi_df, cantieri_df)
        st.success("Dati salvati su Google Sheets!")

if st.button("Aggiungi Cantiere"):
    nuovo_cantiere = {"id_cantiere": len(cantieri_df) + 1, "nome_cantiere": "Nuovo Cantiere", "stato": "Aperto", "mezzi_assegnati": ""}
    cantieri_df = cantieri_df.append(nuovo_cantiere, ignore_index=True)
    salva_dati(mezzi_df, cantieri_df)
    st.success("Cantiere aggiunto correttamente!")

