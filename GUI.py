from tkinter import *
from tkinter import ttk
import threading


def display_bring(event):
    root = Tk()
    #root.attributes('-fullscreen',True)
    root.configure(bg="white")
    text_variable = root.StringVar()
    text_variable.set("初期メッセージ")
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text=text_variable).grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

    signal_reception_thread = threading.Thread(target=Signal_reception,args=(event))
    signal_reception_thread.start()

    root.mainloop()


def Signal_reception(event):
    event.wait()
