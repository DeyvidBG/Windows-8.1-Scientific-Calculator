from tkinter import *
from math import sin, cos, tan, sinh, cosh, tanh, log, log10, pi, radians, degrees, factorial

# Create root window
window = Tk()
window.title("Scientific Calculator")
window.geometry("500x500")

# Create StringVar for entry and label
equation_text = StringVar()
result_text = StringVar()

# Create display label and entry
display_label = Label(window, textvariable=equation_text)
display_label.grid(row=0, column=0, columnspan=10, sticky='ew')
display_entry = Entry(window, textvariable=result_text, justify='right')
display_entry.grid(row=1, column=0, columnspan=10, sticky='ew')

# Create angle mode radio buttons
angle_mode = StringVar(value="deg")
angle_frame = Frame(window, bd=1, relief=SUNKEN)
angle_frame.grid(row=2, column=0, columnspan=5, sticky='w')
Radiobutton(angle_frame, text="Degrees", variable=angle_mode, value="deg").grid(row=0, column=0)
Radiobutton(angle_frame, text="Radians", variable=angle_mode, value="rad").grid(row=0, column=1)

# Create memory buttons
memory_frame = Frame(window)
memory_frame.grid(row=2, column=5, columnspan=5, sticky='e')
Button(memory_frame, text="MC").grid(row=0, column=0)
Button(memory_frame, text="MR").grid(row=0, column=1)
Button(memory_frame, text="MS").grid(row=0, column=2)
Button(memory_frame, text="M+").grid(row=0, column=3)
Button(memory_frame, text="M-").grid(row=0, column=4)

# Create the create_button function
def create_button(text, row, column, rowspan=1, columnspan=1, on_click=None, width=None):
    btn = Button(window, text=text, width=width)
    if text is None:
        btn.config(state=DISABLED)
    btn.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky='ew')
    if on_click:
        btn.config(command=on_click)
    return btn

def on_number_click(number):
    current_text = result_text.get()
    result_text.set(current_text + str(number))

def on_click_square_root():
    # Handle click on the square root button
    try:
        result = sqrt(float(result_text.get()))
        result_text.set(str(result))
    except ValueError:
        result_text.set("Error")


def on_click_percent():
    # Handle click on the percentage button
    try:
        result = float(result_text.get()) / 100
        result_text.set(str(result))
    except ValueError:
        result_text.set("Error")    

def on_click_sin():
    angle = radians(float(result_text.get())) if angle_mode.get() == "rad" else float(result_text.get())
    result_text.set(sin(angle))

def on_click_cos():
    angle = radians(float(result_text.get())) if angle_mode.get() == "rad" else float(result_text.get())
    result_text.set(cos(angle))

def on_click_tan():
    angle = radians(float(result_text.get())) if angle_mode.get() == "rad" else float(result_text.get())
    result_text.set(tan(angle))

def on_click_sinh():
    result_text.set(sinh(float(result_text.get())))

def on_click_cosh():
    result_text.set(cosh(float(result_text.get())))

def on_click_tanh():
    result_text.set(tanh(float(result_text.get())))

def on_click_ln():
    result_text.set(log(float(result_text.get())))

def on_click_log():
    result_text.set(log10(float(result_text.get())))

def on_click_sqrt():
    result_text.set(float(result_text.get()) ** 0.5)

def on_click_square():
    result_text.set(float(result_text.get()) ** 2)

def on_click_power():
    equation_text.set(result_text.get() + " ^ ")
    result_text.set("")

def on_click_equal():
    equation = equation_text.get() + result_text.get()
    try:
        result = str(eval(equation))
        equation_text.set(equation + " = ")
        result_text.set(result)
    except:
        equation_text.set("Error: Invalid equation")
        result_text.set("")

def on_click_clear_entry():
    result_text.set("")

def on_click_clear():
    equation_text.set("")
    result_text.set("")

def on_click_change_sign():
    current_text = result_text.get()
    if current_text.startswith("-"):
        result_text.set(current_text[1:])
    else:
        result_text.set("-" + current_text)

def on_click_inverse():
    current_text = result_text.get()
    if current_text != "0":
        result_text.set(str(1 / float(current_text)))
    else:
        equation_text.set("Error: Division by zero")
        result_text.set("")

def on_click_factorial():
    try:
        result = str(factorial(int(result_text.get())))
        equation_text.set(result_text.get() + "!")
        result_text.set(result)
    except:
        equation_text.set("Error: Invalid input")
        result_text.set("")

def on_click_memory_clear():
    """Handle click on the memory clear button"""
    global memory
    memory = 0


def on_click_memory_recall():
    """Handle click on the memory recall button"""
    global memory
    result_text.set(str(memory))


def on_click_memory_store():
    """Handle click on the memory store button"""
    global memory
    try:
        memory = float(result_text.get())
    except ValueError:
        result_text.set("Error")


def on_click_memory_add():
    """Handle click on the memory add button"""
    global memory
    try:
        memory += float(result_text.get())
    except ValueError:
        result_text.set("Error")


