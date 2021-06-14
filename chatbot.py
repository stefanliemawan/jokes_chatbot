from numpy.random import randint
import pandas as pd
from random import choices
import os

# pd.set_option('display.max_colwidth', None)

# keyword?


users = os.listdir("./stats")
print("Users found", users)

# print("\nType in a username\n")
# user = input()
user = "user1"

if user not in users:
    os.mkdir(f"./stats/{user}")

try:
    jokes = pd.read_csv(f"./stats/{user}/{user}-remaining-jokes.csv",
                        escapechar='\\').reset_index(drop=True)
    stats = pd.read_csv(
        f"./stats/{user}/{user}-stats.csv").reset_index(drop=True)
except:
    print("\nNo saved stats found for your user, using zero preferences...")
    jokes = pd.read_csv("./dataset/wocka-stupidstuff.csv",
                        escapechar='\\').reset_index(drop=True)
    stats = pd.read_csv("./dataset/ws-stats.csv").reset_index(drop=True)

# read_csv have some nan value even though the dataset does not from init_dataset
jokes.dropna(inplace=True)


def calculatePercentage(stats):
    n = stats.hilarious + stats.funny + stats.normal + stats.bad + stats.horrible
    n[n == 0] = 1
    probs = 1/len(stats)
    hilarious = (probs * stats.hilarious) * 1.5
    funny = (probs * stats.funny) * 1
    normal = (probs * stats.normal) * 0
    bad = (probs * stats.bad) * 1
    horrible = (probs * stats.horrible) * 1.5
    score = probs + ((hilarious + funny + normal - bad - horrible))
    print(score.sum())
    stats["score"] = score
    return stats
    # likelihood?


def returnJokeBasedOnCategory(jokes, category):
    chosen = jokes[jokes.category == category]
    rand = randint(len(chosen))
    joke = chosen.iloc[rand]["body"]
    return joke


def handleFeedback(stats, category):
    print("How's the joke? (hilarious/funny/normal/bad/horrible)\n")
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


def printInstructions():
    print("---------------------------------------------")
    print("Type 'joke' for any random joke")
    print("Type 'categories' print every available categories")
    print("Type in any category you want for a joke specific to that category")
    print("Type 'search <keyword>' to return one joke based on that keyword")
    print("Type 'help' to print this instruction again")
    print("---------------------------------------------\n")


print("\nHello,", user, "\n")
print("My name is Joky")
print("I am here to give you jokes and lighten your day")
print("Your feedbacks on the the jokes will enhance my ability to personalize future jokes to your liking based on its category\n")
printInstructions()

categories = stats["category"]
bodies = jokes["body"]


while True:
    stats = calculatePercentage(stats)
    print("What can I do for you?\n")
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
    elif ans == "Categories":
        print(categories)
    elif ans == "Help":
        printInstructions()
    elif ans == "Stats":
        print(stats, "\n")
    elif ans == "Exit":
        print("\nBoo\n")
        break
    else:
        print("\nI don't have the answer for that\n")


stats = calculatePercentage(stats)

print("Saving your jokes preferences...")
jokes.to_csv(f"./stats/{user}/{user}-remaining-jokes.csv", index=False)
stats.to_csv(f"./stats/{user}/{user}-stats.csv", index=False)
print("Done")
