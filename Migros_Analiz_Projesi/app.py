import streamlit as st

from src.data_collector import fetch_nufus_data, fetch_migros_data
from src.data_cleaner import clean_migros_data
from src.analyzer import analyze_data
from src.excel_report import create_excel_report
from src.visualizer import plot_hizmet_endeksi, plot_nokta_sayisi, plot_nufus_iliskisi

st.set_page_config(page_title="Migros Hizmet Boşluğu Analizi", layout="wide")

st.title("🌱 Migros Çevresel Sürdürülebilirlik Analizi")
st.markdown("""
Bu proje, **İstanbul ilçe nüfusları** ile **Migros bitkisel atık yağ toplama noktalarını** karşılaştırarak çevresel hizmet boşluklarını tespit etmeyi amaçlamaktadır. Nüfus verileri Web scraping ile dinamik olarak çekilmektedir.
""")

pdf_dosya_yolu = "data/migros türkiye mağaza listesi.pdf"

with st.spinner('Veriler toplanıyor ve analiz ediliyor...'):
    df_nufus_ham = fetch_nufus_data()
    df_migros_ham = fetch_migros_data(pdf_dosya_yolu)
    
    df_migros_temiz = clean_migros_data(df_migros_ham)
    df_final = analyze_data(df_migros_temiz, df_nufus_ham)

if df_final is not None:
    df_ekran = df_final[['Ilce', 'Atik_Yag_Noktasi_Sayisi', 'Nufus', 'Hizmet_Indeksi']].copy()
    
    st.subheader("📊 Analiz Tablosu")
    st.dataframe(df_ekran.style.format({'Nufus': '{:,}', 'Hizmet_Indeksi': '{:.2f}'}), use_container_width=True)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        csv_veri = df_ekran.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Veriyi CSV Olarak İndir",
            data=csv_veri,
            file_name='migros_hizmet_boslugu.csv',
            mime='text/csv'
        )
    with col_btn2:
        excel_veri = create_excel_report(df_final)
        st.download_button(
            label="Gelişmiş Excel Raporu İndir",
            data=excel_veri,
            file_name='Migros_Detayli_Analiz_Raporu.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    st.divider()
    st.subheader("📈 Veri Görselleştirmeleri")
    
    st.plotly_chart(plot_hizmet_endeksi(df_ekran), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_nokta_sayisi(df_ekran), use_container_width=True)
        
    with col2:
        st.plotly_chart(plot_nufus_iliskisi(df_ekran), use_container_width=True)

else:
    st.warning("Veriler çekilemediği için analiz gerçekleştirilemiyor. Lütfen PDF dosyasının adını ve konumunu kontrol edin.")