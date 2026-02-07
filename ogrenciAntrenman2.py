import pandas as pd
from openpyxl.worksheet.print_settings import PrintArea

df = pd.read_excel("ogrenci1.xlsx")

fakulte = input("Fakülte Giriniz: ")
donem = input("Dönem giriniz (GUZ, BAHAR): ")
dy = int(input("Dönem yılı giriniz (2324,2425,2526): "))
#Ortalama Hesap
df.loc[:, "Ortalama"] = df["Vize"] * 0.4 + df["Final"] * 0.6
#Groupby
f = df.groupby(["Fak..1","donem","donem.1"])
aranan = f.get_group((fakulte, donem, dy))
print(aranan[["Ad","Soyad","Bölüm.1","Vize","Final","Ortalama","ders"]].to_string(index=False))

#Filter - Query
print("FİLTER- QUERY İLE VERİLEN TABLO---------")

f1 = df.query("`Fak..1` == @fakulte and donem == @donem and `donem.1` == @dy")
a1 = f1.filter(["Ad","Soyad","Bölüm.1","Vize","Final","Ortalama","ders"])
print(a1.to_string(index=False))

#sade
print("-------------SADE YAZIM İLE TABLO -------------------")
sart = (df["Fak..1"] == fakulte) & (df["donem"] == donem) & (df["donem.1"] == dy)
ara = df[sart]
sonuc = ara[["Ad","Soyad","Bölüm.1","Vize","Final","Ortalama","ders"]]
print(sonuc.to_string(index=False))

#LOC ile yapma
print("-------------LOC İLE TABLO -------------------")
sutun = ["Ad","Soyad","Bölüm.1","Vize","Final","Ortalama","ders"]
sart1 = (df["Fak..1"] == fakulte) & (df["donem"] == donem) & (df["donem.1"] == dy)
ara1 = df.loc[sart1, sutun]
print(ara1.to_string(index=False))

# 1. Önce gösterilecek sütunların isimlerini değil, konumlarını (index) bulmalıyız
hedef_sutunlar = ["Ad", "Soyad", "Bölüm.1", "Vize", "Final", "Ortalama", "ders"]
sutun_indisleri = [df.columns.get_loc(c) for c in hedef_sutunlar]

# 2. Şartı sağlayan satırların TAM SAYI indislerini (0, 1, 5... gibi) almalıyız
sart = (df["Fak..1"] == fakulte) & (df["donem"] == donem) & (df["donem.1"] == dy)
satir_indisleri = df.index[sart].tolist()

# 3. ILOC ile seçim: df.iloc[satır_numaraları, sütun_numaraları]
print("------------- ILOC İLE TABLO -------------------")
sonuc_iloc = df.iloc[satir_indisleri, sutun_indisleri]
print(sonuc_iloc.to_string(index=False))