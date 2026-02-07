import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

# Örnek sinyal: Kenar 3. indiste
signal = np.array([10, 10, 10, 50, 50, 50, 10, 10])
x = np.arange(len(signal))

# Türev filtresi (x yönü için)
kernel = np.array([-1, 0, 1])

# 'same' → girişle aynı uzunlukta sonuç verir
edge_response = scipy.signal.convolve(signal, kernel, mode='same')

plt.figure(figsize=(10, 5))
plt.plot(x, signal, label='Orijinal Sinyal', linewidth=2)
plt.plot(x, edge_response, label='Türev (Kenar)', linestyle='--', color='red')
plt.axhline(0, color='gray', linestyle=':', linewidth=1)
plt.legend()
plt.title('Türev Filtresiyle Kenar Tespiti')
plt.xlabel('Piksel Konumu')
plt.ylabel('Değer')
plt.grid(True)
plt.show()
