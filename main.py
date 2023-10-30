import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox
import requests
from PIL import Image
Image.CUBIC = Image.BICUBIC

COUNTDOWN_SECONDS = 15
WORDS_WEBSITE = "https://random-word-api.herokuapp.com/"
WORDS_COUNT = 50


def generate_random_words():
    response = requests.get(WORDS_WEBSITE + f"word?number={WORDS_COUNT}")
    data = response.json()
    ready_transcript = " ".join([str(word) for word in data])
    return ready_transcript


def calculate_speed(example_script, typed_script):
    original_arr = example_script.split(" ")
    typed_arr = typed_script.split(" ")

    correct_words = 0
    incorrect_words = 0
    for i in range(len(typed_arr)):
        if typed_arr[i] == original_arr[i]:
            correct_words += 1
        else:
            incorrect_words += 1
    return [correct_words, incorrect_words]


def countdown(count):
    # Disable timer button
    timer_btn.configure(state="disabled")
    # Focus on input field
    transcript_input.focus()
    # Generate Initial transcript text
    if transcript_text.cget("text") == "":
        random_words = generate_random_words()
        transcript_text.configure(text=random_words)
    # Change text in label
    meter['amountused'] = count

    if count > 0:
        # Call countdown again after 1000ms (1s)
        root.after(1000, countdown, count-1)
        # Change meter value
        meter.configure(amountused=count)
    else:
        # Calculate results
        original_transcript = transcript_text.cget("text")
        typed_text = transcript_input.get()

        # Calculate correct and incorrect words
        correct_incorrect_results = calculate_speed(original_transcript, typed_text)
        correct_words = correct_incorrect_results[0]
        incorrect_words = correct_incorrect_results[1]

        # Calculate GROSS and NET result
        gross_wpm = ((correct_words + incorrect_words) / 5 ) / 0.25
        net_wpm = (correct_words / 5 ) / 0.25

        # Setting final results to the corresponding widgets
        gross_result.configure(text=f"Gross WPM: {gross_wpm}", bootstyle='inverse-primary')
        net_result.configure(text=f"Net WPM: {net_wpm}", bootstyle='inverse-warning')
        correct_words_result.configure(text=f"Correct words: {correct_words}", bootstyle='inverse-success')
        incorrect_words_result.configure(text=f"Incorrect words: {incorrect_words}", bootstyle='inverse-danger')

        # Pop up a message if the use wants to retry or not
        answer = Messagebox.retrycancel(
            message="Do you want to test again??",
            title="Time is up !!!",

        )
        # If None we stop the program
        if answer is None: exit(1)
        # If Retry we clear all fields and load new text script
        if answer == "Retry":
            # Enable timer button
            timer_btn.configure(state="enabled")
            # Clear input field
            transcript_input.delete(0, "end")
            # Clear transcript text example
            transcript_text.configure(text="")
            # Clear result labels
            gross_result.configure(text="", bootstyle='primary')
            net_result.configure(text="", bootstyle='warning')
            correct_words_result.configure(text="", bootstyle='success')
            incorrect_words_result.configure(text="", bootstyle='danger')
            # Reset timer
            meter['amountused'] = 15
        else:
            # If Cancel stop program
            exit(1)


root = tb.Window(themename="darkly")
root.title("Speed Typing Tester")
root.geometry("1000x800")

frame = tk.Frame(root)
frame.pack()

heading = tb.Label(frame, text="SPEED TYPING TESTER", font=("Arial", 40, 'bold'), bootstyle="warning")
heading.grid(row=0, column=0, columnspan=2, pady=20)

transcript_text = tk.Label(frame, bg="orange",font=("Arial", 14), wraplength=500, justify="center")
transcript_text.grid(row=1, column=0, columnspan=2, pady=40)

transcript_input = tb.Entry(frame, bootstyle="default", width=100)
transcript_input.grid(row=2, column=0, columnspan=2)

#Style for button
style = tb.Style()
style.configure('my.TButton', font=("Arial", 20, "bold"))

timer_btn = tb.Button(frame,
                      text='Start',
                      width=20,
                      style='my.TButton',
                      bootstyle="primary",
                      command=lambda: countdown(COUNTDOWN_SECONDS))
timer_btn.grid(row=3, column=0, columnspan=2, pady=20)

meter = tb.Meter(frame, bootstyle="primary",
                 amountused=15,
                 textright=" s",
                 metersize=200,
                 amounttotal=COUNTDOWN_SECONDS)
meter.grid(row=4, column=0, columnspan=2, pady=5)

# SUB FRAME FOR RESULTS
result_frame = tb.Frame(frame)
result_frame.grid(row=5, column=0, columnspan=2, pady=10)

gross_result = tb.Label(result_frame, font=('Arial', 20))
gross_result.grid(row=0, column=0, padx=10)

net_result = tb.Label(result_frame, font=('Arial', 20))
net_result.grid(row=0, column=1, padx=10)

correct_words_result = tb.Label(result_frame, font=('Arial', 20))
correct_words_result.grid(row=0, column=2, padx=10)

incorrect_words_result = tb.Label(result_frame, font=('Arial', 20))
incorrect_words_result.grid(row=0, column=3, padx=10)

root.mainloop()
