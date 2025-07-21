import threading
import time

def boil_udon():
    print("スレッド:", threading.currentThread().getName())
    
    print('うどんを茹でます')
    time.sleep(3)
    print('うどんが茹で上がりました')
    
    
def make_tuyu():
    print("スレッド:",threading.currentThread().getName())
    print('ツユを作ります')
    time.sleep(2)
    print('ツユができました')
    
    
if __name__ == "__main__":
    print("スレッド:",threading.currentThread().getName())
    
    print('うどんを作ります')
    
    thread1 = threading.Thread(target=boil_udon)
    thread2 = threading.Thread(target=make_tuyu)
    
    #スレッドの処理を開始
    thread1.start()
    thread2.start()
    
    #スレッドの処理を待つ
    #thread1.join()
    thread2.join()
    
    print('盛り付けます')
    print('うどんが出来上がりました')
    