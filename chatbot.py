from numpy.random import randint
import pandas as pd
from random import choices
import os

# pd.set_option('display.max_colwidth', None)

# keyword?


users = os.listdir("./stats")
print("Users found", users)

# print("Type in a username")
# user = input()
user = "test"

if user not in users:
    os.mkdir(f"./stats/{user}")

try:
    jokes = pd.read_csv(f"./stats/{user}/{user}-remaining-jokes.csv",
                        escapechar='\\').reset_index(drop=True)
    stats = pd.read_csv(
        f"./stats/{user}/{user}-stats.csv").reset_index(drop=True)
except:
    print("No saved stats found for your user, using zero preferences...\n")
    jokes = pd.read_csv("./dataset/wocka-stupidstuff.csv",
                        escapechar='\\').reset_index(drop=True)
    stats = pd.read_csv("./dataset/ws-stats.csv").reset_index(drop=True)

# read_csv have some nan value even though the dataset does not from init_dataset
jokes.dropna(inplace=True)


def calculatePercentage(stats):
    n = stats.hilarious + stats.funny + stats.normal + stats.bad + stats.horrible
    n[n == 0] = 1
    score = 1 * stats.hilarious + 0.8 * stats.funny + 0.6 * \
        stats.normal + 0.4 * stats.bad + 0.2 * stats.horrible / n
    score[score == 0] = 1/len(score)
    stats["score"] = score
    return stats


def returnJokeBasedOnCategory(jokes, category):
    chosen = jokes[jokes.category == category]
    rand = randint(len(chosen))
    joke = chosen.iloc[rand]["body"]
    return joke


def handleFeedback(stats, category):
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
            "\nWhat's that? I see... \nYou don't like personalized stuff, do you?\nVery well, then\n")
    return stats


def handleJoke(jokes, joke):
    print("\n--------------------------------------------------------\n")
    print(joke)
    print("\n--------------------------------------------------------\n")

    jokes = jokes[jokes.body != joke]
    print(len(jokes), "Jokes remaining\n")
    return jokes


stats = calculatePercentage(stats)


print("\nHello,", user, "\n")
print("Welcome to blahblah chatbot")

categories = stats["category"]
bodies = jokes["body"]

while True:
    print("What can I do for you?")
    ans = input().title()
    if ans == "Joke":
        probs = stats["score"]/stats["score"].sum()
        category = choices(categories, probs)[0]
        print("\nChosen category -->", category)
        joke = returnJokeBasedOnCategory(jokes, category)
        jokes = handleJoke(jokes, joke)
        stats = handleFeedback(stats, category)
    elif categories.str.contains(ans).any():
        category = ans
        print("\nChosen category -->", category)
        joke = returnJokeBasedOnCategory(jokes, category)
        jokes = handleJoke(jokes, joke)
        stats = handleFeedback(stats, category)
    elif ans.startswith("Search"):
        keyword = ans.split()[1].lower()
        if bodies.str.contains(keyword).any():
            chosen = jokes[bodies.str.contains(keyword)]
            rand = randint(len(chosen))
            joke = chosen.iloc[rand]["body"]
            category = chosen.iloc[rand]["category"]
            jokes = handleJoke(jokes, joke)
            stats = handleFeedback(stats, category)
        else:
            print("\nKeyword not found\n")
    elif ans == "Exit":
        # print("\nWhat do you want from me then?\n")
        print("Boo\n")
        break


stats = calculatePercentage(stats)

print("Saving your jokes preferences...")
jokes.to_csv(f"./stats/{user}/{user}-remaining-jokes.csv", index=False)
stats.to_csv(f"./stats/{user}/{user}-stats.csv", index=False)
print("Done")
