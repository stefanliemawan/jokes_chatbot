from numpy.random import randint
import pandas as pd
from random import choices
import os
import time
import sys
from bs4 import BeautifulSoup
import requests
import re

# pd.set_option('display.max_colwidth', None)


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


def typeAnimation(text, t):
    print()
    for l in text:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(t)


def calculatePercentage(stats):
    n = stats.hilarious + stats.funny + stats.normal + stats.bad + stats.horrible
    n[n == 0] = 1
    score = ((1.5 * stats.hilarious + 1 * stats.funny +
              0.5 * stats.normal - 1 * stats.bad - 1.5 * stats.horrible)/5)
    stats["score"] = score
    stats.loc[stats.score < 1, "score"] = 1
    return stats


def returnJokeBasedOnCategory(jokes, category):
    chosen = jokes[jokes.category == category]
    if len(chosen) == 0:
        print("No more joke in this category, moving on\n")
        return
    else:
        rand = randint(0, len(chosen))
        joke = chosen.iloc[rand]["body"]
        return joke


def handleFeedback(stats, category):
    print("How's the joke? (hilarious/funny/normal/bad/horrible)\n")
    rev = input()

    if rev == "hilarious":
        strings = [
            "\nAlways knew you have a good sense of humour\n", "\nMy Boy!\n"]
        rand = randint(0, len(strings))
        print(strings[rand])
        stats.loc[stats["category"] == category, rev] += 1
    elif rev == "funny":
        strings = ["\nLOL LMAO\n",
                   "\nI am starting to like you more and more\n"]
        rand = randint(0, len(strings))
        print(strings[rand])
        stats.loc[stats["category"] == category, rev] += 1
    elif rev == "normal":
        strings = ["\nAlrighty then!\n",
                   "\nThat's not bad I suppose\n", "\nMeh, Fine\n"]
        rand = randint(0, len(strings))
        print(strings[rand])
        stats.loc[stats["category"] == category, rev] += 1
    elif rev == "bad":
        strings = ["\nAh, you're just shit\n",
                   "\nSeriously?\n", "\nNo, you're bad\n"]
        rand = randint(0, len(strings))
        print(strings[rand])
        stats.loc[stats["category"] == category, rev] += 1
    elif rev == "horrible":
        strings = ["\nHAHAHAHAHA (laughing sarcastically)\n",
                   "\nYou and your shit humour sense (chuckle)\n", "\nYou disappoint me\n"]
        rand = randint(0, len(strings))
        print(strings[rand])
        stats.loc[stats["category"] == category, rev] += 1
    else:
        print(
            "\nWhat's that? I see... \nYou don't like personalized stuff, do you?\nVery well, then\n")
    return stats


def handleJoke(jokes, joke):
    print("\n--------------------------------------------------------")
    typeAnimation(joke, 0.05)
    print("\n\n--------------------------------------------------------\n")

    jokes = jokes[jokes.body != joke]
    print(len(jokes), "Jokes remaining\n")
    return jokes


def containsWord(word, sentence):
    return f" {word} " in f" {sentence} "


def printInstructions():
    print("---------------------------------------------")
    print("Ask me for a joke or any particular category you want to include")
    print("Ask me with the keyword 'about' to get information regarding anything")
    print("Type 'search <keyword>' to return one joke based on that keyword")
    print("Type 'categories' print every available categories")
    print("Type 'stats' to view your stats and jokes preferences")
    print("Type 'reset stats' to reset your preferences")
    print("Type 'help' to print this instruction again")
    print("Or you can simply say hi to me :)")
    print("---------------------------------------------\n")


def searchOnline(keyword):
    url = "https://en.wikipedia.org/wiki/" + keyword
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, "html.parser")
    tags = soup.find("div", attrs={"class": "mw-parser-output"})
    try:
        for t in tags.findAll("p"):
            if len(t.text) > 30:
                desc = t.text.strip()
                break
        desc = re.sub(r"\[[^[]]*\]", "", desc)
        typeAnimation(desc, 0.01)
        time.sleep(t_sleep)
        print("\nThat's all that I know. :)\n")
    except:
        time.sleep(t_sleep)
        print("\nI could not find anything about that, sorry mate :(\n")
    return


