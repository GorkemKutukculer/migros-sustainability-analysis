import pandas as pd

def analyze_data(df_migros, df_nufus):
    if df_migros is None or df_nufus is None:
        return None
        
    df = pd.merge(df_migros, df_nufus, on="Ilce")
    df['Hizmet_Indeksi'] = (df['Atik_Yag_Noktasi_Sayisi'] / df['Nufus']) * 100000
    df['Nokta_Basina_Kisi'] = (df['Nufus'] / df['Atik_Yag_Noktasi_Sayisi']).round(0)
    
    df_final = df.sort_values(by='Hizmet_Indeksi').reset_index(drop=True)
    return df_final