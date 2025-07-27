import tkinter
import tkinter.font as font


def display_bring(queue,root,com_display_result):
    
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

    event_catch(queue,root,display_text,result_text,com_display_result)

    root.mainloop()


def event_catch(queue,root,display_text,result_text,com_display_result):
    if(not(queue.qsize()==0)):
        received_data = queue.get()
       
        if(isinstance(received_data,bool) and received_data):
            #文字の書き換え
            hidden(display_text[0])
            display(display_text[1],100,100)
            #アニメーション
        else:
            hidden(display_text[1])
            bluetoothTag_judg(root,display_text[0],received_data,result_text,com_display_result)

            
            #display(display_text[0],100,100)
            
    root.after(100,event_catch,queue,root,display_text,result_text,com_display_result)


def bluetoothTag_judg(root,display_text,received_data,result_text,com_display_result):
    AirTag_black_Mac = "4c:e1:00:38:10:36"
    AirTag_white_Mac = "4c:e1:00:36:07:81"
    white=False
    black=False

    result_text_allHidden(result_text)
    
    for dev in received_data:
        if(dev.addr==AirTag_white_Mac):
            display(result_text[0],200,70)
            white=True
        if(dev.addr==AirTag_black_Mac):
            display(result_text[2],200,110)  
            black=True        
    
    if(not(white)):
        display(result_text[1],200,70)
    if(not(black)):
        display(result_text[3],200,110)
    
    root.after(10000,result_text_allHidden,result_text)
    root.after(10100,display,display_text,100,100)
    root.after(10101,queue_put,com_display_result)

#文字表示関数:
def hidden(target_text):
    target_text.place_forget()


def display(target_text,X,Y):
    target_text.place(x=X,y=Y)


def result_text_allHidden(result_text):
    for i in result_text:
        if(i.winfo_ismapped()):
            i.place_forget()


def queue_put(com_display_result):
    com_result = True
    com_display_result.put(com_result)