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

def setPrecision():
    global precision
    precision = ""
    while True:
        try:
            precision = input("Please enter the number of decimal places:")
        except (KeyboardInterrupt, EOFError): 
            print("Input interrupted. Please enter the operand again.")
            continue
        if precision.isnumeric() == False:
            print("Please provide a valid number.")
        elif precision.isnumeric() == True and (int(precision) < 0 or int(precision) > 10):
            print("Please provide a valid number.")
        else:
            precision = int(precision)
            break

print('''
*****************************************************
******** Welcome to our calculator program! *********
*****************************************************

Note: Operations start from 0. Each subsequent
operation will be executed on the previous result.

Our calculator allows you to select the number of
decimal places you would like to use for your 
calculations(the number should be in range 0 and 11).
Please enter the number of decimal places you would 
like to use when prompted.

Please note that using a larger number of decimal
places may result in slower calculation times, but 
will allow for greater precision in your results.

We hope you find our calculator useful and easy to
use. Happy calculating!
''')

setPrecision()

memory = 0
temp_result = 0
equation = "0"
counter = 0
history = {}
counter, history = addToHistory(counter, history, equation, temp_result)

while True:
    print("\nMenu:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Modulo")
    print("6. Square root")
    print("7. Reciprocal")
    print("8. Change sign")
    print("9. Clear")
    print("10. Clear entry")
    print("11. Equal")
    print("12. Memory store")
    print("13. Memory recall")
    print("14. Memory clear")
    print("15. Memory add")
    print("16. Memory subtract")
    print("17. Change precision")
    print("0. Quit")

    choice = None
    while not choice in range(0,18):
        try:
            choice = input("Enter your choice: ")
        except (KeyboardInterrupt, EOFError): 
            print("Input interrupted. Please enter the operand again.")
            continue
        if choice.isnumeric() == False:
            print("Please enter a number.")
            continue
        choice = int(choice)
        if not choice in range(0,18):
            print("Please enter a valid option from the menu.")

    if choice == 0:
        break

    if choice in [1, 2, 3, 4, 5]:
        valid_operand = False
        operand = None
        while not valid_operand:
            try:
                operand = input("Enter the operand: ")
            # except (KeyboardInterrupt, EOFError): 
            #     print("Input interrupted. Please enter the operand again.")
            #     continue
            except: print("Exceptions: " + len(sys.exc_info()))
            if operand.isnumeric():
                operand = Decimal(operand)
                valid_operand = True
            else:
                try:
                    operand = Decimal(operand)
                    valid_operand = True
                except (ValueError, DecimalException):
                    print(f"Invalid input '{operand}'. Please enter a number.")
                    continue

    if choice == 1:
        try:
            temp_result = add(temp_result, operand, precision)
            equation = f"({equation} + {operand})"
            counter, history = addToHistory(counter, history, equation, temp_result)
        except OverflowError as e:
            print(e)
    elif choice == 2:
        try:
            temp_result = subtract(temp_result, operand, precision)
            equation = f"({equation} - {operand})"
            counter, history = addToHistory(counter, history, equation, temp_result)
        except OverflowError as e:
            print(e)
    elif choice == 3:
        try:
            temp_result = multiply(temp_result, operand, precision)
            equation = f"({equation} * {operand})"
            counter, history = addToHistory(counter, history, equation, temp_result)
        except OverflowError as e:
            print(e)
    elif choice == 4:
        try:
            temp_result = divide(temp_result, operand, precision)
            equation = f"({equation} / {operand})"
            counter, history = addToHistory(counter, history, equation, temp_result)
        except ValueError as e:
            print(e)
        except OverflowError as e:
            print(e)
    elif choice == 5:
        try:
            new_result = modulo(temp_result, operand, precision)
            equation = f"({equation}%{operand})"
            temp_result = new_result
            counter, history = addToHistory(counter, history, equation, temp_result)
        except ValueError as e:
            print(e)
        except OverflowError as e:
            print(e)
    elif choice == 6:
        try:
            new_result = sqrt(temp_result, precision)
            equation = f"√({equation})"
            temp_result = new_result
            counter, history = addToHistory(counter, history, equation, temp_result)
        except ValueError as e:
            print(e)
        except OverflowError as e:
            print(e)
    elif choice == 7:
        try:
            temp_result = reciproc(temp_result, precision)
            equation = f"reciproc({equation})"
            counter, history = addToHistory(counter, history, equation, temp_result)
        except ValueError as e:
            print(e)
        except OverflowError as e:
            print(e)
    elif choice == 8:
        try:
            temp_result = change_sign(temp_result, precision)
            equation = f"±({equation})"
            counter, history = addToHistory(counter, history, equation, temp_result)
        except OverflowError as e:
            print(e)
    elif choice == 9:
        print(f"The equation {equation} was cleared. The temporary result is now {0}.")
        temp_result = 0
        equation = "0"
        counter = 0
        counter, history = addToHistory(counter, history, equation, temp_result)
        continue
    elif choice == 10:
        try:
            counter, history, equation, temp_result = clearLastEntry(counter, history)
        except ValueError as e:
            print(e)
    elif choice == 11:
        print(f"{equation} = {temp_result}")
        temp_result = 0
        equation = "0"
        counter, history = clearHistory(counter, history)
        continue
    elif choice == 12:
        print(f"The previous memory value {memory} was overwritten. The new memory value is {temp_result}.")
        memory = temp_result
    elif choice == 13:
        print(f"Memory value: {memory}")
    elif choice == 14:
        memory = 0
        print(f"Memory value was erased. The new memory value is {memory}")
    elif choice == 15:
        memory += temp_result
        print(f"Memory value was updated. The new memory value is {memory}")
    elif choice == 16:
        memory -= temp_result
        print(f"Memory value was updated. The new memory value is {memory}")
    elif choice == 17:
        setPrecision()

    print("Current result:", temp_result)
    print("Equation:", equation)
