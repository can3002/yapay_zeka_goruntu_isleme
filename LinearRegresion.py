import numpy as np
import matplotlib.pyplot as plt

# Örnek veri
X = np.array([1, 2, 3, 4, 5])
y = np.array([3, 4, 2, 5, 6])

# Ortalama hesapla
x_mean = np.mean(X)
y_mean = np.mean(y)

# w ve b hesapla
num = np.sum((X - x_mean) * (y - y_mean))
den = np.sum((X - x_mean) ** 2)
w = num / den
b = y_mean - w * x_mean

print(f"Eğim (w): {w}")
print(f"Kesişim (b): {b}")

# Tahmin fonksiyonu
def predict(x):
    return w * x + b

# Grafik
plt.scatter(X, y, color='blue', label='Gerçek Veri')
plt.plot(X, predict(X), color='red', label='Doğrusal Regresyon')
plt.legend()
plt.show()
