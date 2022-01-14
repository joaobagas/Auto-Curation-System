import torch
from torch import nn


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        # Instantiate convolutional layers
        self.pool = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=2, kernel_size=(3, 3), stride=(1, 1), padding=1),
            nn.MaxPool2d(3, 3)
        )

        # Instantiate fully connected layers
        self.fc = nn.Sequential(
            nn.Linear(8712, 100),
            nn.ReLU(inplace=True),
            nn.Linear(100, 50),
            nn.ReLU(inplace=True),
            nn.Linear(50, 1)
        )


    def forward(self, x):
        x = self.pool(x)
        x = x.view(-1, 8712)
        #x = self.fc(x)
        x = torch.sub(1.1, self.fc(x))

        return x