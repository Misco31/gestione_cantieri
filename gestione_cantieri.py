# Funzione per spostare un mezzo al cantiere di destinazione
def sposta_mezzo(cantieri_df, id_mezzo, cantiere_destinazione):
    # Rimuove il mezzo dal cantiere precedente
    for index, row in cantieri_df.iterrows():
        mezzi_ids = row["mezzi_assegnati"]
        if pd.isna(mezzi_ids) or mezzi_ids == "":
            mezzi_ids = []
        else:
            mezzi_ids = mezzi_ids.split(",")

        if id_mezzo in mezzi_ids:
            mezzi_ids.remove(id_mezzo)
            cantieri_df.at[index, "mezzi_assegnati"] = ",".join(mezzi_ids)

    # Aggiunge il mezzo al cantiere di destinazione
    mezzi_ids = cantieri_df.loc[cantieri_df["id_cantiere"] == cantiere_destinazione, "mezzi_assegnati"].values[0]
    if pd.isna(mezzi_ids) or mezzi_ids == "":
        mezzi_ids = []
    else:
        mezzi_ids = mezzi_ids.split(",")

    if id_mezzo not in mezzi_ids:
        mezzi_ids.append(id_mezzo)
        cantieri_df.loc[cantieri_df["id_cantiere"] == cantiere_destinazione, "mezzi_assegnati"] = ",".join(mezzi_ids)

    # Ottiene il nome del cantiere di destinazione
    nome_cantiere = cantieri_df.loc[cantieri_df["id_cantiere"] == cantiere_destinazione, "nome_cantiere"].values[0]

    # Salva i dati e mostra il messaggio di successo
    salva_cantieri(cantieri_df)
    st.success(f"✅ Mezzo '{id_mezzo}' spostato correttamente al cantiere '{nome_cantiere}'.")



