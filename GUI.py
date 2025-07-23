import tkinter
import sys

#Bluetoothタグのデバイス情報


def display_bring(queue,event,root):
    
    #root.attributes('-fullscreen',True)
    root.title("display_belong")
    root.configure(bg="white")
    root.geometry("400x300")
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
        else:
            bluetoothTag_judg(received_data,display_text)
    root.after(100,event_catch,queue,display_text,root)


def bluetoothTag_judg(received_data,display_text):
    AirTag_white_Mac = "4c:e1:00:38:10:36"
    AirTag_black_Mac = "4c:e1:00:36:07:81"
    temp = "70:5a:6f:63:b2:f7"
    
    display_text.place_forget()
    for dev in received_data:
        if(dev.addr==temp):
            belong_display=tkinter.Label(text="財布あり",background='#FFFFFF')
            belong_display.place(x=150,y=150)
        else:
            belong_display3=tkinter.Label(text="財布なし",background='#FFFFFF')
            belong_display3.place(x=150,y=150)
        if(dev.addr==AirTag_black_Mac):
            belong_display2=tkinter.Label(text="スマホあり",background='#FFFFFF')
            belong_display2.place(x=150,y=200)
        else:
            belong_display4=tkinter.Label(text="スマホなし",background='#FFFFFF')
            belong_display4.place(x=150,y=200)
            
            
