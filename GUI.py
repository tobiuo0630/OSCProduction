import tkinter
import sys

def display_bring(queue,event,root):
    
    #root.attributes('-fullscreen',True)
    root.configure(bg="white")
    display_text = tkinter.Label(text="待機中",background='#ffffff')
    display_text.place(x=100,y=100)
    
    event_catch(queue,display_text,root)

    root.mainloop()


def event_catch(queue,display_text,root):
    if(not(queue.qsize()==0)):
        received_data = queue.get()
        if(isinstance(received_data,bool) and received_data):
            #文字の書き換え
            display_text["text"] = "スキャン中"
        elif(isinstance(received_data,list)):
            #関数（received_data）
    else:
        root.after(100,event_catch,queue,display_text,root)


def bluetoothTag_judg(received_data):
    for dev in received_data:
        if(dev==address)
