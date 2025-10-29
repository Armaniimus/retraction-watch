import pandas as pd
from model_training import ML_Model_Builder
data = pd.read_csv('data/train_set.csv', index_col='Record ID')
target = pd.read_csv('data/target_set.csv', index_col='Record ID')

builder = ML_Model_Builder(data, target["in2022"])
builder.setModel()
model = builder.build()
model.train()