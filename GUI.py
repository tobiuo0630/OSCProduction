import tkinter
import tkinter.font as font
from PIL import Image
from PIL import ImageTk
from datetime import datetime,time


standby_text_x=780
standby_text_y=500
detecting_text_x = 780
detecting_text_y = 300
party_parrot_x = 880
party_parrot_y = 600
result_white_x = 650 
result_white_y = 400
result_black_x = 650
result_black_y = 600
pp_path = "gifImage/parrot.gif"

#gif画像の描画、制御を行うクラス
class GifPlayer:
    def __init__(self, root, gif_path):
        self.root = root
        self.label = tkinter.Label(root,background='#ffffff')
        self.is_stopped = False  # アニメーションを停止するためのフラグ

        # GIFの情報を読み込む
        gif_image = Image.open(gif_path)
        self.frame_count = gif_image.n_frames
        
        self.frames = []

        for i in range(self.frame_count):
            gif_image.seek(i)
            frame_image = ImageTk.PhotoImage(gif_image.copy())
            self.frames.append(frame_image)
        
        self.delay = gif_image.info.get('duration', 100)
        
        self.ind = 0

    def place(self, x, y):
        """ラベルを配置する"""
        self.label.place(x=x, y=y)

    
    def hid(self):
        self.label.place_forget()

    def start(self):
        """アニメーションを開始する"""
        self.is_stopped = False
        self.update()

    def stop(self):
        """アニメーションを停止する"""
        self.is_stopped = True

    def update(self):
        # 停止フラグがTrueなら、ここで処理を終了する
        if self.is_stopped:
            return

        # フレームを更新する
        frame = self.frames[self.ind]
        self.ind = (self.ind + 1) % self.frame_count # 剰余演算でシンプルに書ける
        self.label.configure(image=frame)

        # 次のフレーム更新を予約する
        self.root.after(self.delay, self.update)


def display_bring(queue,root,com_display_result):
    
    root.attributes('-fullscreen',True)
    root.title("display_belong")
    root.configure(bg="white")
    root.bind('<Escape>',lambda event: exit_fullscreen(event,root))


    thread_kill_specified_time()

    #待機中の文字
    font_standby_text = font.Font(family="DejaVu Sans Mono",size=100,weight="bold")
    standby_text = tkinter.Label(text="待機中",foreground='#87cefa',background='#ffffff',font=font_standby_text)
    display(standby_text,standby_text_x,standby_text_y)

    #検知中の文字
    font_detecting_text = font.Font(family="DejaVu Sans Mono",size=100,weight="bold")
    detecting_text = tkinter.Label(text="検知中",foreground='#ffd700',background='#ffffff',font=font_detecting_text)
    hidden(detecting_text)

    #検知結果の文字
    font_result_text1 = font.Font(family="DejaVu Sans Mono",size=100,weight="bold")
    result_phone1 = tkinter.Label(text="スマホあり",foreground='#00ff00',background='#ffffff',font=font_result_text1)
    hidden(result_phone1)

    result_phone2 = tkinter.Label(text="スマホなし",foreground='#ff0000',background='#ffffff',font=font_result_text1)
    hidden(result_phone2)

    font_result_text2 = font.Font(family="DejaVu Sans Mono",size=100,weight="bold")
    result_wallet1 = tkinter.Label(text="財布あり",foreground='#00ff00',background='#ffffff',font=font_result_text2)
    hidden(result_wallet1)

    result_wallet2 = tkinter.Label(text="財布なし",foreground='#ff0000',background='#ffffff',font=font_result_text2)
    hidden(result_wallet2)

    party_parrot = GifPlayer(root,pp_path)
    party_parrot.hid()
    
    display_text = [standby_text,detecting_text]
    result_text = [result_phone1,result_phone2,result_wallet1,result_wallet2]

    event_catch(queue,root,display_text,result_text,com_display_result,party_parrot)

    root.mainloop()


def event_catch(queue,root,display_text,result_text,com_display_result,party_parrot):
    if(not(queue.qsize()==0)):
        received_data = queue.get()
       
        if(isinstance(received_data,bool) and received_data):
            #文字の書き換え
            hidden(display_text[0])
            party_parrot.place(party_parrot_x,party_parrot_y)
            party_parrot.start()
            display(display_text[1],detecting_text_x,detecting_text_y)
            
            
            #アニメーション
        else:
            hidden(display_text[1])
            party_parrot.hid()
            party_parrot.stop()
            bluetoothTag_judg(root,display_text[0],received_data,result_text,com_display_result)

            
            #display(display_text[0],100,100)
            
    root.after(100,event_catch,queue,root,display_text,result_text,com_display_result,party_parrot)


def bluetoothTag_judg(root,display_text,received_data,result_text,com_display_result):
    AirTag_black_Mac = "4c:e1:00:38:10:36"
    AirTag_white_Mac = "4c:e1:00:36:07:81"
    AirTag_RSSI = -66
    white=False
    black=False

    result_text_allHidden(result_text)
    
    for dev in received_data:
        if(dev.addr==AirTag_white_Mac and dev.rssi>=AirTag_RSSI):
            display(result_text[0],result_white_x,result_white_y)
            white=True
        if(dev.addr==AirTag_black_Mac and dev.rssi>=AirTag_RSSI):
            display(result_text[2],result_black_x,result_black_y)  
            black=True        
    
    if(not(white)):
        display(result_text[1],result_white_x,result_white_y)
    if(not(black)):
        display(result_text[3],result_black_x,result_black_y)
    
    root.after(10000,result_text_allHidden,result_text)
    root.after(10100,display,display_text,standby_text_x,standby_text_y)
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


def exit_fullscreen(event,window):
    window.destroy()


def thread_kill_specified_time(root):

    now_time = datetime.now()
    kill_time = now_time.replace(hour=9,minute=0,second=0,microsecond=0)

    if now_time >= kill_time:
        root.destroy()
    else:
        remaining_ms = int((kill_time - now_time).total_seconds() * 1000)
        root.after(remaining_ms,root.destroy)
        
