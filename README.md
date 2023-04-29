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
6. digit - stores a flag that shows if the user continues to enter only digits that build a number / boolean
