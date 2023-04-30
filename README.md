# Scientific Calculator with Python and Tkinter

This is a simple scientific calculator created with Python and Tkinter. It can perform various mathematical operations and can be used as a replacement for the default Windows 8.1 scientific calculator.

## Requirements

To run this program, you need to have Python and Tkinter installed on your system.

## How is it made?

1. Import the necessary libraries, tkinter for GUI and math for some mathematical operations.
2. Declare some variables - memory for the memory, equation where we store the equation at the moment and current where we store the current result.
3. Create the main window. We want it not to be resizable and we give it a title Scientific Calculator.
4. Add widgets to the window.
   1. Label - show the current equation
   2. Entry - Enter new operand or see the current result
   3. All buttons

## Adding some names

1. memory - stores the memory data / integer
2. temp_result - stores the temporary result / integer
3. equation - stores the current equation / string
4. counter - stores the step of the operation / integer
5. history - stores all operations / dictionary key("equation") - value("result")
6. number - stores a flag that shows if the user continues to enter only digits that build a number / boolean

## Signs

There are three groups of sign

1. **Operator that ends the equation:** "="
2. **Unary operators (require only one parameter):** Square root (e.g., "√"), Sine (e.g., "sin"), Cosine (e.g., "cos"), Tangent (e.g., "tan"), Inverse sine (e.g., "asin" or "sin⁻¹"), Inverse cosine (e.g., "acos" or "cos⁻¹"), Inverse tangent (e.g., "atan" or "tan⁻¹"), Hyperbolic sine (e.g., "sinh"), Hyperbolic cosine (e.g., "cosh"), Hyperbolic tangent (e.g., "tanh"), Natural logarithm (e.g., "ln"), Logarithm base 10 (e.g., "log"), Exponential (e.g., "exp"), Factorial (e.g., "n!"), Reciprocal (e.g., "1/x"), Square (e.g., "x^2"), Cube (e.g., "x^3"), Raise to the power of 10 (e.g., "10^x")
3. **Binary operators (require an entry of a new number):** Addition (e.g., "+"), Subtraction (e.g., "-"), Multiplication (e.g., "\*"), Division (e.g., "/"), Modulus (e.g., "Mod"), Exponentiation (e.g., "x^y"), Root with custom exponent (e.g., "y√")
