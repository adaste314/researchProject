import nltk.corpus
from nltk.corpus import words as wds
import parsing
import mysql.connector
from mysql.connector import connect, Error

nltk.download('words')
username, passkey = parsing.username, parsing.passkey

try:
    with connect(
        host="Serge-HP13",
        user=username,
        password=passkey,
        database='data'
    ) as connection:
        with connection.cursor() as cursor:
            d_posts, und_posts = parsing.d_posts, parsing.und_posts
            words = []
            all_posts = d_posts + und_posts
            for i in all_posts:
                words += i.split(" ")
            words = set(words)

            english_words = set(wds.words())
            common_words = ['am', 'is', 'are', 'was', 'were', 'being', 'been', 'and', 'be', 'have', 'has', 'had', 'do',
                            'does',
                            'did', 'will', 'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could', 'the', 'a',
                            'an']
            clean_words = [''.join(filter(str.isalpha, word)) for word in words]
            filtered_words = [i.lower() for i in clean_words if
                              i.lower() in english_words and i.lower() not in common_words]
            words = [(word, filtered_words.count(word) / len(filtered_words)) for word in filtered_words]
            cursor.executemany("INSERT INTO words(word, weighting) VALUES (%s, %f)", words)
            cursor.execute("SELECT link FROM posts")
            for i in cursor.fetchall():
                cursor.execute("INSERT INTO posts(words) VALUES %s", )

            connection.commit()

except Error as e:
    print(e)
