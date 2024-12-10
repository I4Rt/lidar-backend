from config import *
from model.threads.SaverThread  import *
from model.threads.SenderThread import *

Base.metadata.create_all(e)


if __name__ == "__main__":  
    addresses = [
                    {'address':'192.168.0.3', 'port':2111},
                    {'address':'192.168.0.2', 'port':2111}
                ]
    saver = SaverThread(addresses)
    sender = SenderThread()
    
    saver.start()
    # sender.start()
    sleep(5)
    saver.stop()
    # sender.stop()



    

