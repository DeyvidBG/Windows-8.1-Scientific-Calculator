from tkinter import *
from tkinter import messagebox
import math
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

@check_overflow
def sin(a, precision):
    global angle_mode
    if angle_mode == "deg":
        a = math.radians(a)
    return round(Decimal(math.sin(a)), precision)

@check_overflow
def cos(a, precision):
    global angle_mode
    if angle_mode == "deg":
        a = math.radians(a)
    return round(Decimal(math.sin(a)), precision)

@check_overflow
def tan(a, precision):
    global angle_mode
    if angle_mode == "deg":
        a = math.radians(a)
    if math.cos(a) == 0:
        raise ValueError("Undefined: tan is not defined for angles where cos(angle) = 0.")
    else: return round(Decimal(math.tan(a)), precision)

@check_overflow
def sinh(a, precision):
    return round(Decimal(math.sinh(a)), precision)

@check_overflow
def cosh(a, precision):
    return round(Decimal(math.cosh(a)), precision)

@check_overflow
def tanh(a, precision):
    return round(Decimal(math.tanh(a)), precision)

@check_overflow
def ln(a, precision):
    if a <= 0:
        raise ValueError("Undefined: ln(x) is not defined for x <= 0.")
    return round(Decimal(math.log(a)), precision)

@check_overflow
def log(a, precision):
    if a <= 0:
        raise ValueError("Undefined: log10(x) is not defined for x <= 0.")
    return round(Decimal(math.log10(a)), precision)

@check_overflow
def exp(a, precision):
    return round(Decimal(math.exp(a)), precision)

@check_overflow
def factorial(a, precision):
    if a < 0 or int(a) != a:
        raise ValueError("Undefined: Factorial is only defined for non-negative integers.")
    return round(Decimal(math.factorial(a)), precision)

@check_overflow
def square(a, precision):
    return round(Decimal(a ** 2), precision)

@check_overflow
def cube(a, precision):
    return round(Decimal(a ** 3), precision)

@check_overflow
def cube_root(a, precision):
    return round(Decimal(a ** (1/3), precision))

@check_overflow
def nth_root(a, b, precision):
    if a == 0 and b <= 0:
        raise ValueError("Undefined: The root of 0 is not defined for non-positive values of y.")
    if b == 0:
        raise ZeroDivisionError("Undefined: Division by zero is not allowed.")
    return round(Decimal(a ** (1 / b), precision))

@check_overflow
def modulo(a, b, precision):
    if b == 0:
        raise ZeroDivisionError("Undefined: Division by zero is not allowed.")
    return round(Decimal(a % b), precision)

@check_overflow
def exponentiation(a, b, precision):
    if a == 0 and b <= 0:
        raise ValueError("Undefined: 0 raised to a negative power or 0 is not defined.")
    return round(Decimal(a ** b), precision)

memory = 0
disabled = DISABLED
temp_result = 0
equation = ""
counter = 0
history = {}
new_equation = True
number = True
current_operator = None
angle_mode = "deg"

# work with memory
def add_to_history(counter, history, equation, result):
    history[counter] = {"equation": equation, "result": result}
    counter += 1
    return counter, history

def clear_history(counter, history):
    history.clear()
    counter = 0
    return counter, history

def clear_last_entry(counter, history):
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
Radiobutton(angle_frame, text = "Deg", variable = angle_mode, value = "deg", command=lambda: change_angle_mode("deg")).grid(row = 0, column = 0)
Radiobutton(angle_frame, text = "Rad", variable = angle_mode, value = "rad", command=lambda: change_angle_mode("rad")).grid(row = 0, column = 1)

buttons = {}

def disable_button(text):
    button = buttons.get(text)
    if button:
        button.config(state=DISABLED)

def enable_button(text):
    button = buttons.get(text)
    if button:
        button.config(state=NORMAL)

# define functionalities

def add_digit(digit):
    global number, entry_text
    # first check if the last entry was a digit
    if number == True:
        entry_text.set(entry_text.get() + str(digit))
    else:
        entry_text.set(str(digit))
        number = True

