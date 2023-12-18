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

x_train, y_train = evalReader.get_n(10000)
x_test, y_test = evalReader.get_n(100)

class MLPChessEvaluator(nn.Module):
  def __init__(self):
    super().__init__()

    self.net = nn.Sequential(
      nn.Linear(in_features=768, out_features=1024),
      nn.ReLU(),
      nn.Linear(in_features=1024, out_features=512),
      nn.ReLU(),
      nn.Linear(in_features=512, out_features=256),
      nn.ReLU(),
      nn.Linear(in_features=256, out_features=128),
      nn.ReLU(),
      nn.Linear(in_features=128, out_features=64),
      nn.ReLU(),
      nn.Linear(in_features=64, out_features=32),
      nn.ReLU(),
      nn.Linear(in_features=32, out_features=16),
      nn.ReLU(),
      nn.Linear(in_features=16, out_features=8),
      nn.ReLU(),
      nn.Linear(in_features=8, out_features=4),
      nn.ReLU(),
      nn.Linear(in_features=4, out_features=2),
      nn.ReLU(),
      nn.Linear(in_features=2, out_features=1)
    )

  def forward(self, x: torch.Tensor) -> torch.Tensor:
    return self.net(x).squeeze()

train_loss_values = []
test_loss_values = []
epoch_count = []

def train():
  model_0 = MLPChessEvaluator()
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
        #train_loss_values.append(mae_train)
        #test_loss_values.append(mae_test)

        if epoch % 10 == 0:
            print(f"Epoch: {epoch} | MAE Train Loss: {loss} | MAE Test Loss: {test_loss}")
  return model_0

#model = train()

#torch.save(model, './models/MLP.torch')