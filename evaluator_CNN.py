import numpy as np
from chess import ChessGame
from chess_position import ChessPosition
from eval_reader import EvalReader

import numpy as np
import pandas as pd
import torch
from torch import nn
import matplotlib.pyplot as plt

evalReader = EvalReader()

x_train, y_train = evalReader.get_cnn(1000)
x_test, y_test = evalReader.get_cnn(100)

class CNNChessEvaluator(nn.Module):
  def __init__(self):
    super().__init__()

    self.net = nn.Sequential(
      nn.Conv2d(in_channels=12, out_channels=12, padding = 4, kernel_size=(8, 8)),
      nn.ReLU(),
      nn.Conv2d(in_channels=12, out_channels=12, padding = 4, kernel_size=(8, 8)),
      nn.ReLU(),
      nn.Flatten(),
      nn.Linear(1200, 1)
    )

  def forward(self, x: torch.Tensor) -> torch.Tensor:
    out = self.net(x).squeeze()
    return out

train_loss_values = []
test_loss_values = []
epoch_count = []

def train():
  model_0 = CNNChessEvaluator()
  loss_fn = nn.MSELoss()
  optimizer = torch.optim.Adam(params=model_0.parameters(), lr=0.01, weight_decay=1e-5)

  epochs = 501
  
  for epoch in range(epochs):

      model_0.train()

      if torch.is_grad_enabled():
        optimizer.zero_grad()
      output = model_0(x_train)
      loss = loss_fn(output, y_train)
      if loss.requires_grad:
        loss.backward()

      optimizer.step()

      model_0.eval()

      with torch.inference_mode():

        test_pred = model_0(x_test)
        test_loss = loss_fn(test_pred, y_test)        

        epoch_count.append(epoch)
        train_loss_values.append(loss.item())
        test_loss_values.append(test_loss.item())

        if epoch % 10 == 0:
            print(f"Epoch: {epoch} | MAE Train Loss: {loss} | MAE Test Loss: {test_loss}")
  return model_0

#model = train()
#torch.save(model, './models/CNN.torch')