#define types of the operators more info in README.md
unary_operators = ["√", "sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "ln", "log", "exp", "n!", "1/x", "x^2", "x^3", "10^x"]
binary_operators = ["+", "-", "*", "/", "Mod", "x^y", "y√"]

def update_data(temp_result, equation):
    global counter, history
    entry_text.set("")
    label_text.set(equation) 
    counter, history = add_to_history(counter, history, equation, temp_result)

def add_operator(operator):
    global temp_result, equation, counter, history, new_equation, number, current_operator, label_text, entry_text
    #check if is a new equation
    if new_equation == True:
        temp_result += Decimal(entry_text.get())
        equation = entry_text.get()
        entry_text.set("")
        label_text.set(equation)
        new_equation = False
        counter, history = add_to_history(counter, history, equation, temp_result)

    if operator == "=":
        equation = equation + "=" + str(temp_result)
        label_text.set(equation)
        entry_text.set(str(temp_result))
        temp_result = 0
        equation = ""
        counter = 0
        history = {}
        new_equation = True

    if current_operator != None:
        if current_operator == "+":
            temp_result = add(temp_result, Decimal(entry_text.get()), 2)
            equation += entry_text.get()
            update_data(temp_result, equation)
        elif current_operator == "-":
            temp_result = subtract(temp_result, Decimal(entry_text.get()), 2)
            equation += entry_text.get()
            update_data(temp_result, equation)
        elif current_operator == "*":
            temp_result = multiply(temp_result, Decimal(entry_text.get()), 2)
            equation += entry_text.get()
            update_data(temp_result, equation)
        elif current_operator == "/":
            try:
                temp_result = divide(temp_result, Decimal(entry_text.get()), 2)
                equation += entry_text.get()
                update_data(temp_result, equation)
            except ValueError as e:
                messagebox.showerror('Calculator Error', 'Error: ' + str(e))
        elif current_operator == "Mod":
            try:
                temp_result = modulo(temp_result, Decimal(entry_text.get()), 2)
                equation = "(" + equation + ")%" + str(Decimal(entry_text.get()))
            except ZeroDivisionError as e:
                messagebox.showerror('Calculator Error', 'Error: ' + str(e))
        elif current_operator == "x^y":
            try:
                temp_result = modulo(temp_result, Decimal(entry_text.get()), 2)
                equation = "(" + equation + ")^" + str(Decimal(entry_text.get()))
            except ValueError as e:
                messagebox.showerror('Calculator Error', 'Error: ' + str(e))
        elif current_operator == "y√":
            try:
                temp_result = modulo(temp_result, Decimal(entry_text.get()), 2)
                equation = str(Decimal(entry_text.get())) + "√(" + equation + ")"
            except ValueError as e:
                messagebox.showerror('Calculator Error', 'Error: ' + str(e))
            except ZeroDivisionError as e:
                messagebox.showerror('Calculator Error', 'Error: ' + str(e))
    current_operator = None

    if operator in unary_operators and current_operator == None:
        if operator == "√":
            try:
                temp_result = sqrt(temp_result, 2)
                equation = "√(" + label_text.get() + ")"
                update_data(temp_result, equation)
            except ValueError as e:
                messagebox.showerror('Calculator Error', 'Error: ' + str(e))
            except OverflowError as e:
                messagebox.showerror('Calculator Error', 'Error: ' + str(e))
        elif operator == "sin":
            temp_result = sin(temp_result, 2)
            equation = "sin(" + label_text.get() + ")"
            update_data(temp_result, equation)
        elif operator == "sinh":
            temp_result = sinh(temp_result, 2)
            equation = "sinh(" + label_text.get() + ")"
            update_data(temp_result, equation)
        elif operator == "cos":
            temp_result = cos(temp_result, 2)
            equation = "cos(" + label_text.get() + ")"
            update_data(temp_result, equation)
        elif operator == "cosh":
            temp_result = cosh(temp_result, 2)
            equation = "cosh(" + label_text.get() + ")"
            update_data(temp_result, equation)
        elif operator == "tan":
            try:
                temp_result = tan(temp_result, 2)
                equation = "tan(" + label_text.get() + ")"
                update_data(temp_result, equation)
            except ValueError as e:
                messagebox.showerror('Calculator Error', 'Error: ' + str(e))
        elif operator == "ln":
            try:
                temp_result = ln(temp_result, 2)
                equation = "tan(" + label_text.get() + ")"
                update_data(temp_result, equation)
            except ValueError as e:
                messagebox.showerror('Calculator Error', 'Error: ' + str(e))
        elif operator == "log":
            try:
                temp_result = log(temp_result, 2)
                equation = "log(" + label_text.get() + ")"
                update_data(temp_result, equation)
            except ValueError as e:
                messagebox.showerror('Calculator Error', 'Error: ' + str(e))
        elif operator == "exp":
            try:
                temp_result = exp(temp_result, 2)
                equation = "exp(" + label_text.get() + ")"
                update_data(temp_result, equation)
            except ValueError as e:
                messagebox.showerror('Calculator Error', 'Error: ' + str(e))
        elif operator == "n!":
            try:
                temp_result = factorial(temp_result, 2)
                equation = "(" + label_text.get() + ")!"
                update_data(temp_result, equation)
            except ValueError as e:
                messagebox.showerror('Calculator Error', 'Error: ' + str(e))
        elif operator == "x^2":
            temp_result = square(temp_result, 2)
            equation = "(" + label_text.get() + ")^2"
            update_data(temp_result, equation)
        elif operator == "x^3":
            temp_result = cube(temp_result, 2)
            equation = "(" + label_text.get() + ")^3"
            update_data(temp_result, equation)
        elif operator == "1/x":
            try:
                temp_result = reciproc(temp_result, 2)
                equation = "reciproc(" + label_text.get() + ")"
                update_data(temp_result, equation)
            except ValueError as e:
                messagebox.showerror('Calculator Error', 'Error: ' + str(e))
        elif operator == "³√":
            temp_result = cube_root(temp_result, 2)
            equation = "³√(" + label_text.get() + ")"
            update_data(temp_result, equation)
        elif operator == "±":
            temp_result = change_sign(temp_result)
            equation = "±(" + label_text.get() + ")"
            update_data(temp_result, equation)
        else: messagebox.showerror('Calculator Error', 'You have already chose an operator that requires second argument, please add the second argument and after the execution you will be able to reverse the last operation.')

    if operator in binary_operators and current_operator == None:
        current_operator = operator
        equation += current_operator
        label_text.set(equation)


def memory_operator(operator):
    global memory, temp_result
    if operator == "MC":
        memory = None
        disable_button("MC")
        disable_button("MR")
        disable_button("M+")
        disable_button("M-")
    elif operator == "MR":
        entry_text.set(str(memory))
    elif operator == "MS":
        memory = temp_result
        enable_button("MC")
        enable_button("MR")
        enable_button("M+")
        enable_button("M-")
    elif operator == "M+":
        memory += temp_result
    elif operator == "M-":
        memory -= temp_result


def clear_entry(type):
    global temp_result, equation, counter, history, new_equation
    if type == "partially":
        try:
            counter, history, equation, temp_result = clear_last_entry(counter, history)
            label_text.set(equation)
            entry_text.set("")
        except ValueError as e:
            messagebox.showinfo("Info", str(e))
    elif type == "fully":
        counter, history = clear_history(counter, history)
        temp_result = 0
        equation = ""
        new_equation = True
        label_text.set("")
        entry_text.set("")

def change_angle_mode(type):
    global angle_mode
    angle_mode = type

# Left-side buttons
buttons_left = [
    ("", DISABLED, 3, 0, 1, 1, None),
    ("Inv", NORMAL, 3, 1, 1, 1, None),
    ("ln", NORMAL, 3, 2, 1, 1, lambda: add_operator("ln")),
    ("", DISABLED, 3, 3, 1, 1, None),
    ("", DISABLED, 3, 4, 1, 1, None),
    ("Int", NORMAL, 4, 0, 1, 1, None),
    ("sinh", NORMAL, 4, 1, 1, 1, lambda: add_operator("sinh")),
    ("sin", NORMAL, 4, 2, 1, 1, lambda: add_operator("sin")),
    ("x^2", NORMAL, 4, 3, 1, 1, lambda: add_operator("x^2")),
    ("n!", NORMAL, 4, 4, 1, 1, lambda: add_operator("n!")),
    ("", DISABLED, 5, 0, 1, 1, None),
    ("cosh", NORMAL, 5, 1, 1, 1, lambda: add_operator("cosh")),
    ("cos", NORMAL, 5, 2, 1, 1, lambda: add_operator("cos")),
    ("x^y", NORMAL, 5, 3, 1, 1, lambda: add_operator("x^y")),
    ("y√", NORMAL, 5, 4, 1, 1, lambda: add_operator("y√")),
    ("Pi", NORMAL, 6, 0, 1, 1, None),
    ("tanh", NORMAL, 6, 1, 1, 1, lambda: add_operator("tanh")),
    ("tan", NORMAL, 6, 2, 1, 1, lambda: add_operator("tan")),
    ("x^3", NORMAL, 6, 3, 1, 1, lambda: add_operator("x^3")),
    ("³√", NORMAL, 6, 4, 1, 1, lambda: add_operator("³√")),
    ("", DISABLED, 7, 0, 1, 1, None),
    ("Exp", NORMAL, 7, 1, 1, 1, lambda: add_operator("exp")),
    ("Mod", NORMAL, 7, 2, 1, 1, lambda: add_operator("Mod")),
    ("log", NORMAL, 7, 3, 1, 1, lambda: add_operator("log")),
    ("10^x", NORMAL, 7, 4, 1, 1, None),
]

# Right-side buttons
buttons_right = [
    ("MC", DISABLED, 2, 5, 1, 1, lambda: memory_operator("MC")),
    ("MR", DISABLED, 2, 6, 1, 1, lambda: memory_operator("MR")),
    ("MS", NORMAL, 2, 7, 1, 1, lambda: memory_operator("MS")),
    ("M+", DISABLED, 2, 8, 1, 1, lambda: memory_operator("M+")),
    ("M-", DISABLED, 2, 9, 1, 1, lambda: memory_operator("M-")),
    ("", DISABLED, 3, 5, 1, 1, None),
    ("CE", NORMAL, 3, 6, 1, 1, lambda: clear_entry("partially")),
    ("C", NORMAL, 3, 7, 1, 1, lambda: clear_entry("fully")),
    ("±", NORMAL, 3, 8, 1, 1, lambda: add_operator("±")),
    ("√", NORMAL, 3, 9, 1, 1, lambda: add_operator("√")),
    ("7", NORMAL, 4, 5, 1, 1, lambda: add_digit(7)),
    ("8", NORMAL, 4, 6, 1, 1, lambda: add_digit(8)),
    ("9", NORMAL, 4, 7, 1, 1, lambda: add_digit(9)),
    ("/", NORMAL, 4, 8, 1, 1, lambda: add_operator("/")),
    ("%", NORMAL, 4, 9, 1, 1, lambda: add_operator("%")),
    ("4", NORMAL, 5, 5, 1, 1, lambda: add_digit(4)),
    ("5", NORMAL, 5, 6, 1, 1, lambda: add_digit(5)),
    ("6", NORMAL, 5, 7, 1, 1, lambda: add_digit(6)),
    ("*", NORMAL, 5, 8, 1, 1, lambda: add_operator("*")),
    ("1/x", NORMAL, 5, 9, 1, 1, lambda: add_operator("1/x")),
    ("1", NORMAL, 6, 5, 1, 1, lambda: add_digit(1)),
    ("2", NORMAL, 6, 6, 1, 1, lambda: add_digit(2)),
    ("3", NORMAL, 6, 7, 1, 1, lambda: add_digit(3)),
    ("-", NORMAL, 6, 8, 1, 1, lambda: add_operator("-")),
    ("=", NORMAL, 6, 9, 2, 1, lambda: add_operator("=")),
    ("0", NORMAL, 7, 5, 1, 2, lambda: add_digit(0)),
    (".", NORMAL, 7, 7, 1, 1, None),
    ("+", NORMAL, 7, 8, 1, 1, lambda: add_operator("+")),
]

# Display buttons
for (text, disabled, row, col, rowspan, columnspan, command) in buttons_left + buttons_right:
    btn = Button(window, text=text)
    btn.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky='nsew')
    if command:
        buttons[text] = btn
        btn.config(command=command, state=disabled)

# Start the main event loop
window.mainloop()