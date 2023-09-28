# import scipy.stats as stats
#
# data = train_test.data
# correct = train_test.correct
# predicted_und, predicted_d, actual_d, actual_und = train_test.predicted_und, train_test.predicted_d, train_test.actual_d, train_test.actual_und
# fn, tn, fp, tp = train_test.fn, train_test.tn, train_test.fp, train_test.tp
#
# print(f"Percent correct: {correct / len(data) * 100}%")
# print(f"Total datapoints: {len(data)}")
#
# print(f"Actual Positives: {actual_d} | Actual Negatives: {actual_und} | Predicted Positives: {predicted_d} | Predicted Negatives: {predicted_und}")
# print(f"True Positives: {tp} | False Negatives: {fn} | False Positives: {fp} | True Negatives: {tn}")
#
# chi_square_test_statistic, p_value = stats.chisquare([predicted_und, predicted_d], [actual_und, actual_d])
# print(f'Chi square test statistic: {str(chi_square_test_statistic)}')
# print(f'p-value: {str(p_value)}')
# print(f'Critical value: {stats.chi2.ppf(1 - 0.05, df=1)}')

import tkinter as tk
import importlib
import math

words = {}

# Open the file for reading
with open("training_data.txt", "r") as file:
    # Read each line in the file
    for line in file:
        # Split the line into word and weighting using ':' as the separator
        parts = line.strip().split(':')
        if len(parts) == 2:
            word = parts[0].strip()  # Get the word (trimmed of leading/trailing spaces)
            weighting = float(parts[1].strip())  # Get the weighting (converted to float)
            words[word] = weighting  # Add the word and weighting to the dictionary

def predict(text):
    predict = 0
    for word in text.split(" "):
        if word in words:
            predict += words[word]

    predict = 1 / (1 + math.exp(-predict))
    return predict

# Function to update the training data
def update(update_data, root):
    if update_data:
        try:
            import train_test  # Import the other module if "Yes" is selected
            importlib.reload(train_test)  # Reload the module in case it has already been imported
            print("Training data updated.")
        except ImportError:
            print("Error importing the module.")
    else:
        print("Training data not updated.")

    # Close the main window
    root.destroy()

    # Create a new window to prompt the user for text
    prompt_window = tk.Tk()
    prompt_window.title("Adam Stepansky's BPD/ASPD Prediction Model")
    prompt_window.geometry("500x500")

    # Create a label to instruct the user
    label = tk.Label(prompt_window, text="Enter the text to be analyzed:\n(it can be a collection of multiple texts, and does not need a separator)\nNOTE: THE MORE TEXT, THE MORE ACCURATE THE PREDICTION")
    label.pack(pady=10)

    # Create a scalable text entry widget
    text_widget = tk.Text(prompt_window, height=10, width=40)
    text_widget.pack(pady=10)

    # Function to handle text submission
    def submit_text():
        user_text = text_widget.get("1.0", tk.END)  # Get text from the widget
        if user_text:
            prediction_label.config(text=f"Probability of diagnosis: {predict(user_text):.4f} ({predict(user_text)*100:.2f}%)")

    # Create a submit button
    submit_button = tk.Button(prompt_window, text="Submit", command=submit_text)
    submit_button.pack()

    prediction_label = tk.Label(prompt_window, text="\nProbability of diagnosis: ")
    prediction_label.pack()

    prompt_window.mainloop()


# Create the main window
root = tk.Tk()
root.title("Adam Stepansky's BPD/ASPD Prediction Model")
root.geometry("500x500")

# Create a frame to hold the widgets and center it vertically
frame = tk.Frame(root)
frame.pack(expand=True, fill='both')  # Expand to fill available space

# Create a label widget and center it vertically in the frame
label = tk.Label(frame,
                 text="Would you like to update the training data?\n(this may take a few minutes, but will also slightly increase accuracy)")
label.pack(side='top', pady=10)  # Use pady to add vertical spacing

# Create a frame to hold the buttons and center it vertically within the main frame
button_frame = tk.Frame(frame)
button_frame.pack(side='top')

# Create the first button and pack it to the left of the button frame
button1 = tk.Button(button_frame, text="Yes", padx=20, command=lambda: update(True, root))
button1.pack(side='left', padx=10)  # Use padx to add horizontal spacing

# Create the second button and pack it to the left of the button frame
button2 = tk.Button(button_frame, text="No", padx=20, command=lambda: update(False, root))
button2.pack(side='left', padx=10)  # Use padx to add horizontal spacing

root.mainloop()
