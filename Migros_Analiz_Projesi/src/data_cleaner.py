import pandas as pd

def ilce_temizle(adres):
    if not adres: return "DIGER"
    adr = str(adres).upper().replace('İ', 'I').replace('Ü', 'U').replace('Ö', 'O').replace('Ş', 'S').replace('Ç', 'C').replace('Ğ', 'G')
    
    if "MECIDIYEKOY" in adr: return "SISLI"
    if "BAHCESEHIR" in adr: return "BASAKSEHIR"
    if any(x in adr for x in ["G.OSMANPASA", "GAZI OSMAN PASA", "GOP "]): return "GAZIOSMANPASA"
    if "EYUP" in adr: return "EYUPSULTAN"
    if "CEKMEKOY" in adr: return "CEKMEKOY"
    if "K.CEKMECE" in adr: return "KUCUKCEKMECE"
    if "B.CEKMECE" in adr: return "BUYUKCEKMECE"

    ilceler = ["ADALAR", "ARNAVUTKOY", "ATASEHIR", "AVCILAR", "BAGCILAR", "BAHCELIEVLER", "BAKIRKOY", "BASAKSEHIR", "BAYRAMPASA", "BESIKTAS", "BEYKOZ", "BEYLIKDUZU", "BEYOGLU", "BUYUKCEKMECE", "CATALCA", "CEKMEKOY", "ESENLER", "ESENYURT", "EYUPSULTAN", "FATIH", "GAZIOSMANPASA", "GUNGOREN", "KADIKOY", "KAGITHANE", "KARTAL", "KUCUKCEKMECE", "MALTEPE", "PENDIK", "SANCAKTEPE", "SARIYER", "SILIVRI", "SULTANBEYLI", "SULTANGAZI", "SILE", "SISLI", "TUZLA", "UMRANIYE", "USKUDAR", "ZEYTINBURNU"]
    
    for ilce in ilceler:
        if ilce in adr:
            return ilce
    return "DIGER"

def clean_migros_data(raw_df):
    if raw_df is None: return None
    
    df_ist = raw_df[raw_df['Adres'].str.contains("İSTANBUL|ISTANBUL", case=False, na=False)].copy()
    df_ist['Ilce'] = df_ist['Adres'].apply(ilce_temizle)
    
    df_counts = df_ist[df_ist['Ilce'] != "DIGER"]['Ilce'].value_counts().reset_index()
    df_counts.columns = ['Ilce', 'Atik_Yag_Noktasi_Sayisi']
    return df_counts