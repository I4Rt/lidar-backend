import datetime
import time

class MoverThread:

    values_start = [0x00, 0x00, 0x02, 0x03, 0x45, 0x41]
    values_return = [0x00, 0x00, 0x02, 0x02, 0x85, 0x80]
    values_stop = [0x00, 0x00, 0x02, 0x01, 0x84, 0xc0]

    @classmethod
    def move(cls, client):
        print('start move ' + str(datetime.datetime.now()))

        client.write(cls.values_start)
        time.sleep(14)
        print(client.readline())

        print('end move ' + str(datetime.datetime.now()))

        client.write(cls.values_stop)
        print(client.readline())

        client.write(cls.values_return)
        time.sleep(14)
        print(client.readline())

        return True