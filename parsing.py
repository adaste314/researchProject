import requests as req
from bs4 import BeautifulSoup as bs
import random
import mysql.connector
from mysql.connector import connect, Error
import database_creation

username, passkey = database_creation.username, database_creation.passkey
try:
    with connect(
        host="Serge-HP13",
        user=username,
        password=passkey,
        database='data'
    ) as connection:
        with connection.cursor() as cursor:
            d_posts, und_posts = [], []
            pages_total = int(input("PAGES TO PARSE: "))

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

            d_posts = [str(i).split('href="')[1].split('"')[0] for i in d_posts]
            und_posts = ["https://www.gardening-forums.com/" + str(i).split('href="')[1].split('"')[0] for i in und_posts]
            cursor.executemany("INSERT INTO posts(type, link) VALUES (0, %s)", und_posts)
            cursor.executemany("INSERT INTO posts(type, link) VALUES (1, %s)", d_posts)

            for i in d_posts:
                parser = bs(req.get(i).text, 'html.parser')
                d_posts[d_posts.index(i)] = str(parser.find('div', class_="content")).split('">')[1].split('</')[0]

            for i in und_posts:
                parser = bs(req.get(i).text, 'html.parser')
                und_posts[und_posts.index(i)] = " ".join(str(parser.find('div', class_="bbWrapper")).split('"'))

            cursor.execute('DELETE FROM posts WHERE COUNT(link) > 1 ORDER BY link')
            connection.commit()

except Error as e:
    print(e)

