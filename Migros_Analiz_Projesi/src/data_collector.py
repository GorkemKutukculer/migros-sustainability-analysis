import pandas as pd
import requests
from bs4 import BeautifulSoup
import pdfplumber
import streamlit as st

def fetch_nufus_data():
    url = "https://www.nufusu.com/ilceleri/istanbul-ilceleri-nufusu"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status() 
        soup = BeautifulSoup(r.content, 'html.parser')
        
        nufus_liste = []
        for satir in soup.find('table').find_all('tr')[1:]:
            cols = satir.find_all('td')
            if len(cols) > 1:
                name = cols[1].text.strip().upper().replace('İ', 'I').replace('Ü', 'U').replace('Ö', 'O').replace('Ş', 'S').replace('Ç', 'C').replace('Ğ', 'G')
                if "EYUP" in name: name = "EYUPSULTAN"
                pop = int(cols[2].text.replace('.', '').strip())
                nufus_liste.append({"Ilce": name, "Nufus": pop})
        
        return pd.DataFrame(nufus_liste)
    except Exception as e:
        st.error(f"Nüfus verileri çekilemedi: {e}")
        return None

def fetch_migros_data(pdf_path):
    try:
        raw_data = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table: raw_data.extend(table[1:])
        
        return pd.DataFrame(raw_data, columns=["Magaza_Adi", "Adres"])
    except Exception as e:
        st.error(f"PDF okunurken hata oluştu: {e}")
        return None