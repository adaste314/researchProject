import math
import random
import scraping

d_posts, und_posts, words = scraping.d_posts, scraping.und_posts, scraping.word_dict
all_posts = d_posts + und_posts

# Split the data into train and test sets
train_posts = random.sample(all_posts, int(0.8 * len(all_posts)))
test_posts = [post for post in all_posts if post not in train_posts]

# Train the model
for post in train_posts:
    predict = 0
    for word in post.split(" "):
        if word in words:
            predict += words[word]

    actual = int(post in d_posts)
    predict = 1 / (1 + math.exp(-predict))
    change = predict * (1 - predict)

    for word in post.split(" "):
        if actual < predict:
            if word in words:
                words[word] -= change
        else:
            if word in words:
                words[word] += change

# Test the model
data = []
for post in test_posts:
    predict = 0
    for word in post.split(" "):
        if word in words:
            predict += words[word]

    actual = int(post in d_posts)
    predict = round(1 / (1 + math.exp(-predict)))
    data.append((predict, actual))

# Evaluate the model
correct = 0
predicted_d, predicted_und, actual_d, actual_und = 0, 0, 0, 0
fn, tn, fp, tp = 0, 0, 0, 0

for prediction, actual in data:
    if prediction == actual:
        if prediction:
            tp += 1
        else:
            tn += 1
        correct += 1
    else:
        if prediction:
            fp += 1
        else:
            fn += 1

    if prediction:
        predicted_d += 1
    else:
        predicted_und += 1

    if actual:
        actual_d += 1
    else:
        actual_und += 1