from numpy.random import randint
import pandas as pd
from random import choices
import os

# pd.set_option('display.max_colwidth', None)


def calculatePercentage():
    score = 1 * stats.hilarious + 0.8 * stats.funny + 0.6 * stats.normal + 0.4 * stats.bad + \
        0.2 * stats.horrible / stats.hilarious + stats.funny + \
        stats.normal + stats.bad + stats.horrible
    stats["score"] = score


users = os.listdir("./stats")
print("Users found", users)

print("\nNew user or old user? (new/old)")
newold = input()

if newold == "new":
    print("Type in a username for your new user")
    user = input()
elif newold == "old":
    print("Type in your username")
    user = input()

print("\nHello, ", user, "\n")

try:
    jokes = pd.read_csv(f"./stats/{user}/user1-remaining-jokes.csv",
                        escapechar='\\').reset_index(drop=True)
    stats = pd.read_csv(
        f"./stats/{user}/user1-stats.csv").reset_index(drop=True)
except:
    print("No saved stats found for your user, using zero preferences...\n")
    jokes = pd.read_csv("./dataset/wocka-stupidstuff.csv",
                        escapechar='\\').reset_index(drop=True)
    stats = pd.read_csv("./dataset/ws-stats.csv").reset_index(drop=True)
    calculatePercentage()

while True:
    print("Jokes? (y/n)")
    ans = input()
    if ans == "y":
        categories = stats["category"]
        probs = stats["score"]/stats["score"].sum()
        category = choices(categories, probs)[0]
        print("\nChosen category -->", category)

        chosen = jokes[jokes.category == category]
        rand = randint(len(chosen))
        joke = jokes.loc[rand]["body"]
        print("\n--------------------------------------------------------\n")
        print(joke)
        print("\n--------------------------------------------------------\n")

        jokes = jokes[jokes.body != joke]
        print(len(jokes), "Jokes remaining\n")

        print("How's the joke? (hilarious/funny/normal/bad/horrible)")
        rev = input()

        if rev == "hilarious":
            print("\nAlways knew you have a good sense of humour\n")
            stats.loc[stats["category"] == category, rev] += 1
        elif rev == "funny":
            print("\nLOL LMAO\n")
            stats.loc[stats["category"] == category, rev] += 1
        elif rev == "normal":
            print("\nAlrighty then!\n")
            stats.loc[stats["category"] == category, rev] += 1
        elif rev == "bad":
            print("\nAh, you're just shit\n")
            stats.loc[stats["category"] == category, rev] += 1
        elif rev == "horrible":
            print("\nHAHAHAHAHA (laughing sarcastically)\n")
            stats.loc[stats["category"] == category, rev] += 1
        else:
            print(
                "\nWhat's that? I see... \nYou don't like personalized stuff, do you?\nVery well, then\n")  # something better

    elif ans == "n":
        break


calculatePercentage()

print("Saving your jokes preferences...")
jokes.to_csv("./stats/user1-remaining-jokes.csv", index=False)
stats.to_csv("./stats/user1-stats.csv", index=False)
print("Done")
