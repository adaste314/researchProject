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

t = time.time()

d_posts = []
#pages_total = 250 # Number of pages of interest across both forums
pages_total = 10

for i in range(pages_total):
    page = req.get("https://www.psychforums.com:443/borderline-personality/?start=" + str(i * 40)).text
    parser = bs(page, 'html.parser')
    d_posts += list(parser.find(id="wrap").find_all("li", class_="row bg1")) + list(parser.find(id="wrap").find_all("li", class_="row bg2"))

    page = req.get("https://www.psychforums.com:443/antisocial-personality/?start=" + str(i * 40)).text
    parser = bs(page, 'html.parser')
    d_posts += list(parser.find(id="wrap").find_all("li", class_="row bg1")) + list(parser.find(id="wrap").find_all("li", class_="row bg2"))

d_posts = random.sample([str(i).split('href="')[1].split('"')[0] for i in d_posts], 5)
print(f"DIAGNOSED TIME: {time.time() - t} seconds")
t = time.time()

und_posts = []
for i in range(10):
    page = req.get("https://www.gardening-forums.com/forums/general-gardening-talk.5/page-" + str(i)).text
    parser = bs(page, 'html.parser')
    und_posts += list(parser.find(id="top").find_all("div", class_="structItem-title"))

und_posts = random.sample([str(i).split('href="')[1].split('"')[0] for i in und_posts], 5)
print(f"UNDIAGNOSED TIME: {time.time() - t}")
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

print(f"CONTENT TIME: {time.time() - t} seconds; number of words is {len(words)}")

t = time.time()

english_words = set(wds.words())
clean_words = [''.join(filter(str.isalpha, word)) for word in words]
filtered_words = [i for i in clean_words if i in english_words]
word_freq = {word: filtered_words.count(word) for word in filtered_words}
print(f"WORD TIME: {time.time() - t}")

# Tested up to this line

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

    sigmoid_der = (math.exp(predict) / (math.exp(predict) + 1)) * (1 - math.exp(predict) / math.exp(predict) + 1)
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
        data.append((predict, 0))

print(f"DATA TIME: {time.time() - t}")

for i in data:
    print(f"Prediction: {i[0]} | True Value: {i[1]}")
