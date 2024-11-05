from tools.StopableThread import *
from model.database.Measurement import *
from random import randint
class SaverThread:
    
    def __init__(self):
        self.__thread = StopableThread(target=self.__getData, looped=True)
        
        
    def __getData(self):
        print('GetData')
        # проверка на положение анода
        # если анод в зоне
        self.__saveData()
        sleep(5)
        # иначе
        pass
    
    def __saveData(self):
        print('SaveData')
        m = Measurement(randint(0, 10)/10, randint(0, 10)/10, randint(0, 10)/10,
                        randint(0, 10)/10, randint(0, 10)/10, randint(0, 10)/10,
                        randint(0, 10)/10, randint(0, 10)/10, randint(0, 10)/10,
                        randint(0, 10)/10, randint(0, 10)/10, randint(0, 10)/10,
                        randint(0, 10)/10, randint(0, 10)/10, randint(0, 10)/10
                        )
        m.save()

        
    def start(self):
        self.__thread.start()
        
    def stop(self):
        self.__thread.stop()
        self.__thread.join()
        
    def pause(self):
        self.__thread.pause()