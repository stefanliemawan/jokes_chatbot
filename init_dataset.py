import pandas as pd
from sklearn.utils import shuffle

wocka = pd.read_json("./joke-dataset-master/wocka.json")
wocka.drop(["id", "title"], axis=1, inplace=True)
# print(wocka)

stupidstuff = pd.read_json("./joke-dataset-master/stupidstuff.json")
stupidstuff.drop(["id", "rating"], axis=1, inplace=True)
# print(stupidstuff)

dadjokes = pd.read_csv("./crawled/dadjokes.csv").reset_index(drop=True)

data = pd.concat([wocka, stupidstuff, dadjokes]).reset_index(drop=True)

data["category"].replace("Animals", "Animal", inplace=True)
data["category"].replace("Bar Jokes", "Bar", inplace=True)
data["category"].replace("Blind Jokes", "Blind", inplace=True)
data["category"].replace("Blonde Jokes", "Blonde", inplace=True)
data["category"].replace("Blond", "Blonde", inplace=True)
data["category"].replace("Computer", "Computer", inplace=True)
data["category"].replace("Crazy Jokes", "Crazy", inplace=True)
data["category"].replace("Ethnic Jokes", "Ethnic", inplace=True)
data["category"].replace("Farmers", "Farmer", inplace=True)
data["category"].replace("Food Jokes", "Food", inplace=True)
data["category"].replace("Holidays", "Holiday", inplace=True)
data["category"].replace("Idiots", "Idiot", inplace=True)
data["category"].replace("Insults", "Insult", inplace=True)
data["category"].replace("Lawyers", "Lawyer", inplace=True)
data["category"].replace("Light Bulbs", "Light Bulb", inplace=True)
data["category"].replace("Lightbulb", "Light Bulb", inplace=True)
data["category"].replace("Office Jokes", "Office", inplace=True)
data["category"].replace("One Liners", "One Liner", inplace=True)
data["category"].replace("Other / Misc", "Miscellaneous", inplace=True)
data["category"].replace("Police Jokes", "Police", inplace=True)
data["category"].replace("Puns", "Pun", inplace=True)
data["category"].replace("Sports", "Sport", inplace=True)
data["category"].replace("State Jokes", "State", inplace=True)
data["category"].replace("Yo Mama", "Yo Momma", inplace=True)

data.dropna(inplace=True)
data.sort_values("category", inplace=True)
data.to_csv("./dataset/wocka-stupidstuff.csv", encoding="utf-8", index=False)
# print(data)

# categories = data["category"].unique()
# categories = pd.Series(categories)
stats = pd.DataFrame(
    {"category": data["category"], "hilarious": 0, "funny": 0, "normal": 0, "bad": 0, "horrible": 0})
stats.drop_duplicates("category", inplace=True)
stats.sort_values("category", inplace=True)
stats.to_csv("./dataset/ws-stats.csv", index=False)
# print(stats)
