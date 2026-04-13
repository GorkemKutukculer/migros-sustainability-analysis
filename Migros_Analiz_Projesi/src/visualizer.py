import plotly.express as px

def plot_hizmet_endeksi(df):
    return px.bar(df, x='Ilce', y='Hizmet_Indeksi', 
                  title="1. İlçe Bazlı Hizmet Endeksi (100 Bin Kişiye Düşen Nokta)",
                  labels={'Hizmet_Indeksi': 'Hizmet Endeksi', 'Ilce': 'İlçeler'},
                  color='Hizmet_Indeksi', color_continuous_scale='Reds_r')

def plot_nokta_sayisi(df):
    return px.bar(df.sort_values('Atik_Yag_Noktasi_Sayisi', ascending=False), 
                  x='Ilce', y='Atik_Yag_Noktasi_Sayisi',
                  title="2. İlçelere Göre Toplam Atık Yağ Noktası",
                  labels={'Atik_Yag_Noktasi_Sayisi': 'Mağaza Sayısı'})

def plot_nufus_iliskisi(df):
    return px.scatter(df, x='Nufus', y='Atik_Yag_Noktasi_Sayisi', 
                      hover_name='Ilce', size='Nufus', color='Hizmet_Indeksi',
                      title="3. Nüfus Büyüklüğü ve Nokta Sayısı İlişkisi",
                      labels={'Atik_Yag_Noktasi_Sayisi': 'Nokta Sayısı', 'Nufus': 'Nüfus'})