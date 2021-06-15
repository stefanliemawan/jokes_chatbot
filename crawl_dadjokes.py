from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import urllib.request
import requests

url1 = "https://www.countryliving.com/life/a27452412/best-dad-jokes/"

dadjokes = []

webpage = requests.get(url1)
soup = BeautifulSoup(webpage.text, "html.parser")

tags = soup.find_all("ul", attrs={"class": "body-ul"})
for t in tags:
    lis = t.find_all("li")
    lis = [eval(li.text.strip()) for li in lis]
    dadjokes = dadjokes + lis


print(dadjokes)

dj = pd.DataFrame({"body": dadjokes, "category": "Dad"})
print(dj)

dj.to_csv("./crawled/dadjokes.csv", index=False)
