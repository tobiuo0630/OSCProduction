import RPi.GPIO as GPIO
import time
import sys
from bluepy.btle import Scanner, DefaultDelegate
from tkinter import *
from tkinter import ttk
import threading



trig_pin =15 #GPIO(General Purpose input/output(汎用入出力）) 15 command to emit ultrasound
echo_pin = 14 #GPIO 14 returns reflection time
speed_of_sound = 34370 #20℃での音速(cm/s)

#pythonでGPIOピンを安全かつ意図通りに使うための初期化設定
GPIO.setmode(GPIO.BCM)#Broadcom SOC channel ピンの指定を物理的な位置１番２番ではなくCPUの機能番号GPIO2,3として扱う
GPIO.setwarnings(False)#GPIO操作を繰り返すと出る警告メッセージ（このピンは使用中です）を非表示にする
GPIO.setup(trig_pin,GPIO.OUT)#.setupは入出力の指定 ラズパイから超音波センサへtrig_pinからトリガー信号を送る
GPIO.setup(echo_pin,GPIO.IN)#外部からの電圧をecho_pinで受け取る


class ScanDelegate(DefaultDelegate):
    Earfun_Air_MacAddress = "70:5a:6f:63:b2:f7"
    
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):#dev 発見したデバイスの情報(MAC) isNewDev デバイスの初回発見時True isNewData 発見済みのデバイスから新規データ受診時 True
        if isNewDev:
            if(dev.addr==self.Earfun_Air_MacAddress and dev.rssi>=-50):
                print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
                display_bring(dev.addr)
                
                
        elif isNewData:
            print("Received new data from", dev.addr)    


def get_distance():
    GPIO.output(trig_pin, GPIO.HIGH)#send ultrasound
    time.sleep(0.000010)#wait this time
    GPIO.output(trig_pin, GPIO.LOW)#stop ultrasound
    
    #超音波センサが超音波を発信して跳ね返りを受信するまでecho_pinはtrue
    while not GPIO.input(echo_pin):#発信するまで待機
        pass
    t1 = time.time()#超音波の発信時間 #trueで計測開始
    
    while GPIO.input(echo_pin):#falseになるまで待機
        pass
    t2 = time.time()#超音波の受信時間 #falseで計測終了
    
    return (t2-t1) * speed_of_sound /2 #時間*速さ=距離(t2-t1は対象物までの往復時間）


def display_bring():
    root = Tk()
    #root.attributes('-fullscreen',True)
    root.configure(bg="white")
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text=default_text).grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    root.mainloop()
  
def print_test():
    while True:
        try:
            print(1)
            time.sleep(5)
        
        except KeyboardInterrupt:
            sys.exit()
    
    
def Ultrasonic_scan():
    while True:
        try:
            distance = '{:.1f}'.format(get_distance())
            print("Distance: " + distance + "cm")
            if(float(distance)<=5.0):
               global default_text
               default_text = "スキャン中"
               print_test()
            time.sleep(5)
            
        except KeyboardInterrupt:
            GPIO.cleanup()
            sys.exit()


scanner = Scanner().withDelegate(ScanDelegate())
default_text = "待機中"

if __name__ == "__main__":

    display_thread = threading.Thread(target=display_bring)
    Ultrasonic_thread = threading.Thread(target=Ultrasonic_scan)
    
    display_thread.start()
    Ultrasonic_thread.start()