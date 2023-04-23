import requests as req
from bs4 import BeautifulSoup as bs
import random
import nltk.corpus
from nltk.corpus import words as wds
import math
import scipy.stats as stats
import numpy as np

nltk.download('words')

d_posts, und_posts = [], []
pages_total = 50
sample_size = 2000

for i in range(pages_total):
    page = req.get("https://www.psychforums.com:443/borderline-personality/?start=" + str(i * 40)).text
    parser = bs(page, 'html.parser')
    d_posts += list(parser.find(id="wrap").find_all("li", class_="row bg1")) + list(
        parser.find(id="wrap").find_all("li", class_="row bg2"))

    page = req.get("https://www.psychforums.com:443/antisocial-personality/?start=" + str(i * 40)).text
    parser = bs(page, 'html.parser')
    d_posts += list(parser.find(id="wrap").find_all("li", class_="row bg1")) + list(
        parser.find(id="wrap").find_all("li", class_="row bg2"))

    page = req.get("https://www.gardening-forums.com/forums/general-gardening-talk.5/page-" + str(i)).text
    parser = bs(page, 'html.parser')
    und_posts += list(parser.find(id="top").find_all("div", class_="structItem-title"))

d_posts = random.sample([str(i).split('href="')[1].split('"')[0] for i in d_posts], sample_size)
und_posts = random.sample([str(i).split('href="')[1].split('"')[0] for i in und_posts], sample_size)

print(f"POSTS TAKEN: {len(d_posts) + len(und_posts)}")

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

print(f"UNFILTERED WORDS: {len(words)}")

english_words = set(wds.words())
common_words = ['am', 'is', 'are', 'was', 'were', 'being', 'been', 'and', 'be', 'have', 'has', 'had', 'do', 'does',
                'did', 'will', 'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could', 'the', 'a', 'an']
clean_words = [''.join(filter(str.isalpha, word)) for word in words]
filtered_words = [i.lower() for i in clean_words if i.lower() in english_words and i.lower() not in common_words]
words = {word: filtered_words.count(word) / len(filtered_words) for word in filtered_words}

print(f"FILTERED WORDS: {len(words)}")

train_posts = random.sample(all_posts, int(.8 * len(all_posts)))
test_posts = [i for i in all_posts if i not in train_posts]

for i in train_posts:
    predict = 1
    for word in i.split(" "):
        if word in words:
            predict *= words[word]

    if i in d_posts:
        actual = 1
    else:
        actual = 0

    sigmoid_der = (math.exp(-1 * predict) / (math.exp(-1 * predict) + 1)) * ((1 - math.exp(-1 * predict)) / math.exp(-1 * predict) + 1)
    for word in i.split(" "):
        if actual < predict:
            if word in words:
                words[word] -= sigmoid_der
                if words[word] < 0:
                    words[word] = 0
        else:
            if word in words:
                words[word] += sigmoid_der
                if words[word] > 1:
                    words[word] = 1

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

correct = 0
predicted_und = 0
predicted_d = 0
actual_und = 0
actual_d = 0
for i in data:
    if i[0] == i[1]:
        correct += 1

    if i[0]:
        predicted_d += 1
    elif not i[0]:
        predicted_und += 1

    if i[1]:
        actual_d += 1
    elif not i[1]:
        actual_und += 1

print(f"Percent correct: {correct / len(data) * 100}%")
print(f"Total datapoints: {len(data)}")

print("Table values")
print([predicted_und, predicted_d])
print([actual_und, actual_d])

chi_square_test_statistic, p_value = stats.chisquare([predicted_und, predicted_d], [actual_und, actual_d])
print(f'Chi square test statistic: {str(chi_square_test_statistic)}')
print(f'p-value: {str(p_value)}')
print(f'Critical value: {stats.chi2.ppf(1 - 0.05, df=1)}')
