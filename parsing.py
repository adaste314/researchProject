import requests
from bs4 import BeautifulSoup
import threading
import time

t = time.time()
d_posts, und_posts = [], []
pages_total = 50

def extract_posts(url, class_type, class_name, result_list):
    while True:
        try:
            page = requests.get(url).text
            parser = BeautifulSoup(page, 'html.parser')
            wrap_element = parser.find(id="wrap")
            if wrap_element is not None:
                posts = wrap_element.find_all(class_type, class_=class_name)
                result_list.extend([str(post).split('href="')[1].split('"')[0] for post in posts])
            else:
                posts = parser.find_all(class_type, class_=class_name)
                result_list.extend([str(post).split('href="')[1].split('"')[0] for post in posts])
            return
        except requests.RequestException:
            pass

def extract_content(url, class_type, class_name, result_list, index):
    while True:
        try:
            page = requests.get(url).text
            parser = BeautifulSoup(page, 'html.parser')
            content_element = parser.find(class_type, class_=class_name)
            if content_element is not None:
                result_list[index] = str(content_element).split('">')[1].split('</')[0]
                return

        except requests.RequestException:
            pass

# Create thread lists for post extraction
threads_d_posts = []
threads_und_posts = []

# Extract d_posts from Psych Forums using threads
for i in range(pages_total):
    url = "https://www.psychforums.com:443/borderline-personality/?start=" + str(i * 40)
    thread = threading.Thread(target=extract_posts, args=(url, "li", "row bg1", d_posts))
    threads_d_posts.append(thread)
    thread.start()

    thread = threading.Thread(target=extract_posts, args=(url, "li", "row bg2", d_posts))
    threads_d_posts.append(thread)
    thread.start()

# Extract und_posts from Gardening Forum using threads
for i in range(pages_total):
    url = "https://www.gardening-forums.com/forums/general-gardening-talk.5/page-" + str(i)
    thread = threading.Thread(target=extract_posts, args=(url, "div", "structItem-title", und_posts))
    threads_und_posts.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads_d_posts:
    thread.join()

for thread in threads_und_posts:
    thread.join()

# Create thread lists for content extraction
threads_d_content = []
threads_und_content = []

# Extract content for d_posts using threads
for i, url in enumerate(d_posts):
    thread = threading.Thread(target=extract_content, args=(url, "div", "content", d_posts, i))
    threads_d_content.append(thread)
    thread.start()

# Extract content for und_posts using threads
for i, url in enumerate(und_posts):
    thread = threading.Thread(target=extract_content, args=("https://www.gardening-forums.com/" + url, "div", "bbWrapper", und_posts, i))
    threads_und_content.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads_d_content:
    thread.join()

for thread in threads_und_content:
    thread.join()

print(f"PARSE TIME: {time.time() - t}")
