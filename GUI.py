import tkinter
import tkinter.font as font


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
    #検知結果の文字
    font_result_text1 = font.Font(family="DejaVu Sans Mono",size=20,weight="bold")
    result_text2 = tkinter.Label(text="スマホあり",foreground='#ff0000',background='#ffffff',font=font_result_text1)
    font_result_text2 = font.Font(family="DejaVu Sans Mono",size=20,weight="bold")
    result_text2 = tkinter.Label(text="財布あり",foreground='#ff0000',background='#ffffff',font=font_result_text2)
    

    event_catch(queue,standby_text,root,detecting_text)

    root.mainloop()


def event_catch(queue,display_text,root,detecting_text):
    if(not(queue.qsize()==0)):
        received_data = queue.get()
       
        if(isinstance(received_data,bool) and received_data):
            #文字の書き換え
            hidden(detecting_text)
            display()
        else:
            bluetoothTag_judg(received_data,display_text)
    root.after(100,event_catch,queue,display_text,root)


def bluetoothTag_judg(received_data,display_text):
    AirTag_white_Mac = "4c:e1:00:38:10:36"
    AirTag_black_Mac = "4c:e1:00:36:07:81"
    
    display_text.place_forget()
    for dev in received_data:
        if(dev.addr==AirTag_white_Mac):
            belong_display=tkinter.Label(text="財布あり",background='#FFFFFF')
            belong_display.place(x=150,y=150)
        #else:
        #    belong_display3=tkinter.Label(text="財布なし",background='#FFFFFF')
        #    belong_display3.place(x=150,y=150)
        if(dev.addr==AirTag_black_Mac):
            belong_display2=tkinter.Label(text="スマホあり",background='#FFFFFF')
            belong_display2.place(x=150,y=200)
        #else:
        #    belong_display4=tkinter.Label(text="スマホなし",background='#FFFFFF')
        #    belong_display4.place(x=150,y=200)
            
            
#文字表示関数:
def hidden(target_text):
    target_text.forget()


def display(target_text,X,Y):
    target_text.place(x=X,y=Y)



#待機画面
#スキャン中の画面
#結果の画面
