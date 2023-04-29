from tkinter import *
from math import sin, cos, tan, sinh, cosh, tanh, log, log10, pi, radians, degrees, factorial

memory = 0
temp_result = 0
equation = "0"
counter = 0
history = {}

# work with memory
def addToHistory(counter, history, equation, result):
    history[counter] = {"equation": equation, "result": result}
    return counter + 1, history

def clearHistory(counter, history):
    history.clear()
    counter = 0
    return counter, history

def clearLastEntry(counter, history):
    if len(list(history.values())) <= 1:
        raise ValueError("History is empty.")
    else: 
        history.pop(counter-1)
        counter -= 1
        return counter, history, history[counter-1]["equation"], history[counter-1]["result"]

# Create window
window = Tk()
window.title("Scientific Calculator")
window.configure(padx=20, pady=20)
window.resizable(False,False)

# Define size for all columns and rows
for i in range(0, 8):
    window.rowconfigure(i, minsize = 50)

for i in range(0,10):
    window.columnconfigure(i, minsize = 50)

label_text = StringVar(value = "0")
entry_text = StringVar(value = "0")

# Define label where the equation will be shown
label = Label(window, textvariable=label_text)
label.grid(row = 0, column = 0, columnspan = 10, sticky = 'ew')
entry = Entry(window, textvariable=entry_text, justify = 'right')
entry.grid(row = 1, column = 0, columnspan = 10, sticky = 'ew')

# Create angle mode radio buttons
angle_mode = StringVar(value = "deg")
angle_frame = Frame(window, bd = 1, relief=SUNKEN)
angle_frame.grid(row = 2, column = 0, columnspan = 5, sticky = 'ew')
Radiobutton(angle_frame, text = "Deg", variable = angle_mode, value = "deg").grid(row = 0, column = 0)
Radiobutton(angle_frame, text = "Rad", variable = angle_mode, value = "rad").grid(row = 0, column = 1)

# Function that creates button
def create_button(text, row, column, rowspan=1, columnspan=1, on_click=None, width=None):
    btn = Button(window, text=text, width=width)
    if text is None:
        btn.config(state=DISABLED)
    btn.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky='ew')
    if on_click:
        btn.config(command=on_click)
    return btn

# Left-side buttons
buttons_left = [
    ("", 3, 0, 1, 1, None),
    ("Inv", 3, 1, 1, 1, None),
    ("ln", 3, 2, 1, 1, None),
    ("", 3, 3, 1, 1, None),
    ("", 3, 4, 1, 1, None),
    ("Int", 4, 0, 1, 1, None),
    ("sinh", 4, 1, 1, 1, None),
    ("sin", 4, 2, 1, 1, None),
    ("x^2", 4, 3, 1, 1, None),
    ("n!", 4, 4, 1, 1, None),
    ("", 5, 0, 1, 1, None),
    ("cosh", 5, 1, 1, 1, None),
    ("cos", 5, 2, 1, 1, None),
    ("x^y", 5, 3, 1, 1, None),
    ("y√", 5, 4, 1, 1, None),
    ("Pi", 6, 0, 1, 1, None),
    ("tanh", 6, 1, 1, 1, None),
    ("tan", 6, 2, 1, 1, None),
    ("x^3", 6, 3, 1, 1, None),
    ("³√", 6, 4, 1, 1, None),
    ("", 7, 0, 1, 1, None),
    ("Exp", 7, 1, 1, 1, None),
    ("Mod", 7, 2, 1, 1, None),
    ("log", 7, 3, 1, 1, None),
    ("10^x", 7, 4, 1, 1, None),
]

# Right-side buttons
buttons_right = [
    ("MC", 2, 5, 1, 1, None),
    ("MR", 2, 6, 1, 1, None),
    ("MS", 2, 7, 1, 1, None),
    ("M+", 2, 8, 1, 1, None),
    ("M-", 2, 9, 1, 1, None),
    ("", 3, 5, 1, 1, None),
    ("CE", 3, 6, 1, 1, None),
    ("C", 3, 7, 1, 1, None),
    ("±", 3, 8, 1, 1, None),
    ("√", 3, 9, 1, 1, None),
    ("7", 4, 5, 1, 1, None),
    ("8", 4, 6, 1, 1, None),
    ("9", 4, 7, 1, 1, None),
    ("/", 4, 8, 1, 1, None),
    ("%", 4, 9, 1, 1, None),
    ("4", 5, 5, 1, 1, None),
    ("5", 5, 6, 1, 1, None),
    ("6", 5, 7, 1, 1, None),
    ("*", 5, 8, 1, 1, None),
    ("1/x", 5, 9, 1, 1, None),
    ("1", 6, 5, 1, 1, None),
    ("2", 6, 6, 1, 1, None),
    ("3", 6, 7, 1, 1, None),
    ("-", 6, 8, 1, 1, None),
    ("=", 6, 9, 2, 1, None),
    ("0", 7, 5, 1, 2, None),
    (".", 7, 7, 1, 1, None),
    ("+", 7, 8, 1, 1, None),
]

# Display buttons
for (text, row, col, rowspan, columnspan, command) in buttons_left + buttons_right:
    if text is None:
        button = Button(window, state="disabled")
    else:
        button = Button(window, text=text, font=("Arial", 12), command=command)
    button.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky="nsew")

# Start the main event loop
window.mainloop()