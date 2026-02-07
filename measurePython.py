from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Gerçek değerler ve model tahminleri
y_true = [0, 1, 1, 1, 0, 1, 0, 0]
y_pred = [0, 1, 0, 1, 0, 1, 1, 0]

print("Accuracy:", accuracy_score(y_true, y_pred))
print("Precision:", precision_score(y_true, y_pred))
print("Recall:", recall_score(y_true, y_pred))
print("F1-score:", f1_score(y_true, y_pred))