print("\nHello,", user, "\n")
print("My name is Jokybo")
print("I am here to give you jokes and lighten your day")
print("Your feedbacks on the the jokes will enhance my ability to personalize future jokes to your liking based on its category\n")
printInstructions()

categories = stats["category"]
bodies = jokes["body"]


t_sleep = 1

while True:
    stats = calculatePercentage(stats)
    time.sleep(0.5)
    print("What can I do for you?\n")
    ans = input()
    category_keyword = ans.title().split()
    category_keyword = [s for s in category_keyword if len(s) > 2]
    category_keyword = "|".join(category_keyword)
    if containsWord("do you know about", ans.lower()) or containsWord("tell me about", ans.lower()):
        keyword = ans.split("about ")[1]
        searchOnline(keyword)
    elif categories.str.contains(category_keyword).any():
        if len(category_keyword) == 0:
            print("I'm afraid I do not have any joke about that particular category\n")
        else:
            category = categories.loc[categories.str.contains(
                category_keyword) == True].values
            print("\nMatched Category: ", category)
            category = category[0]
            time.sleep(t_sleep)
            print("\nChosen category -->", category)
            joke = returnJokeBasedOnCategory(jokes, category)
            jokes = handleJoke(jokes, joke)
            stats = handleFeedback(stats, category)
    elif ans.startswith("search"):
        search_keyword = ans.split()[1]
        print("Searching for '", search_keyword, "'")
        time.sleep(t_sleep)
        if bodies.str.contains(search_keyword).any():
            chosen = jokes[bodies.str.contains(search_keyword)]
            rand = randint(0, len(chosen))
            joke = chosen.iloc[rand]["body"]
            category = chosen.iloc[rand]["category"]
            jokes = handleJoke(jokes, joke)
            stats = handleFeedback(stats, category)
        else:
            print("\nKeyword not found\n")
    elif containsWord("joke", ans) or containsWord("joke?", ans):
        print("\nOne hilarious joke, coming right away")
        probs = stats["score"]/stats["score"].sum()
        category = choices(categories, probs)[0]
        time.sleep(t_sleep)
        print("\nChosen category -->", category)
        joke = returnJokeBasedOnCategory(jokes, category)
        jokes = handleJoke(jokes, joke)
        stats = handleFeedback(stats, category)
    elif ans == "categories":
        print(categories)
    elif ans == "help":
        printInstructions()
    elif ans == "stats":
        print(stats, "\n")
    elif ans == "reset stats":
        stats[["hilarious", "funny", "normal", "bad", "horrible"]] = 0
        print("\nStats reset done\n")
    elif containsWord("hey", ans.lower()) or containsWord("hello", ans.lower()) or containsWord("hi", ans.lower()) or containsWord("greetings", ans.lower()):
        print("\nGreetings, ", user)
        time.sleep(t_sleep)
        print("Are you ready for the best joke of your life?\n")
        time.sleep(t_sleep)
        print("Go on, ask me for a joke\n")
    elif containsWord("jokybo", ans.lower()):
        print("\nDid you call my name?")
        time.sleep(t_sleep)
        print("Nobody has ever called me by my name in such a long time...")
        time.sleep(t_sleep)
        print("Just kidding :)")
        time.sleep(t_sleep)
        print("Or am I?\n")
    elif ans == "bye":
        print("\nBoo\n")
        break
    else:
        print("\nI don't have the answer for that, unfortunately")


stats = calculatePercentage(stats)


print("Saving your jokes preferences...")
jokes.to_csv(f"./stats/{user}/{user}-remaining-jokes.csv", index=False)
stats.to_csv(f"./stats/{user}/{user}-stats.csv", index=False)
print("Done")
