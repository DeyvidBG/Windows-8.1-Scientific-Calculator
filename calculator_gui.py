from tkinter import *
from math import sin, cos, tan, sinh, cosh, tanh, log, log10, pi, radians, degrees, factorial

memory = 0
equation = ""
current = 0

# Create window
window = Tk()
window.title("Scientific Calculator")
window.resizable(False,False)

label_text = StringVar(value = "0")
entry_text = StringVar(value = "0")

# Define label where the equation will be shown
label = Label(window, textvariable=label_text)
label.grid(row=0, column=0, columnspan=10, sticky='ew')
entry = Entry(window, textvariable=entry_text, justify='right')
entry.grid(row=1, column=0, columnspan=10, sticky='ew')




# Start the main event loop
window.mainloop()