import praw
import nltk
from collections import defaultdict

# Initialize NLTK's English dictionary and stop words
nltk.download("words")
nltk.download("stopwords")
from nltk.corpus import words, stopwords

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id="WplWeD8RP-FsYmDJxXWL4g",
    client_secret="ERvaTz_AnWrSzE6o2VHa2sv7Yty6Tg",
    user_agent="scraper by /u/Kneemium"
)

reddit.config.store_json_result = True
# Define the subreddits to scrape
subreddits = ["bpd", "aspd", "cooking", "books"]

# Function to filter out stop words, make words lowercase, and check if they are in the English dictionary
english_words = set(words.words())
stop_words = set(stopwords.words("english"))

def is_meaningful_word(word):
    word = word.lower()
    return word in english_words and word not in stop_words

# Initialize a dictionary to store word frequencies
word_frequency = defaultdict(int)

# Scrape posts from each subreddit
for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.top(limit=1000)

    for post in top_posts:
        # Split the post content into words
        words_in_post = post.title.split() + post.selftext.split()

        # Filter out stop words, make words lowercase, and update word frequencies
        meaningful_words_in_post = filter(is_meaningful_word, words_in_post)
        for word in meaningful_words_in_post:
            word_frequency[word.lower()] += 1

# Calculate the total number of words
total_words = sum(word_frequency.values())

# Calculate word frequencies as ratios
word_frequency_ratios = {word: count / total_words for word, count in word_frequency.items()}

# Print the dictionary of word frequencies
print(word_frequency_ratios)
