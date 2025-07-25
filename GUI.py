import tkinter
import tkinter.font as font
import time


def display_bring(queue,root):
    
    #root.attributes('-fullscreen',True)
    root.title("display_belong")
    root.configure(bg="white")
    root.geometry("400x300")

    #待機中の文字
    font_standby_text = font.Font(family="DejaVu Sans Mono",size=20,weight="bold")
    standby_text = tkinter.Label(text="待機中",foreground='#ff0000',background='#ffffff',font=font_standby_text)
    display(standby_text,100,100)

    #検知中の文字
    font_detecting_text = font.Font(family="DejaVu Sans Mono",size=20,weight="bold")
    detecting_text = tkinter.Label(text="検知中",foreground='#ff0000',background='#ffffff',font=font_detecting_text)
    hidden(detecting_text)

    #検知結果の文字
    font_result_text1 = font.Font(family="DejaVu Sans Mono",size=20,weight="bold")
    result_phone1 = tkinter.Label(text="スマホあり",foreground='#ff0000',background='#ffffff',font=font_result_text1)
    hidden(result_phone1)

    result_phone2 = tkinter.Label(text="スマホなし",foreground='#ff0000',background='#ffffff',font=font_result_text1)
    hidden(result_phone2)

    font_result_text2 = font.Font(family="DejaVu Sans Mono",size=20,weight="bold")
    result_wallet1 = tkinter.Label(text="財布あり",foreground='#ff0000',background='#ffffff',font=font_result_text2)
    hidden(result_wallet1)

    result_wallet2 = tkinter.Label(text="財布なし",foreground='#ff0000',background='#ffffff',font=font_result_text2)
    hidden(result_wallet2)
    
    display_text = [standby_text,detecting_text]
    result_text = [result_phone1,result_phone2,result_wallet1,result_wallet2]

    event_catch(queue,root,display_text,result_text)

    root.mainloop()


def event_catch(queue,root,display_text,result_text):
    if(not(queue.qsize()==0)):
        received_data = queue.get()
       
        if(isinstance(received_data,bool) and received_data):
            #文字の書き換え
            hidden(display_text[0])
            display(display_text[1],100,100)
        else:
            hidden(display_text[1])
            bluetoothTag_judg(received_data,result_text)
            display(display_text[0],100,100)
    root.after(100,event_catch,queue,root,display_text,result_text)


def bluetoothTag_judg(received_data,result_text):
    AirTag_white_Mac = "4c:e1:00:38:10:36"
    AirTag_black_Mac = "4c:e1:00:36:07:81"
    white=False
    black=False
    
    for dev in received_data:
        if(dev.addr==AirTag_white_Mac):
            display(result_text[0],100,70)
            white=True
        if(dev.addr==AirTag_black_Mac):
            display(result_text[2],100,110)  
            black=True        
    
    if(not(white)):
        display(result_text[1],100,70)
    if(not(black)):
        display(result_text[3],100,110)

    time.sleep(10)
    if(not(white) and not(black)):
        hidden(result_text[1])
        hidden(result_text[3])
    elif(white and black):
        hidden(result_text[0])
        hidden(result_text[2])
    elif(white and not(black)):
        hidden(result_text[0])
        hidden(result_text[3])
    elif(not(white) and black):
        hidden(result_text[1])
        hidden(result_text[2])
    
            
#文字表示関数:
def hidden(target_text):
    target_text.forget()


def display(target_text,X,Y):
    target_text.place(x=X,y=Y)