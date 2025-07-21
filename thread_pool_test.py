from concurrent.futures import ThreadPoolExecutor
import time

def make_udon(kind):
    print('%sうどんを作ります' % kind)
    time.sleep(3)
    return kind + 'うどん'


kinds = ['たぬき','かけ','カレー','きつね','天ぷら']
executor = ThreadPoolExecutor(max_workers=3)
futures = []


for kind in kinds:
    print('%sうどん オーダー' % kind)
    future  =executor.submit(make_udon, kind)
    futures.append(future)
    
for future in futures:
    print('%sおまたせしました' % future.result())
    
    
executor.shutdown()