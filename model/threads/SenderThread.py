from tools.StopableThread import *
from model.database.Measurement import *
import requests

class SenderThread:
    
    def __init__(self):
        self.__thread = StopableThread(target=self.__sendData, looped=True)
        
        
    def __sendData(self):
        
        print('Send Data')
        m = Measurement.getLastNotSent()
        if m:
            # add base auth
            resp = requests.post('https://vk.com', verify=False)
            if resp.status_code == 200: 
                self.__saveData(m)
            else:
                pass
        else:
            print('Nothing to send')
        
        sleep(0.5)
        
    
    def __saveData(self, m):
        print('Set sent')
        m.setSent()
        pass    
        
    def start(self):
        self.__thread.start()
        
    def stop(self):
        self.__thread.stop()
        self.__thread.join()
        
    def pause(self):
        self.__thread.pause()