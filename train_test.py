import math
import random
import scraping
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.calibration import calibration_curve

d_posts, und_posts, words = scraping.d_posts, scraping.und_posts, scraping.word_dict
all_posts = d_posts + und_posts

# Split the data into train and test sets
train_posts = random.sample(all_posts, int(0.8 * len(all_posts)))
test_posts = [post for post in all_posts if post not in train_posts]

# Train the model
for post in train_posts:
    predict = 0
    for word in set(post.split(" ")):
        if word in words:
            predict += words[word]

    actual = int(post in d_posts)
    predict = 1 / (1 + math.exp(-0.5 * predict))
    change = predict * (1 - predict)

    for word in post.split(" "):
        if actual < predict:
            if word in words:
                words[word] -= change
        else:
            if word in words:
                words[word] += change

# Save the words and their weightings to a file (clearing it if it exists)
with open("training_data.txt", "w") as file:
    for word, weighting in words.items():
        file.write(f"{word}: {weighting}\n")

if __name__ == "__main__":
    # Test the model
    data = []
    for post in test_posts:
        predict = 0
        for word in set(post.split(" ")):
            if word in words:
                predict += words[word]

        actual = int(post in d_posts)
        predict = round(1 / (1 + math.exp(-0.5 * predict)))
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

    # Accuracy
    accuracy = correct / len(test_posts)

    # Precision, Recall, and F1-Score
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    # Confusion Matrix
    confusion_matrix = np.array([[tp, fp], [fn, tn]])

    # Plot the confusion matrix and save it as an image
    plt.figure(figsize=(6, 6))
    plt.imshow(confusion_matrix, interpolation='nearest', cmap=plt.get_cmap('Blues'))
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, ['Predicted Positive', 'Predicted Negative'])
    plt.yticks(tick_marks, ['Actual Positive', 'Actual Negative'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')

    for i in range(2):
        for j in range(2):
            plt.text(j, i, confusion_matrix[i, j], ha='center', va='center', color='black', fontsize=16)

    # Print the metrics
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-Score: {f1_score:.2f}")

    # Compute ROC and AUC
    fpr, tpr, _ = roc_curve([actual for _, actual in data], [predict for predict, _ in data])
    roc_auc = auc(fpr, tpr)

    # Plot the ROC curve
    plt.figure(figsize=(6, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (AUC = {:.2f})'.format(roc_auc))
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC)')
    plt.legend(loc='lower right')

    # Calculate and plot calibration curve
    prob_true, prob_pred = calibration_curve([actual for _, actual in data], [predict for predict, _ in data], n_bins=10)

    plt.figure(figsize=(6, 6))
    plt.plot(prob_pred, prob_true, marker='o', markersize=5, label='Calibration Curve')
    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='gray', label='Perfectly Calibrated')
    plt.xlabel('Mean Predicted Probability')
    plt.ylabel('Fraction of Positives')
    plt.title('Calibration Curve')
    plt.legend(loc='lower right')
    plt.show()

    # Print the metrics
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-Score: {f1_score:.2f}")
    print(f"ROC AUC: {roc_auc:.2f}")
