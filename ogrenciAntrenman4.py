import  pandas as pd

df = pd.read_excel("ogrenci1.xlsx")
fakulte = input("fakulte giriniz: ")
dyil = int(input("dyil giriniz: "))
donem = input("donem giriniz: ")

print("------------Groupby ile Tablo-------------")
a = df.groupby(["Fak..1","donem.1","donem"])
ara = a.get_group((fakulte,dyil,donem))
print(ara[["ders"]].to_string(index=False))

print("------------Filter - Query---------")
f1 = df.query("`Fak..1`== @fakulte and`donem.1`== @dyil and donem==@donem")
ara1 = f1.filter(["ders"])
print(ara1.to_string(index=False))

print("-----------Sade-------------")
sart = (df["Fak..1"]== fakulte) & (df["donem.1"]== dyil) & (df["donem"] == donem)
ar = df[sart]
sonuc = ar[["ders"]]
print(sonuc.to_string(index=False))

print("------LOC----------")
sutun = ["ders"]
sart1 = (df["Fak..1"] == fakulte) & (df["donem.1"]== dyil) & (df["donem"] == donem)
ara1 = df.loc[sart1, sutun]
print(ara1.to_string(index=False))
