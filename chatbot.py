from numpy.random import randint
import pandas as pd

pd.set_option('display.max_colwidth', None)

jokes = pd.read_csv("./dataset/wocka-stupidstuff.csv",
                    escapechar='\\').reset_index(drop=True)

stats = pd.read_csv("./dataset/ws-stats.csv").reset_index(drop=True)
# stats = pd.read_csv("./stats/user1.csv").reset_index(drop=True)

# make a formula to get random jokes based on stats

while True:
    print("Jokes? (y/n)")
    ans = input()
    rand = randint(len(jokes))
    if ans == "y":
        joke = jokes.loc[rand]["body"]
        category = jokes.loc[rand]["category"]
        print("\n--------------------------------------------------------\n")
        print(joke)
        print("\n--------------------------------------------------------\n")

        print("How's the joke? (hilarious/funny/normal/bad/horrible)")
        rev = input()
        stats.loc[stats["category"] == category, rev] += 1

        if rev == "hilarous":
            print("\nAlways knew you have a good sense of humour\n")
        if rev == "funny":
            print("\nLOL LMAO\n")
        if rev == "normal":
            print("\nAlrighty then!\n")
        if rev == "bad":
            print("\nAh, you're just shit\n")
        if rev == "horrible":
            print("\nHAHAHAHAHA (laughing sarcastically)\n")

    elif ans == "n":
        break

stats.to_csv("./stats/user1.csv", index=False)
