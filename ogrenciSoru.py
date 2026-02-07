import pandas as pd
import numpy as np

df = pd.read_excel("ogrenci1.xlsx")
listelemeTur = int(input("Hangi Tür listeleme istiyorsunuz 1. Filter, 2. Groupby, 3. Normal"))

donem = str(input("Donem giriniz: "))
donemYil = (input("Donem Yılıs giriniz(2425 gibi): "))


def bolumListe():
    print("Listeleme Ekranına Hoşgeldiniz")
    bolum = str(input("Bolum giriniz: "))
    kosul = (
            (df["Bölüm.1"] == bolum) &  # Bölüm Adı (Bilgisayar vb.)
            (df["donem"] == donem) &  # GUZ / BAHAR
            (df["donem.1"] == int(donemYil))  # Yıl (2324) - Sayısal olduğu için int'e çevirdik
    )
    sonuc_df = df[kosul]
    # 4. Sonuçları Göster
    if not sonuc_df.empty:
        print("\n--- Bulunan Dersler ---")
        # Sadece görmek istediğimiz sütunları seçip ekrana basalım
        gosterilecek_sutunlar = ["Ad", "Soyad", "ders", "Vize", "Final"]
        print(sonuc_df[gosterilecek_sutunlar].to_string(index=False))

        # İsterseniz bu sonucu ayrı bir dataframe olarak saklayabilirsiniz
        return sonuc_df
    else:
        print("\nAradığınız kriterlere uygun kayıt bulunamadı.")
        return None

def grupBolum():
    print("--- GroupBy ile Ders Listeleme ---")
    bolum = str(input("Bolum giriniz: "))
    grup_veri = df.groupby(["Bölüm.1", "donem", "donem.1"])
    aranan_grup = grup_veri.get_group((bolum, donem, int(donemYil)))
    print(aranan_grup[["Ad", "Soyad", "ders", "Vize", "Final"]].to_string(index=False))
def grupFiltre():
    print("--- Filter ile Ders Listeleme ---")
    bolum = str(input("Bolum giriniz: "))
    donemint = int(donemYil)
    sonuc = df.query("`Bölüm.1` == @bolum and donem == @donem and `donem.1` == @donemint")
    if not sonuc.empty:
        print(sonuc[["Ad", "Soyad", "ders", "Vize", "Final"]].to_string(index=False))
    else:
        print("Kayıt bulunamadı.")
# Fonksiyonu çalıştır
def fakListe():
    fakulte = str(input("Fakulte giriniz: "))
    print("Listeleme Ekranına Hoşgeldiniz")
    kosul = (
        (df["Fak."]== fakulte) &
        (df["donem"] == donem) &
        (df["donem.1"] == int(donemYil))
    )
    sonuc_df = df[kosul]
    if not sonuc_df.empty:
        gosterilecek_sutunlar = ["Ad", "Soyad", "ders", "Vize", "Final"]
        print(sonuc_df[gosterilecek_sutunlar].to_string(index=False))
        return sonuc_df
    else:
        print("\nAradığınız kriterlere uygun kayıt bulunamadı.")
        return None
def bolumTum():
    bolum = str(input("Bolum giriniz: "))
    print("--- Bolum ile Ders Listeleme ---")
    kosul = (
        (df["Bolum.1"] == bolum)
    )
    sonuc = df[kosul]
    if not sonuc.empty:
        gosterilecek_sutunlar = ["Ad", "Soyad", "ders", "Vize", "Bölüm.1"]
        print(sonuc[gosterilecek_sutunlar].to_string(index=False))
        return sonuc
    else:
        print("\nAradığınız kriterlere uygun kayıt bulunamadı.")
        return None

if listelemeTur == 1:
    grupFiltre()
elif listelemeTur == 2:
    grupBolum()
elif listelemeTur == 3:
    bolumListe()
elif listelemeTur == 4:
    fakListe()
elif listelemeTur == 5:
    bolumTum()
else:
    print("Uygun bir sıralama seçmediniz")