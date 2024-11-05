from config import *
from model.threads.SaverThread  import *
from model.threads.SenderThread import *

Base.metadata.create_all(e)


if __name__ == "__main__":  
    saver = SaverThread()
    sender = SenderThread()
    
    saver.start()
    sender.start()
    sleep(15)
    saver.stop()
    sender.stop()



    

