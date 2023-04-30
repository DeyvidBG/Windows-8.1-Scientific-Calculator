from tkinter import *
from math import sin, cos, tan, sinh, cosh, tanh, log, log10, pi, radians, degrees, factorial
import sys
from decimal import Decimal, DecimalException

max_float = sys.float_info.max
min_float = -sys.float_info.max

def within_range(value):
    return (value > min_float) and (value < max_float)

def check_overflow(func):
    def wrapper(*args):
        result = func(*args)
        if not within_range(result):
            raise OverflowError("Result is too large or too small to be represented as a float.")
        return result
    return wrapper

@check_overflow
def add(temp, a, precision):
    return round(Decimal(temp + a), precision)

@check_overflow
def subtract(temp, a, precision):
    return round(Decimal(temp - a),precision)

@check_overflow
def multiply(temp, a, precision):
    return round(Decimal(temp * a),precision)

@check_overflow
def divide(temp, a, precision):
    if a == 0:
        '''
        if temp == 0:
            return float('inf')
        '''
        raise ValueError("Division by 0 is not allowed.")
    return round(Decimal(temp / a),precision)

@check_overflow
def modulo(temp, a, precision):
    if a == 0:
        raise ValueError("We cannot get the rest from division by zero.")
    return round(Decimal(math.fmod(temp,a)), precision)

@check_overflow
def sqrt(a, precision):
    if a < 0:
        raise ValueError("Square root of a negative number is not supported.")
    return round(Decimal(math.sqrt(a)), precision)

@check_overflow
def reciproc(a, precision):
    if a == 0:
        raise ValueError("Division by 0 is not allowed.")
    return round(Decimal(1 / a), precision)

@check_overflow
def change_sign(a, precision):
    return round(Decimal(-a), precision)

memory = 0
temp_result = 0
equation = ""
counter = 0
history = {}
new_equation = True
digit = True

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

label_text = StringVar(value = "")
entry_text = StringVar(value = "")

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

# define functionalities

# add number
def add_number(number):
    global digit
    if digit == True:
        entry_text.set(entry_text.get() + str(number))
    else:
        entry_text.set(str(number))
        digit = True

# add operator
def add_operator(operator):
    global temp_result, equation, counter, digit
    if digit == True:
        digit = False
        counter+=1
        if operator in ["+","-","*","/"]:
            equation += entry_text.get()
            if counter == 1:
                temp_result += int(entry_text.get())
                equation += operator
                entry_text.set("")
                label_text.set(equation)
            elif operator == "=":
                entry_text.set(str(temp_result))
                label_text.set(equation + "=" + str(temp_result))



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
    ("7", 4, 5, 1, 1, lambda: add_number(7)),
    ("8", 4, 6, 1, 1, lambda: add_number(8)),
    ("9", 4, 7, 1, 1, lambda: add_number(9)),
    ("/", 4, 8, 1, 1, lambda: add_operator("/")),
    ("%", 4, 9, 1, 1, lambda: add_operator("%")),
    ("4", 5, 5, 1, 1, lambda: add_number(4)),
    ("5", 5, 6, 1, 1, lambda: add_number(5)),
    ("6", 5, 7, 1, 1, lambda: add_number(6)),
    ("*", 5, 8, 1, 1, lambda: add_operator("*")),
    ("1/x", 5, 9, 1, 1, None),
    ("1", 6, 5, 1, 1, lambda: add_number(1)),
    ("2", 6, 6, 1, 1, lambda: add_number(2)),
    ("3", 6, 7, 1, 1, lambda: add_number(3)),
    ("-", 6, 8, 1, 1, lambda: add_operator("-")),
    ("=", 6, 9, 2, 1, None),
    ("0", 7, 5, 1, 2, lambda: add_number(0)),
    (".", 7, 7, 1, 1, None),
    ("+", 7, 8, 1, 1, lambda: add_operator("+")),
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