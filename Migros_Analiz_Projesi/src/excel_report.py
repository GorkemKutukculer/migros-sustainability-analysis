import pandas as pd
import io

def create_excel_report(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Veri Analizi', index=False)
    
    workbook = writer.book
    worksheet = writer.sheets['Veri Analizi']
    
    worksheet.set_column('A:A', 20) 
    worksheet.set_column('B:E', 18) 
    worksheet.set_column('G:G', 95) 
    worksheet.set_column('I:I', 130) 
    
    num_format = workbook.add_format({'num_format': '#,##0'})
    float_format = workbook.add_format({'num_format': '0.00'})
    bold_format = workbook.add_format({'bold': True, 'font_size': 12, 'font_color': '#333333'})
    
    box_header_format = workbook.add_format({'bold': True, 'font_size': 13, 'bg_color': '#EFEFEF', 'border': 1})
    box_calc_header_format = workbook.add_format({'bold': True, 'font_size': 13, 'bg_color': '#E3F2FD', 'border': 1})
    box_text_format = workbook.add_format({'font_size': 11, 'border': 1, 'text_wrap': True, 'valign': 'vcenter'})
    box_calc_text_format = workbook.add_format({'font_size': 11, 'border': 1, 'font_name': 'Consolas', 'text_wrap': True, 'valign': 'vcenter'})

    worksheet.set_column('B:B', 22, num_format) 
    worksheet.set_column('C:C', 18, num_format) 
    worksheet.set_column('D:D', 18, float_format) 
    worksheet.set_column('E:E', 22, num_format) 

    max_row = len(df) + 1
    
    toplam_nokta = int(df['Atik_Yag_Noktasi_Sayisi'].sum())
    toplam_nufus = int(df['Nufus'].sum())
    max_nokta = int(df['Atik_Yag_Noktasi_Sayisi'].max())
    min_nokta = int(df['Atik_Yag_Noktasi_Sayisi'].min())
    fark = max_nokta - min_nokta
    ortalama_nokta_kisi = int(toplam_nufus / toplam_nokta) if toplam_nokta > 0 else 0
    hedef_nokta = toplam_nokta * 2
    toplam_ilce = len(df)
    ortalama_nufus = int(toplam_nufus / toplam_ilce) if toplam_ilce > 0 else 0
    genel_hizmet_endeksi = round((toplam_nokta / toplam_nufus) * 100000, 2) if toplam_nufus > 0 else 0
    ortalama_nokta_ilce = round(toplam_nokta / toplam_ilce, 1) if toplam_ilce > 0 else 0
    ideal_nokta_sayisi = int(toplam_nufus / 50000) 
    kapasite_acigi = ideal_nokta_sayisi - toplam_nokta if ideal_nokta_sayisi > toplam_nokta else 0

    df_sorted_pop = df.sort_values(by='Nufus', ascending=False)
    top3_pop = int(df_sorted_pop['Nufus'].head(3).sum())
    top3_pop_ratio = round((top3_pop / toplam_nufus) * 100, 1) if toplam_nufus > 0 else 0
    top3_points = int(df_sorted_pop['Atik_Yag_Noktasi_Sayisi'].head(3).sum())
    top3_points_ratio = round((top3_points / toplam_nokta) * 100, 1) if toplam_nokta > 0 else 0
    
    worst_ratio_row = df.loc[df['Nokta_Basina_Kisi'].idxmax()]
    worst_ilce = worst_ratio_row['Ilce']
    worst_ratio = int(worst_ratio_row['Nokta_Basina_Kisi'])
    worst_vs_avg = round(worst_ratio / ortalama_nokta_kisi, 1) if ortalama_nokta_kisi > 0 else 0
    
    new_total_points = toplam_nokta + 50
    new_avg_kisi = int(toplam_nufus / new_total_points)
    iyilesme_miktari = ortalama_nokta_kisi - new_avg_kisi
    
    top_pop_row = df_sorted_pop.iloc[0]
    top_pop_ilce = top_pop_row['Ilce']
    top_pop = int(top_pop_row['Nufus'])
    top_pop_points = int(top_pop_row['Atik_Yag_Noktasi_Sayisi'])
    toplam_yag_litre = int(top_pop * 0.5)
    kutu_basi_yag = int(toplam_yag_litre / top_pop_points) if top_pop_points > 0 else 0

    worksheet.write('G2', '📌 Veri Notları ve Çıkarımlar', box_header_format)
    worksheet.write('G3', f'📦 Toplam Kapasite: {toplam_nufus:,} kişilik nüfusa {toplam_nokta} atık toplama noktasıyla hizmet verilmektedir.', box_text_format)
    worksheet.write('G4', f'⚖️ Dağılım Aralığı (Fark): En yüksek ve en düşük kapasiteye sahip ilçeler arasında {fark} adet mağaza farkı (varyans) bulunmaktadır.', box_text_format)
    worksheet.write('G5', f'🎯 Birim Yük Optimizasyonu: Altyapı genelinde bir (1) atık yağ noktasına ortalama {ortalama_nokta_kisi:,} kişi düşmektedir. Kaynak tahsisi bu yoğunluğa göre planlanmalıdır.', box_text_format)
    worksheet.write('G6', f'🌱 Gelecek Hedefi: Kapasitenin 2 katına çıkarılması durumunda projelendirilen toplam altyapı büyüklüğü {hedef_nokta} nokta olmalıdır.', box_text_format)
    worksheet.write('G7', f'📊 Ortalama İlçe Ölçeği: Analiz edilen toplam {toplam_ilce} ilçenin her birine düşen ortalama demografik büyüklük {ortalama_nufus:,} kişidir.', box_text_format)
    worksheet.write('G8', f'📈 Genel Hizmet Penetrasyonu: İstanbul genel ortalamasına bakıldığında her 100.000 kişiye ortalama {genel_hizmet_endeksi} adet hizmet noktası düşmektedir.', box_text_format)
    worksheet.write('G9', f'🏢 İlçe Başına Ortalama Nokta: Mevcut noktalar eşit dağıtılsaydı, her bir ilçeye ortalama {ortalama_nokta_ilce} adet hizmet noktası düşecekti.', box_text_format)
    worksheet.write('G10', f'⚠️ İdeal Kapasite Açığı: Her 50.000 kişiye 1 nokta (ideal) standardı baz alındığında, sistemde acilen {kapasite_acigi} adet yeni noktaya ihtiyaç vardır.', box_text_format)
    worksheet.write('G11', f'🌍 Nüfus Yoğunluğu Etkisi: İstanbul\'un en kalabalık 3 ilçesi, tüm nüfusun %{top3_pop_ratio}\'sini oluştururken, atık toplama noktalarımızın sadece %{top3_points_ratio}\'sine sahiptir.', box_text_format)
    worksheet.write('G12', f'🚨 En Zayıf Halka: En kalabalık noktalara sahip {worst_ilce} ilçesinde, bir kutunun sırtındaki yük ortalamadan {worst_vs_avg} kat daha fazladır.', box_text_format)
    worksheet.write('G13', f'🚀 İyileştirme Senaryosu: Eğer sisteme 50 yeni atık noktası eklersek, kutu başına düşen insan yükü {iyilesme_miktari:,} kişi azalacaktır.', box_text_format)
    worksheet.write('G14', f'🛢️ Tahmini Atık Yağ Kapasitesi: Sadece {top_pop_ilce}, yılda tahmini {toplam_yag_litre:,} litre atık yağ üretebilir. Mağaza başı {kutu_basi_yag:,} litre yağ toplanmalıdır.', box_text_format)

    worksheet.write('I2', '🧮 Detaylı Matematiksel Çözümler ve Formüller', box_calc_header_format)
    worksheet.write('I3', f'Toplama: ∑ Nüfus = {toplam_nufus:,} | ∑ Nokta Sayısı = {toplam_nokta}', box_calc_text_format)
    worksheet.write('I4', f'Çıkarma: Maksimum Nokta ({max_nokta}) - Minimum Nokta ({min_nokta}) = {fark}', box_calc_text_format)
    worksheet.write('I5', f'Bölme  : {toplam_nufus:,} / {toplam_nokta} = {ortalama_nokta_kisi:,}', box_calc_text_format)
    worksheet.write('I6', f'Çarpma : {toplam_nokta} * 2 = {hedef_nokta}', box_calc_text_format)
    worksheet.write('I7', f'Bölme  : {toplam_nufus:,} / {toplam_ilce} (Toplam İlçe) = {ortalama_nufus:,}', box_calc_text_format)
    worksheet.write('I8', f'Orantı : ({toplam_nokta} / {toplam_nufus:,}) * 100.000 = {genel_hizmet_endeksi}', box_calc_text_format)
    worksheet.write('I9', f'Bölme  : {toplam_nokta} / {toplam_ilce} = {ortalama_nokta_ilce}', box_calc_text_format)
    worksheet.write('I10', f'Fark   : İdeal({toplam_nufus:,} / 50.000) - Mevcut({toplam_nokta}) = {kapasite_acigi}', box_calc_text_format)
    worksheet.write('I11', f'Adım 1: İlk 3 İlçe = {top3_pop:,} | Adım 2: Nüfus Oranı = %{top3_pop_ratio} | Adım 3: Nokta Oranı = %{top3_points_ratio}', box_calc_text_format)
    worksheet.write('I12', f'Adım 1: {worst_ilce} Yükü = {worst_ratio:,} kişi/kutu | Adım 2: Kıyaslama = {worst_vs_avg} Kat', box_calc_text_format)
    worksheet.write('I13', f'Adım 1: {toplam_nokta} + 50 = {new_total_points} Nokta | Adım 2: Yeni Yük = {new_avg_kisi:,} | Adım 3: İyileşme = {iyilesme_miktari:,}', box_calc_text_format)
    worksheet.write('I14', f'Adım 1: {top_pop:,} Kişi * 0.5 Lt = {toplam_yag_litre:,} Lt | Adım 2: Dağıtım = {kutu_basi_yag:,} Litre/Nokta', box_calc_text_format)

    worksheet.write('G17', '1. Hizmet Boşluğu Endeksi (100.000 Kişiye Düşen Nokta)', bold_format)
    chart1 = workbook.add_chart({'type': 'column'})
    chart1.add_series({'categories': ['Veri Analizi', 1, 0, max_row-1, 0], 'values': ['Veri Analizi', 1, 3, max_row-1, 3], 'fill': {'color': '#E53935'}})
    worksheet.insert_chart('G19', chart1, {'x_scale': 1.2, 'y_scale': 1.1})
    
    worksheet.write('G36', '2. Toplam Atık Yağ Noktası Sayısı', bold_format)
    chart2 = workbook.add_chart({'type': 'column'})
    chart2.add_series({'categories': ['Veri Analizi', 1, 0, max_row-1, 0], 'values': ['Veri Analizi', 1, 1, max_row-1, 1], 'fill': {'color': '#43A047'}})
    worksheet.insert_chart('G38', chart2, {'x_scale': 1.2, 'y_scale': 1.1})

    worksheet.write('G55', '3. İlçe Nüfus Büyüklüğü', bold_format)
    chart3 = workbook.add_chart({'type': 'area'}) 
    chart3.add_series({'categories': ['Veri Analizi', 1, 0, max_row-1, 0], 'values': ['Veri Analizi', 1, 2, max_row-1, 2], 'fill': {'color': '#1E88E5'}})
    worksheet.insert_chart('G57', chart3, {'x_scale': 1.2, 'y_scale': 1.1})

    worksheet.write('G74', '4. Nokta Başına Düşen Kişi (Yük Analizi)', bold_format)
    chart4 = workbook.add_chart({'type': 'line'}) 
    chart4.add_series({'categories': ['Veri Analizi', 1, 0, max_row-1, 0], 'values': ['Veri Analizi', 1, 4, max_row-1, 4], 'line': {'color': '#8E24AA', 'width': 2}})
    worksheet.insert_chart('G76', chart4, {'x_scale': 1.2, 'y_scale': 1.1})
    
    writer.close()
    return output.getvalue()