from tools.StopableThread import *
from tools.DataAnalize import *
from tools.GetDataFromDevice import *
from model.threads.DeviceThread import *
from model.threads.MoverThread import *
from model.database.Measurement import *
from datetime import datetime
import socket
import serial

class SaverThread:

    def __init__(self, addresses):
        self.addresses = addresses
        
    def __getData(self, listener):
        print('GetData')
        results = [{},{}]
        threads = []
        try:
            data, addr = listener.recvfrom(1024)
            print(data.hex())
            if data.hex().lower() in 'aaaa':
                print('received')

                client_moving = serial.Serial('COM5', 57600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,
                      timeout=0.1)
                movingThread = DeviceThread(target=MoverThread.move, args=(client_moving,))
                threads.append(movingThread)

                for address in self.addresses:
                    client_lidar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_lidar.connect((address['address'], address['port']))

                    deviceThread = DeviceThread(target=self.__scan, args=(client_lidar,),)
                    threads.append(deviceThread)

                for index, thread in enumerate(threads):
                    thread.start()

                for index, thread in enumerate(threads):
                    results[index] = thread.join()

                self.__saveData(results)

        except socket.error as e:
            print(str(e))

    def __scan(self, client):
        print('scan ' + str(datetime.datetime.now()))
        all_data = GetDataFromDevice.scanning(client)
        arrays = GetDataFromDevice.getDataForAnalize(all_data)

        print('start analize ' + str(datetime.datetime.now()))
        final_results = DataAnalize.final_analize(arrays)
        print('stop analize ' + str(datetime.datetime.now()))

        return final_results
    
    def __saveData(self, results):
        print('SaveData')
        m = Measurement(results[1]['horizontal'][0][0], results[1]['horizontal'][1][0], results[1]['horizontal'][2][0],
                        results[2]['horizontal'][0][0], results[2]['horizontal'][1][0], results[2]['horizontal'][2][0],
                        results[1]['vertical'][0][0], results[1]['vertical'][1][0], results[1]['vertical'][2][0],
                        results[2]['vertical'][0][0], results[2]['vertical'][1][0], results[2]['vertical'][2][0],
                        0, 0, 0,
                        0, 0, 0
                        )
        m.save()

        
    def start(self):
        # lidarSettings()

        listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listener.bind(('127.0.0.1', 61557))
        print('listening')

        self.__thread = StopableThread(target=self.__getData, args=(listener,), looped=True)
        self.__thread.start()

    def stop(self):
        print('stop')
        self.__thread.stop()
        # self.__thread.join()
        
    def pause(self):
        self.__thread.pause()
