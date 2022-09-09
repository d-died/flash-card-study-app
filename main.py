from tkinter import *
import random
import pandas as pd

# ---------------------- Access New Word --------------------
def new_word():
    global current, vocab_list, timer
    window.after_cancel(timer)
    # I COULD do it this way, but it's harder to specify "English" vs "French" then when flipping the card
    # Good to note that there are many different ways you can import and read data with pandas
    # french_dict = {row.French: row.English for (index, row) in french_data.iterrows()}
    # random_word = random.choice(list(french_dict.items()))
    # french_word = random_word[0]
    # english_word = random_word[1]

    current = random.choice(vocab_list)
    french_word = current["French"]
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(vocab_word, text=french_word, fill="black")
    canvas.itemconfig(language_title, text="French", fill="black")
    timer = window.after(3000, flip_card)

# -------------------3 Second Countdown-------------------------
def flip_card():
    global current
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(language_title, text="English", fill="white")
    canvas.itemconfig(vocab_word, text=current["English"], fill="white")

# -------------------Remembered the word-------------------------
def learned_word():
    # Remove the current card tuple
    vocab_list.remove(current)
    # Create a new df out of the remaining list
    df = pd.DataFrame(vocab_list)
    # Save the df as a csv to the file
    df.to_csv("./data/words_to_learn.csv", index=False)
    # Pick a new word
    new_word()


BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

current = {}
timer = window.after(3000, flip_card)

# Card front
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front)
language_title = canvas.create_text(400, 150, fill="black", text="French", font=("Arial", 40, "italic"))
vocab_word = canvas.create_text(400, 263, fill="black", text="word", font=("Arial", 60, "bold"))
canvas.grid(column=0, columnspan=2, row=0)

# Red wrong button
wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=new_word)
wrong_button.grid(column=0, row=1)

# Green right button
right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightbackground=BACKGROUND_COLOR, command=learned_word)
right_button.grid(column=1, row=1)

try:
    french_data = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    french_data = pd.read_csv("./data/french_words.csv")
finally:
    vocab_list = french_data.to_dict(orient="records")


new_word()

window.mainloop()