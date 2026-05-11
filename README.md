# 🛒 Migros Environmental Sustainability Analysis

Bu proje, Migros'un çevresel sürdürülebilirlik verilerini ve lojistik ağını analiz ederek anlamlı stratejik çıkarımlar sunan bir **Veri Analitiği ve Karar Destek Sistemi** çalışmasıdır.

## 🚀 Öne Çıkan Özellikler
* **Otomatik Veri Toplama:** Migros web sitesi ve kurumsal raporlarından `BeautifulSoup` ve `pdfplumber` ile veri kazıma.
* **Demografik Entegrasyon:** Bölgesel nüfus verilerinin analize dahil edilerek veri setinin zenginleştirilmesi.
* **Konumsal Analiz:** Nüfus yoğunluğu verileri ile atık yağ toplama merkezlerinin lokasyonlarının karşılaştırılması.
* **Stratejik Çıkarımlar:** Nüfus başına düşen geri dönüşüm kapasitesinin ölçülmesi ve verimlilik analizi ile yeni merkez ihtiyaçlarının belirlenmesi.
* **Interaktif Dashboard:** Tüm analiz sonuçlarının `Streamlit` ve `Plotly` kullanılarak görselleştirilmesi.

## 🛠️ Teknik Stack
* **Language:** Python 3.x
* **Data Processing:** `Pandas`, `pdfplumber`
* **Web Scraping & Parsing:** `BeautifulSoup4`, `requests`
* **Visualization:** `Streamlit`, `Plotly`

## 📈 Karar Destek Vizyonu
Bu çalışma, ham veriyi sadece listelemekle kalmaz; "Hangi bölgede nüfusa oranla toplama merkezi eksik?" veya "Atık yağ toplama verimliliği nerede en yüksek?" gibi kritik iş sorularına yanıt vererek veri odaklı karar verme süreçlerini simüle eder.

## 📂 Proje Yapısı

```text
migros-sustainability-analysis/
├── data/               # Analiz edilen veri setleri ve CSV dosyaları
├── reports/            # İndirilen PDF sürdürülebilirlik raporları
├── src/                # Veri kazıma ve işleme mantığını içeren yardımcı kodlar
├── app.py              # Ana Streamlit dashboard arayüzü
├── main.py             # Veri toplama ve analiz sürecini başlatan ana dosya
├── README.md           # Proje dokümantasyonu
└── requirements.txt    # Gerekli Python kütüphanelerinin listesi

## ⚙️ Kurulum ve Kullanım

Aşağıdaki adımları takip ederek projeyi kendi yerel ortamınızda çalıştırabilirsiniz:

1. **Projeyi bilgisayarınıza klonlayın:**
   ```bash
   git clone [https://github.com/GorkemKutukculer/migros-sustainability-analysis.git](https://github.com/GorkemKutukculer/migros-sustainability-analysis.git)

2. **Proje dizinine gidin:**

   cd migros-sustainability-analysis

3. **Gerekli Python kütüphanelerini yükleyin:**

   pip install -r requirements.txt

4.**Analiz panelini (Dashboard) başlatın:**

  python -m streamlit run app.py

