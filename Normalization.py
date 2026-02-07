# Veriyi yükle
from keras.datasets import mnist
import numpy as np

(X_train, y_train), (X_test, y_test) = mnist.load_data()

# 1. Min-Max Normalizasyon (0–1 arası)
X_train_1 = X_train / 255.0
X_test_1 = X_test / 255.0

# 2. Z-Score Normalizasyon
mean = np.mean(X_train)
std = np.std(X_train)
X_train_2 = (X_train - mean) / std
X_test_2 = (X_test - mean) / std

# 3. -1 ile 1 arası normalizasyon
X_train_3 = (X_train / 127.5) - 1
X_test_3 = (X_test / 127.5) - 1
