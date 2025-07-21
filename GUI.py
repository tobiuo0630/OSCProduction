import sys
import tkinter
test = "あいうえお"
root = tkinter.Tk()
root.title(u"software title")
root.geometry("400x300")

static = tkinter.Label(text=test,background='#ffffff')
static.place(x=200,y=150)

root.mainloop()