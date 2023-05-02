import requests as req
from bs4 import BeautifulSoup as bs
import random

d_posts, und_posts = [], []
pages_total = int(input("PAGES TO PARSE: "))
sample_size = int(input("NUM POSTS TO PULL: "))

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

for i in d_posts:
    parser = bs(req.get(i).text, 'html.parser')
    d_posts[d_posts.index(i)] = str(parser.find('div', class_="content")).split('">')[1].split('</')[0]

for i in und_posts:
    parser = bs(req.get("https://www.gardening-forums.com/" + str(i)).text, 'html.parser')
    und_posts[und_posts.index(i)] = " ".join(str(parser.find('div', class_="bbWrapper")).split('"'))