def on_click_memory_subtract():
    """Handle click on the memory subtract button"""
    global memory
    try:
        memory -= float(result_text.get())
    except ValueError:
        result_text.set("Error")

buttons_left = [
    ("", 1, 0, 1, 5, None),
    ("Inv", 2, 1, 1, 1, None),
    ("ln", 2, 2, 1, 1, on_click_log),
    ("", 2, 3, 1, 1, None),
    ("", 2, 4, 1, 1, None),
    ("Int", 3, 0, 1, 1, None),
    ("sinh", 3, 1, 1, 1, None),
    ("sin", 3, 2, 1, 1, on_click_sin),
    ("x^2", 3, 3, 1, 1, lambda: result_text.set(str(float(result_text.get()) ** 2))),
    ("n!", 3, 4, 1, 1, on_click_factorial),
    ("", 4, 0, 1, 1, None),
    ("cosh", 4, 1, 1, 1, None),
    ("cos", 4, 2, 1, 1, on_click_cos),
    ("x^y", 4, 3, 1, 1, on_click_power),
    ("x^(1/y)", 4, 4, 1, 1, None),
    ("Pi", 5, 0, 1, 1, lambda: result_text.set(str(pi))),
    ("tanh", 5, 1, 1, 1, on_click_tanh),
    ("tan", 5, 2, 1, 1, on_click_tan),
    ("x^3", 5, 3, 1, 1, lambda: result_text.set(str(float(result_text.get()) ** 3))),
    ("x^(1/3)", 5, 4, 1, 1, None),
    ("", 6, 0, 1, 1, None),
    ("Exp", 6, 1, 1, 1, None),
    ("Mod", 6, 2, 1, 1, None),
    ("log", 6, 3, 1, 1, on_click_log),
    ("10^x", 6, 4, 1, 1, lambda: result_text.set(str(10 ** float(result_text.get())))),
]

buttons_right = [
    ("MC", 2, 7, 1, 1, on_click_memory_clear),
    ("MR", 2, 8, 1, 1, on_click_memory_recall),
    ("MS", 2, 9, 1, 1, on_click_memory_store),
    ("M+", 2, 10, 1, 1, on_click_memory_add),
    ("M-", 3, 7, 1, 1, on_click_memory_subtract),
    ("CE", 3, 8, 1, 1, on_click_clear_entry),
    ("C", 3, 9, 1, 1, on_click_clear),
    ("+-", 3, 10, 1, 1, on_click_change_sign),
    ("sqrt", 4, 7, 1, 1, on_click_square_root),
    ("7", 4, 8, 1, 1, lambda: on_number_click(7)),
    ("8", 4, 9, 1, 1, lambda: on_number_click(8)),
    ("9", 4, 10, 1, 1, lambda: on_number_click(9)),
    ("/", 5, 7, 1, 1, lambda: on_number_click("/")),
    ("%", 5, 8, 1, 1, on_click_percent),
    ("4", 5, 9, 1, 1, lambda: on_number_click(4)),
    ("5", 5, 10, 1, 1, lambda: on_number_click(5)),
    ("*", 6, 7, 1, 1, lambda: on_number_click("*")),
    ("1/x", 6, 8, 1, 1, on_click_inverse),
    ("1", 6, 9, 1, 1, lambda: on_number_click(1)),
    ("2", 6, 10, 1, 1, lambda: on_number_click(2)),
    ("-", 7, 7, 1, 1, lambda: on_number_click("-")),
    ("=", 7, 8, 2, 2, on_click_equal),
    ("0", 8, 7, 1, 2, lambda: on_number_click(0)),
    (".", 8, 9, 1, 1, lambda: on_number_click(".")),
    ("+", 8, 10, 1, 1, lambda: on_number_click("+")),
]

angle_mode = StringVar()
angle_mode.set("deg")
equation_text = StringVar()
result_text = StringVar()

entry_label = Label(window, textvariable=equation_text, anchor="e", font=("Arial", 12))
entry_label.grid(row=0, column=0, columnspan=5, sticky="nsew")

result_entry = Entry(window, textvariable=result_text, font=("Arial", 16), justify="right")
result_entry.grid(row=1, column=0, columnspan=10, sticky="nsew")

angle_frame = Frame(window)
angle_frame.grid(row=2, column=0, columnspan=5, sticky="w")

deg_radio = Radiobutton(angle_frame, text="Deg", variable=angle_mode, value="deg")
deg_radio.pack(side="left")

rad_radio = Radiobutton(angle_frame, text="Rad", variable=angle_mode, value="rad")
rad_radio.pack(side="left")

for (text, row, col, rowspan, columnspan, command) in buttons_left:
    if text is None:
        button = Button(window, state="disabled")
    else:
        button = Button(window, text=text, font=("Arial", 12), command=command)
    button.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky="nsew")

for (text, row, col, rowspan, columnspan, command) in buttons_right:
    if text is None:
        button = Button(window, state="disabled")
    else:
        button = Button(window, text=text, font=("Arial", 12), command=command)
    button.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky="nsew")

# Start the main event loop
window.mainloop()