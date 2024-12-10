import time
import datetime
import math

class GetDataFromDevice:

    slices = 1300

    MESSAGE_START_FAST = b'\x02\x02\x02\x02\x00\x00\x00\x11\x73\x45\x4E\x20\x4C\x4D\x44\x73\x63\x61\x6E\x64\x61\x74\x61\x20\x01\x33'
    MESSAGE_STOP_FAST = b'\x02\x02\x02\x02\x00\x00\x00\x11\x73\x45\x4E\x20\x4C\x4D\x44\x73\x63\x61\x6E\x64\x61\x74\x61\x20\x00\x32'
    
    MESSAGE_START_MES = b'\x02\x02\x02\x02\x00\x00\x00\x10\x73\x4D\x4E\x20\x4C\x4D\x43\x73\x74\x61\x72\x74\x6D\x65\x61\x73\x68'
    MESSAGE_STANDBY = b'\x02\x02\x02\x02\x00\x00\x00\x0E\x73\x4D\x4E\x20\x4C\x4D\x43\x73\x74\x61\x6E\x64\x62\x79\x65'
    
    z = 0.0018562291554143687

    @classmethod
    def scanning(cls, client):
        all_data = []

        time.sleep(0.5)
        client.sendall(cls.MESSAGE_START_MES)
        in_data = client.recv(100)
        print(in_data.hex())

        client.sendall(cls.MESSAGE_START_FAST)
        in_data = client.recv(100)
        print(in_data.hex())

        print(datetime.datetime.now())
        for i in range(cls.slices):
            # with refl client.recv(5192)
            in_data = client.recv(3489)
            all_data.append(in_data.hex())

        client.sendall(cls.MESSAGE_STOP_FAST)
        print(datetime.datetime.now())

        client.sendall(cls.MESSAGE_STANDBY)
        in_data = client.recv(100)
        print(in_data.hex())

        return all_data
    
    @classmethod
    def counting(cls, c_arrays_len, c_arrays_angle, z, value_counting):
        coord_array = []
        for j in range(len(c_arrays_len)):
            coordinates = []
            length = c_arrays_len[j]
            # if j > 820:
            #     print(str(j) + " " + str(c_arrays_angle[j]))
            if len(c_arrays_angle) != 841:
                print(len(c_arrays_len))
                print(len(c_arrays_angle))
                print(value_counting)

            angle_rad = c_arrays_angle[j] * math.pi / 180
            x = math.cos(angle_rad) * length
            y = math.sin(angle_rad) * length
            if length != 0:
                coordinates.append(x)
                coordinates.append(y)
                coordinates.append(z)
                coord_array.append(coordinates)
        return coord_array
    
    @classmethod
    def counting_arrays(cls, string, choice, c_array):
        angle_count = 0
        while len(string) > 1:
            dec = int(string[0:4], 16)
            string = string[4:len(string)]
            if choice == 1:
                c_array.append(float(dec) / 10000)
            elif choice == 2:
                c_array.append(55 + (angle_count * 0.0833))
                angle_count = angle_count + 1
            elif choice == 3:
                c_array.append(dec)
        return c_array
    
    @classmethod
    def getDataForAnalize(cls, all_data):
        arrays = []
        for i in range(len(all_data)):
            if i == 0:
                print('len ' + str(len(all_data))) 
                print('start counting ' + str(datetime.datetime.now()))
            if i == len(all_data)-1:
                print('stop counting ' + str(datetime.datetime.now()))
            value = all_data[i]
            # with refl value [182:10358]
            value = value[182:6952]
            c_arrays_len = cls.counting_arrays(value[0:3364], 1, c_arrays_len)
            value = value[3406:len(value)]
            c_arrays_angle = cls.counting_arrays(value[0:3364], 2, c_arrays_angle)

            coord_array = cls.counting(c_arrays_len, c_arrays_angle, z, value)
            for i in range(len(coord_array)):
                # arrays_csv.append(coord_array[i][0])
                # arrays_csv.append(coord_array[i][1])
                # arrays_csv.append(coord_array[i][2])
                arrays.append(coord_array[i])
            c_arrays_angle.clear()
            c_arrays_len.clear()
            z = z + 0.0018562291554143687
        return arrays