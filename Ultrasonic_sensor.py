import RPi.GPIO as GPIO
import time
import sys
from bluepy.btle import Scanner, DefaultDelegate
import threading
import GUI
from queue import Queue
import tkinter



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
             print(1)   
                
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

    
def Ultrasonic_scan(queue,scanner,com_display_result):
    com_result = True#検知結果の表示が完了したことを表す。初期値はTrue

    while True:
        try:
            distance = '{:.1f}'.format(get_distance())
            print("Distance: " + distance + "cm")

            if(not(com_display_result.qsize()==0)):
                com_result = com_display_result.get()

            if(float(distance)<=5.0 and com_result):
                com_result=False
                scan = True
                queue.put(scan)
                devices = scanner.scan(4)
                
                queue.put(devices)
                
            time.sleep(3)
            
        except KeyboardInterrupt:
            GPIO.cleanup()
            sys.exit()


scanner = Scanner()#.withDelegate(ScanDelegate())
default_text = "待機中"
scan = False


if __name__ == "__main__":
    queue = Queue()
    com_display_result = Queue()
    root = tkinter.Tk()
    
    Ultrasonic_thread = threading.Thread(target=Ultrasonic_scan,args=(queue,scanner,com_display_result))
    Ultrasonic_thread.start()
    
    GUI.display_bring(queue,root,com_display_result)
    