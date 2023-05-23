import math
import random
import filtering

d_posts, und_posts, words = filtering.d_posts, filtering.und_posts, filtering.words
all_posts = d_posts + und_posts

train_posts = random.sample(all_posts, int(.8 * len(all_posts)))
test_posts = [i for i in all_posts if i not in train_posts]

predict = 0
for i in train_posts:
    for word in i.split(" "):
        if word in words:
            predict += words[word]

    if i in d_posts:
        actual = 1
    else:
        actual = 0

    predict = 1 / (1 + math.exp(-1 * predict))
    change = predict * (1 - predict)
    for word in i.split(" "):
        if actual < predict:
            if word in words:
                words[word] -= change

        else:
            if word in words:
                words[word] += change

data = []
for i in test_posts:
    predict = 0
    for word in i.split(" "):
        if word in words:
            predict += words[word]

    if i in d_posts:
        actual = 1
    else:
        actual = 0

    predict = round(1 / (1 + math.exp(-1 * predict)))
    data.append((predict, actual))

correct = 0
predicted_und, predicted_d, actual_d, actual_und = 0, 0, 0, 0
fn, tn, fp, tp = 0, 0, 0, 0
for i in data:
    if i[0] == i[1]:
        if i[0]:
            tp += 1
        else:
            tn += 1

        correct += 1
    else:
        if i[0]:
            fp += 1
        else:
            fn += 1

    if i[0]:
        predicted_d += 1
    elif not i[0]:
        predicted_und += 1

    if i[1]:
        actual_d += 1
    elif not i[1]:
        actual_und += 1