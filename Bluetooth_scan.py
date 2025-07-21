from bluepy.btle import Scanner, DefaultDelegate
import sys

class ScanDelegate(DefaultDelegate):
    Earfun_Air_MacAddress = "70:5a:6f:63:b2:f7"
    
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):#dev 発見したデバイスの情報(MAC) isNewDev デバイスの初回発見時True isNewData 発見済みのデバイスから新規データ受診時 True
        if isNewDev:
            print("Discoverd device", dev.addr)
            print("Discoverd device", dev.rssi)
            '''if(dev.addr==self.Earfun_Air_MacAddress):
                print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
                print("Yes, We can")
                sys.exit()'''
                
        elif isNewData:
            print("Received new data from", dev.addr)    

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)


'''for dev in devices:
    if(dev.addr==Earfun_Air_MacAddress):
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        print("Yes, We can")
    for(adtype, desc, value) in dev.getScanData():
        print(" %s = %s" % (desc, value))'''
