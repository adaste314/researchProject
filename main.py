import requests as req
from bs4 import BeautifulSoup as bs
import random
import collections
import nltk.corpus
from nltk.corpus import words as wds
import re
import math
import time

nltk.download('words')

while True:
    page_number = 0
    d_posts = []
    page, last_page = 0, -1

    t = time.time()

    while page != last_page:
        page = req.get("https://www.psychforums.com:443/borderline-personality/?start=" + str(page_number)).text
        parser = bs(page, 'html.parser')
        d_posts += list(parser.find(id="wrap").find_all("li", class_="row bg1")) + list(parser.find(id="wrap").find_all("li", class_="row bg2"))
        page_number += 40
        last_page = req.get("https://www.psychforums.com:443/borderline-personality/?start=" + str(page_number - 40)).text

    print(f"BORDERLINE PERSONALITY TIME: {time.time() - t}")
    t = time.time()

    page_number = 0
    page, last_page = 0, -1
    while page != last_page:
        page = req.get("https://www.psychforums.com:443/antisocial-personality/?start=" + str(page_number)).text
        parser = bs(page, 'html.parser')
        d_posts += list(parser.find(id="wrap").find_all("li", class_="row bg1")) + list(parser.find(id="wrap").find_all("li", class_="row bg2"))
        page_number += 40
        last_page = req.get("https://www.psychforums.com:443/antisocial-personality/?start=" + str(page_number - 40)).text

    print(f"ANTISOCIAL PERSONALITY TIME: {time.time() - t}")

    try:
        d_posts = random.sample([str(i).split('href="')[1].split('"')[0] for i in d_posts], 5)
        break
    except:
        continue

t = time.time()

while True:
    page_number = 0
    und_posts = []
    # page, last_page = 0, -1
    # while page != last_page:
    for i in range(82):
        page = req.get("https://www.gardening-forums.com/forums/general-gardening-talk.5/page-" + str(i)).text
        parser = bs(page, 'html.parser')
        und_posts += list(parser.find(id="top").find_all("div", class_="structItem-title"))
        # last_page = req.get("https://www.gardening-forums.com/forums/general-gardening-talk.5/page-" + str(page_number)).text
        # page_number += 1

    try:
        und_posts = random.sample([str(i).split('href="')[1].split('"')[0] for i in und_posts], 5)
        break
    except:
        continue

print(f"GARDENING TIME: {time.time() - t}")
t = time.time()

for i in d_posts:
    parser = bs(req.get(i).text, 'html.parser')
    d_posts[d_posts.index(i)] = str(parser.find('div', class_="content")).split('">')[1].split('</')[0]

for i in und_posts:
    parser = bs(req.get("https://www.gardening-forums.com/" + str(i)).text, 'html.parser')
    und_posts[und_posts.index(i)] = " ".join(str(parser.find('div', class_="bbWrapper")).split('"'))

words = []
all_posts = d_posts + und_posts
for i in all_posts:
    words += i.split(" ")

print(f"CONTENT TIME: {time.time() - t}")
t = time.time()

words = collections.Counter([re.sub('[^A-Za-z0-9]+', '', i.lower()) for i in words if re.sub('[^A-Za-z0-9]+', '', i.lower()) in set(wds.words()) and len(re.sub('[^A-Za-z0-9]+', '', i.lower())) >= 3])
total = len(words)
for i in words:
    words.update({i: (words[i] / total) - words[i]})

print(f"WORD TIME: {time.time() - t}")
t = time.time()

train_posts = random.sample(all_posts, int(.8 * len(all_posts)))
test_posts = [i for i in all_posts if not i in train_posts]

for i in train_posts:
    predict = 1
    for word in i.split(" "):
        if word in words:
            predict *= words[word]

    if i in d_posts:
        actual = 1
    else:
        actual = 0

    sigmoid_der = (round(math.exp(predict), 16) / (round(math.exp(predict), 16) + 1)) * (1 - round(math.exp(predict), 16) / round(math.exp(predict), 16) + 1)
    if actual < predict:
        for word in i.split(" "):
            if word in words:
                words[word] -= sigmoid_der
    else:
        for word in i.split(" "):
            if word in words:
                words[word] -= sigmoid_der

print(f"TRAIN TIME: {time.time() - t}")
t = time.time()

data = []
for i in test_posts:
    predict = 1
    for word in i.split(" "):
        if word in words:
            predict *= words[word]
    predict = round(predict)
    if i in d_posts:
        data.append((predict, 1))
    else:
        data.append(predict, 0)

print(f"DATA TIME: {time.time() - t}")

for i in data:
    print(f"Prediction: {i[0]} | True Value: {i[1]}")
