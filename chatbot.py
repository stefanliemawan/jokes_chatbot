import pandas as pd

pd.set_option('display.max_colwidth', None)

data = pd.read_csv("./dataset/wocka-stupidstuff.csv").reset_index(drop=True)
