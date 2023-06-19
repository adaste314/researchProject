import nltk
import parsing
import time

nltk.download('words')

d_posts, und_posts = parsing.d_posts, parsing.und_posts
all_posts = d_posts + und_posts
t = time.time()

# Filter and clean the words while splitting the posts
english_words = set(nltk.corpus.words.words())
common_words = set(['am', 'is', 'are', 'was', 'were', 'being', 'been', 'and', 'be', 'have', 'has', 'had', 'do',
                    'does', 'did', 'will', 'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could',
                    'the', 'a', 'an'])
word_counts = nltk.FreqDist()
total_words = 0

for post in all_posts:
    post_words = [word.lower() for word in post.split() if word.isalpha() and word.lower() in english_words and word.lower() not in common_words]
    word_counts.update(post_words)
    total_words += len(post_words)

# Calculate relative frequency for each word
word_dict = {word: count / total_words for word, count in word_counts.items()}

for word in word_dict:
    print(word)

print(f"FILTER TIME: {time.time() - t}")
