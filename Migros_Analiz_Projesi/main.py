from src.data_collector import fetch_nufus_data, fetch_migros_data
from src.data_cleaner import clean_migros_data
from src.analyzer import analyze_data
from src.excel_report import create_excel_report

def run_pipeline():
    print("1. Veriler internetten ve PDF'den çekiliyor...")
    pdf_yolu = "data/migros türkiye mağaza listesi.pdf"
    
    df_nufus_ham = fetch_nufus_data()
    df_migros_ham = fetch_migros_data(pdf_yolu)
    
    print("2. Veriler temizleniyor ve matematiksel analiz yapılıyor...")
    df_migros_temiz = clean_migros_data(df_migros_ham)
    df_final = analyze_data(df_migros_temiz, df_nufus_ham)
    
    if df_final is not None:
        print("3. Raporlar oluşturuluyor ve klasörlere kaydediliyor...")
        
        df_final.to_csv("data/migros_analiz_sonucu.csv", index=False)
        
        excel_verisi = create_excel_report(df_final)
        with open("reports/Migros_Detayli_Rapor.xlsx", "wb") as f:
            f.write(excel_verisi)
            
        print("✅ İşlem BAŞARILI! Çıktıları 'data' ve 'reports' klasörlerinde bulabilirsiniz.")
    else:
        print("❌ Hata: Veriler işlenemediği için rapor oluşturulamadı.")

if __name__ == "__main__":
    run_pipeline()