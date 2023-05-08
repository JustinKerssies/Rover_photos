from tkinter import *
root = Tk()
leftFrame = Frame(root)
leftFrame.pack(side=LEFT, expand=True, fill='both')
rightFrame = Frame(root)
rightFrame.pack(side=RIGHT, expand=True, fill='both')

button1 = Button(leftFrame,text="Round 1",fg="white",bg="black")
button2 = Button(leftFrame,text="Round 2",fg="yellow",bg="blue")
button3 = Button(leftFrame,text="Round 3",fg="purple",bg="cyan")
button4 = Button(leftFrame,text="Round 4",fg="green",bg="orange")

button1.pack(expand=True,fill='both')
button2.pack(expand=True,fill='both')
button3.pack(expand=True,fill='both')
button4.pack(expand=True,fill='both')

root.mainloop()