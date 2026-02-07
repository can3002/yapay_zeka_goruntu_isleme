import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

# CNN model tanımı
class SimpleCNN(nn.Module):
    def __init__(self, output_activation=None):
        super(SimpleCNN, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(16*14*14, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )
        self.output_activation = output_activation

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        if self.output_activation == 'log_softmax':
            return torch.log_softmax(x, dim=1)
        elif self.output_activation == 'softmax':
            return torch.softmax(x, dim=1)
        else:
            return x

# Eğitim fonksiyonu
def train(model, loss_fn, optimizer, train_loader, device):
    model.train()
    total_loss = 0
    for data, target in train_loader:
        data, target = data.to(device), target.to(device)

        optimizer.zero_grad()
        output = model(data)

        # One-hot encoding gereken loss'lar
        if isinstance(loss_fn, (nn.MSELoss, nn.L1Loss, nn.SmoothL1Loss)):
            target_one_hot = torch.zeros_like(output)
            target_one_hot.scatter_(1, target.unsqueeze(1), 1.0)
            loss = loss_fn(output, target_one_hot)

        # CrossEntropyLoss, NLLLoss için doğrudan
        elif isinstance(loss_fn, (nn.CrossEntropyLoss, nn.NLLLoss)):
            loss = loss_fn(output, target)

        # BCELoss ve BCEWithLogitsLoss sadece binary için çalışır!
        else:
            raise ValueError(f"{loss_fn} bu model için uygun değil. Sadece ikili sınıflandırmada kullanılır.")

        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(train_loader)


# Test fonksiyonu
def test(model, test_loader, device):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            pred = output.argmax(dim=1)
            correct += (pred == target).sum().item()
            total += target.size(0)
    return correct / total

# Veri seti ve loader
transform = transforms.ToTensor()
train_dataset = datasets.MNIST(root='./data', train=True, transform=transform, download=True)
test_dataset = datasets.MNIST(root='./data', train=False, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1000)

# Deneysel karşılaştırma
loss_functions = {
    "CrossEntropyLoss": (nn.CrossEntropyLoss(), None),
    "NLLLoss": (nn.NLLLoss(), 'log_softmax'),
    "MSELoss": (nn.MSELoss(), 'softmax'),
    "L1Loss": (nn.L1Loss(), 'softmax'),
    "BCELoss": (nn.BCELoss(), 'sigmoid'),
    "BCEWithLogitLoss": (nn.BCEWithLogitsLoss(), None),
    "SmoothL1Loss": (nn.SmoothL1Loss(), 'softmax'),

}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
results = {}

for name, (loss_fn, activation) in loss_functions.items():
    print(f"\n==> Eğitim Başladı: {name}")
    model = SimpleCNN(output_activation=activation).to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    loss_values = []
    acc_values = []

    for epoch in range(5):
        loss = train(model, loss_fn, optimizer, train_loader, device)
        acc = test(model, test_loader, device)
        loss_values.append(loss)
        acc_values.append(acc)
        print(f"Epoch {epoch+1}: Loss = {loss:.4f}, Accuracy = {acc*100:.2f}%")

    results[name] = (loss_values, acc_values)

# Sonuçları çizdir
for name in results:
    plt.plot(results[name][1], label=name)

plt.title("Loss Fonksiyonlarının Doğruluk Karşılaştırması")
plt.xlabel("Epoch")
plt.ylabel("Doğruluk")
plt.legend()
plt.grid(True)
plt.show()
