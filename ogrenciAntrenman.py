import  pandas as pd
df = pd.read_excel("ogrenci1.xlsx")
#Ortalama Hesap
def OrtalamaHesap(df):
    df["Ortalama"] = df["Vize"] * 0.4 + df["Final"] * 0.6
    return df

df = OrtalamaHesap(df)

#kullanıcı etkileşimi girdi alma
bolum = str(input("Bolum giriniz: "))
donem = str(input("Donemi giriniz: "))
dy = int(input("Yıl giriniz"))

#BÖLÜM BAZLI LİSTELEME
#Gruopby
b = df.groupby(["Bölüm.1","donem","donem.1"])
aranan = b.get_group((bolum,donem,dy))
print(aranan[["Ad","Soyad","ders","Vize","Final","Ortalama"]].to_string(index = False))

#Filter - Query
# Sütun isimlerini ` ` içine aldık
d = df.query("`Bölüm.1` == @bolum and donem == @donem and `donem.1` == @dy")
s = d.filter(["Ad","Soyad","ders","Vize","Final","Ortalama"])
print(s.to_string(index = False))

#İloc loc ile
sutun = ["Ad","Soyad","Vize","Final","Ortalama","ders"]
sart = (df["Bölüm.1"] == bolum) & (df["donem"] == donem) & (df["donem.1"] == dy)
aranan = df.loc[sart,sutun]
print(aranan.to_string(index = False))

#sade yazım
sa = (df["Bölüm.1"] == bolum) & (df["donem"] == donem) & (df["donem.1"] == dy)
ar = df[sa]
son = ar[["Ad","Soyad","ders","Vize","Final","Ortalama"]]
print(son.to_string(index = False))


