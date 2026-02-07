import pandas as pd
from openpyxl.worksheet.print_settings import PrintArea

df = pd.read_excel("ogrenci1.xlsx")
#ORTALAMA HESABI
df.loc[:, "Ortalama"] = df["Vize"] * 0.4 + df["Final"] * 0.6
#Ad ve soyad sütunlarını birleştime ve ekleme
df.loc[:, "Öğrenci"] = df["Ad"] + " " + df["Soyad"]
#Bir öğrencinin tüm dönemlerde aldığı dersler ve notları sıralama
ogrenci = input("Öğrenci giriniz (Ali Ak gibi arada boşluk olmalı): ")

#Groupby ile yapma
f = df.groupby("Öğrenci")
aranan = f.get_group(ogrenci)
print(aranan[["donem","donem.1","ders","Vize", "Final","Ortalama"]].to_string(index=False))

print("-------Filter Query--------")
#Filter - Query ile yapma
f1 = df.query("`Öğrenci` == @ogrenci")
ara = f1.filter(["donem","donem.1","ders","Vize","Final","Ortalama"])
print(ara.to_string(index=False))

print("--------Sade Yazım-----------")
sart = (df["Öğrenci"] == ogrenci)
ara1 = df[sart]
sonuc = ara1[["donem","donem.1","ders","Vize","Final","Ortalama"]]
print(sonuc.to_string(index=False))

print("-----------LOC TABLO------------")
sutun = ["donem","donem.1","ders","Vize","Final","Ortalama"]
sart = (df["Öğrenci"] == ogrenci)
ara1 = df.loc[sart, sutun]
print(ara1.to_string(index=False))

print("-----------İLOC TABLO------------")
sutun = ["donem","donem.1","ders","Vize","Final","Ortalama"]
sutun_indis = [df.columns.get_loc(c) for c in sutun]
sart = (df["Öğrenci"] == ogrenci)
satir = df.index[sart].tolist()
sonuc = df.iloc[satir, sutun_indis]
print(sonuc.to_string(index=False))