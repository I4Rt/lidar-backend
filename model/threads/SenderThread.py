from tools.StopableThread import *
from model.database.Measurement import *
import requests
from requests.auth import HTTPBasicAuth

class SenderThread:
    
    def __init__(self):
        self.__thread = StopableThread(target=self.__sendData, looped=True)
        self.__headers = {'content-type': 'application/json',
                          'Host': 'vk.com',
                          'accept': '*/*'
                          }
        
    def __sendData(self):
        
        print('Send Data')
        m = Measurement.getLastNotSent()
        if m:
            # add base auth
            data = {'data': m.getParamsList()}
           
            resp = requests.post('https://vk.com', 
                                 auth=HTTPBasicAuth('user', 'password'), 
                                 headers=self.__headers, 
                                 json=data, 
                                 verify=False
                                )
            if resp.status_code == 200: 
                print('resp', resp)
                respBody = resp.json()
                if respBody:
                    if 'error' in respBody:
                        # log the error
                        pass
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