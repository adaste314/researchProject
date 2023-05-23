import nltk
import parsing
from collections import Counter

nltk.download('words')

d_posts, und_posts = parsing.d_posts, parsing.und_posts
all_posts = d_posts + und_posts

# Combine all posts and split into words
words = []
for post in all_posts:
    words.extend(post.split())

# Filter and clean the words
english_words = set(nltk.corpus.words.words())
common_words = set(['am', 'is', 'are', 'was', 'were', 'being', 'been', 'and', 'be', 'have', 'has', 'had', 'do',
                    'does', 'did', 'will', 'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could',
                    'the', 'a', 'an'])
filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() in english_words and word.lower() not in common_words]

# Count the occurrence of each word and calculate relative frequency
word_counts = Counter(filtered_words)
total_words = len(filtered_words)
words = [(word, count / total_words) for word, count in word_counts.items()]
