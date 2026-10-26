import pandas as pd

df = pd.read_csv("ratings.csv")

matrix = df.pivot_table(index="user", columns="title", values="rating")

print(matrix.shape)