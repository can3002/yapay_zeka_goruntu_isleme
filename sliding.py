import pandas as pd

# 1. Dosyayı oku
df = pd.read_excel('hamveri.xlsx')

# 2. İşlenecek kolonları belirle
tarih_kolonlari = ['Year', 'Month', 'Day', 'Hour']
veri_kolonlari = ['SICAKLIK_°C', 'hiz', 'TOPRAK_SICAKLIGI_5_°C', 'TOPRAK_SICAKLIGI_20_°C']


yeni_df = df[tarih_kolonlari].copy()

#KAYDIRMA İŞLEMİ YAPILACAK
pencere = 6 # (5 saat geçmiş + 1 saat kendisi)

for kolon in veri_kolonlari:
    for i in range(pencere - 1, -1, -1):
        # Yeni kolon ismi (Örn: SICAKLIK_GecmiSGs_5)
        yeni_isim = f"{kolon}_Gecmis_{i}"
        yeni_df[yeni_isim] = df[kolon].shift(i)

# 5. Boş satırları temizle ve kaydet
yeni_df = yeni_df.dropna()
yeni_df.to_excel('hamveri_islenmis.xlsx', index=False)