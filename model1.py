import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from torchvision.datasets import MNIST
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

class EdgeFilters(nn.Module):
    def __init__(self, mode ='sobel'):
        super(EdgeFilters, self).__init__()
        if mode == 'sobel':
            self.kernel_x = torch.tensor([[[-1,0,1],
                                         [-2,0,2],
                                         [-1,0,1]]], dtype=torch.float32)
            self.kernel_y = torch.tensor([[[-1,-2,1],
                                         [0,0,0],
                                         [1,2,1]]], dtype=torch.float32)
        elif mode == 'laplace':
            self.kernel_x = torch.tensor([[[0., -1., 0.],
                                           [-1., 4., -1.],
                                           [0., -1., 0.]]], dtype=torch.float32)
            self.kernel_y = self.kernel_x
        elif mode == 'prewitt':
            self.kernel_x = torch.tensor([[[-1,0,1],
                                           [-1,0,1],
                                           [-1,0,1]]], dtype=torch.float32)
            self.kernel_y = torch.tensor([[[-1,-1,-1],
                                           [0,0,0],
                                           [1,1,1]]], dtype=torch.float32)
        else:
            raise ValueError("mode bunlardan biri olmalı")
        
        self.kernel_x = self.kernel_x.unsqueeze(0)
        self.kernel_y = self.kernel_y.unsqueeze(0)

    def forward(self,x):
        b,c,h,w = x.shape
        kernel_x = self.kernel_x.to(x.device).repeat(c,1,1,1)
        kernel_y = self.kernel_y.to(x.device).repeat(c,1,1,1)
        edge_x = F.conv2d(x, kernel_x, padding=1, groups=c)
        edge_y = F.conv2d(x, kernel_y, padding=1, groups=c)
        edge = torch.sqrt(edge_x ** 2 + edge_y ** 2)
        return edge
class SimpleCNN(nn.Module):
    def __init__(self, edge_mode='sobel'):
        super(SimpleCNN, self).__init__()
        self.edge_filter = EdgeFilters(mode=edge_mode)
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(16 * 14 * 14, 10)

    def forward(self, x):
        x = self.edge_filter(x)
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = x.view(-1, 16 * 14 * 14)
        x = self.fc1(x)
        return x

# 3. Veri Yükleme
transform = transforms.Compose([transforms.ToTensor()])
train_dataset = MNIST(root='./data', train=True, transform=transform, download=True)
test_dataset = MNIST(root='./data', train=False, transform=transform, download=True)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# 4. Model ve Eğitim Ayarları
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleCNN(edge_mode='prewitt').to(device)  # burayı: 'sobel', 'laplace', 'prewitt' olarak değiştirebilirsin
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# 5. Eğitim Döngüsü
for epoch in range(5):
    model.train()
    total_loss = 0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

# 6. Doğruluk Testi
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"Test Accuracy: {100 * correct / total:.2f}%")