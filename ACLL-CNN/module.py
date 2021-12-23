import torch
from torch import nn
from torch.autograd.grad_mode import F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        # Instantiate convolutional layers
        self.conv = nn.Sequential(
            nn.Conv2d(1, 3, (3, 3), (1, 1), bias=True),
            nn.ReLU(),
            nn.Dropout(p=0.5),
            nn.AvgPool2d(4, 4),
        )

        # Instantiate fully connected layers
        self.fc = nn.Sequential(
            nn.Linear(7203, 200),
            nn.ReLU(),
            nn.Dropout(p=0.5),
            nn.Linear(200, 20),
            nn.ReLU(),
            nn.Dropout(p=0.5),
            nn.Linear(20, 2)
        )

    def forward(self, x):
        x = self.conv(x)
        x = x.view(-1, 7203)
        x = self.fc(x)

        return x


