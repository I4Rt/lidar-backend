import datetime
import math
import numpy
from sklearn.cluster import DBSCAN

class DataAnalize:

    @classmethod
    def final_analize(cls, data_3d_outside):
        print('start analize')
        result_str = {"horizontal": [], "vertical":[], "Exception": "", 'time': str(datetime.datetime.now())}

        first_cut_list = cls.get_iterable_close_data(data_3d_outside, "artificial", 0.1, delta=0.01)

        first_results = []

        for cut in first_cut_list:
            lines_array, array_c, fractures = cls.one_way_analize_advanced(cut, averaging_segment_len = 10, indenting_segment_len = 15, significant_angle_1 = 0.7, significant_angle_2 = 2.0, noise_angle = 0.6, not_meaning = 10)
            biggest_plot, biggest_min_digression, biggest_max_digression, plot_coordinates = cls.calculate_info(cut, fractures)

            first_results.append([biggest_plot, biggest_min_digression, biggest_max_digression, lines_array, array_c, fractures, plot_coordinates])

        first_result = cls.get_closest(first_results)
        if( first_result == None):
            for i in first_results:
                print(i[0])
            return {"horizontal": [[0, 0, 0],[0, 0, 0],[0, 0, 0]], "vertical":[[0, 0, 0],[0, 0, 0],[0, 0, 0]], "Exception": "Anode is out of scaning bounds", 'time': str(datetime.datetime.now())}

        left_coordinate_Z = first_result[6][0][0] + 0.05
        right_coordinate_Z = first_result[6][-1][0] - 0.05
        center_coordinate_Z = (left_coordinate_Z + right_coordinate_Z)/2

        
        reference_vertical_scan = None
        
        for coordinate in [left_coordinate_Z, center_coordinate_Z, right_coordinate_Z]:
            vertical_cut_list = cls.get_iterable_close_data(data_3d_outside, "normal", coordinate, delta=0.0018)

            #print(f'vertical_cut_list: {len(vertical_cut_list)}')

            vertical_results = []

            for cut in vertical_cut_list:
                lines_array, array_c, fractures = cls.one_way_analize_advanced(cut, averaging_segment_len = 10, indenting_segment_len = 5, significant_angle_1 = 0.7, significant_angle_2 = 0.9, noise_angle = 0.6, not_meaning = 10)
                biggest_plot, biggest_min_digression, biggest_max_digression, plot_coordinates = cls.calculate_info(cut, fractures)

                vertical_results.append([biggest_plot, biggest_min_digression, biggest_max_digression, lines_array, array_c, fractures, plot_coordinates])

            #print(len(vertical_results))

            vertical_result = cls.get_closest(vertical_results, cut_type = "vertical")

            if( vertical_result == None):
                result_str["vertical"].append([0, 0, 0])
            else: 
                result_str["vertical"].append([round(vertical_result[0], 4), round(vertical_result[1], 4), round(vertical_result[2], 4)])
                reference_vertical_scan = vertical_result
                
        if(reference_vertical_scan != None):
            left_coordinate_Y = reference_vertical_scan[6][0][0] + 0.1
            right_coordinate_Y = reference_vertical_scan[6][-1][0] - 0.1
            center_coordinate_Y = (left_coordinate_Y + right_coordinate_Y) / 2

            for coordinate in [left_coordinate_Y, center_coordinate_Y, right_coordinate_Y]:
                horizontal_cut_list = cls.get_iterable_close_data(data_3d_outside, "artificial", coordinate)

                #print(f'horizontal_cut_list: {len(horizontal_cut_list)}')

                horizontal_results = []

                for cut in horizontal_cut_list:
                    lines_array, array_c, fractures = cls.one_way_analize_advanced(cut, averaging_segment_len = 10, indenting_segment_len = 20, significant_angle_1 = 0.9, significant_angle_2 = 5.0, noise_angle = 0.6, not_meaning = 10)
                    biggest_plot, biggest_min_digression, biggest_max_digression, plot_coordinates = cls.calculate_info(cut, fractures)

                    horizontal_results.append([biggest_plot, biggest_min_digression, biggest_max_digression, lines_array, array_c, fractures, plot_coordinates])

                #print(len(horizontal_results))

                horizontal_result = cls.get_closest(horizontal_results)

                if( horizontal_result == None):
                    result_str["horizontal"].append([0, 0, 0])
                else: 
                    result_str["horizontal"].append([round(horizontal_result[0], 4), round(horizontal_result[1], 4), round(horizontal_result[2], 4)])
                
        else:
            return {"horizontal": [[0, 0, 0],[first_result[0], first_result[1], first_result[2]],[0, 0, 0]], "vertical":[[0, 0, 0],[0, 0, 0],[0, 0, 0]], "Exception": "Need Check", 'time': str(datetime.datetime.now())}

        return result_str
    
    @classmethod
    def calculate_info(data_ready, fractures):
        main_lines = [[(fractures[point_id + 1][1] - fractures[point_id][1])/(fractures[point_id + 1][0] - fractures[point_id][0] + 0.0000000001), fractures[point_id][1] - ((fractures[point_id + 1][1] - fractures[point_id][1])/(fractures[point_id + 1][0] - fractures[point_id][0] + 0.000000001))*fractures[point_id][0]] for point_id in range(len(fractures) - 1)]
        cur_line_index = 0
        point_id = 0
        cur_min = 0
        cur_max = 0
        min_max_array = []
        
        while (point_id < len(data_ready)):
            if(data_ready[point_id] != fractures[cur_line_index + 1]):
                distance = (main_lines[cur_line_index][0] * data_ready[point_id][0] - data_ready[point_id][1] + main_lines[cur_line_index][1])/math.sqrt(1 + main_lines[cur_line_index][0]**2)    
                if(cur_min > distance):
                    cur_min = distance
                if(cur_max < distance):
                    cur_max = distance
            else:
                min_max_array.append([cur_min, cur_max])
                cur_min = 0
                cur_max = 0
                cur_line_index += 1
            point_id += 1

        distances = [math.sqrt((fractures[index][0] - fractures[index + 1][0])**2 + (fractures[index][1] - fractures[index + 1][1])**2) for index in range(len(fractures) - 1)]
        biggest_plot = -1;
        biggest_min_digression = 10;
        biggest_max_digression = -10;
        fracture_id = 0
        plot_coordinates = []
        for index in range(len(distances)):
            fracture_id+=1;
            if(distances[index] > biggest_plot):
                biggest_plot = distances[index]
                #print(plot_coordinates)
                plot_coordinates = [fractures[fracture_id - 1], fractures[fracture_id]]
                if(min_max_array[index][0] < biggest_min_digression):
                    biggest_min_digression = min_max_array[index][0]
                if(min_max_array[index][1] > biggest_max_digression):
                    biggest_max_digression = min_max_array[index][1]
                
            #print(f"Range: {distances[index]}")
            #print(f"Min digression: {min_max_array[index][0]}")
            #print(f"Max digression: {min_max_array[index][1]}")
        
        return biggest_plot, biggest_min_digression, biggest_max_digression, plot_coordinates


    @classmethod
    def get_closest(cls, data, cut_type = "horizontal"):
    
        if(cut_type == "horizontal"):
            first_array = []
            for result in data:
                #print(result[0])
                if(abs(result[0] - 1.45) < 0.05 or abs(result[0] - 1.55) < 0.05):
                    if( abs(result[0] - 1.45) <= abs(result[0] - 1.55)):
                        first_array.append(45)
                    else: 
                        first_array.append(55)

                else:
                    first_array.append(-1)


            distance = 10.0

            fin = None

            mode, count =  cls.count_mode(first_array)

            if(mode == 45 and count > 1):
                for result in data:
                    if ((result[0] - 1.45) < distance):
                        distance = abs(result[0] - 1.45)
                        fin = result

            if(mode == 55 and count > 1):
                for result in data:
                    if (abs(result[0] - 1.55) < distance):
                        distance = abs(result[0] - 1.55)
                        fin = result
        
        else:
            first_array = []
            for result in data:
                #print(result[0])
                if(abs(result[0] - 0.575) < 0.05):
                    first_array.append(575)
                else:
                    first_array.append(-1)
            
            distance = 10.0
            
            fin = None

            mode, count =  cls.count_mode(first_array)

            if(mode == 575 and count > 2):
                for result in data:
                    if (abs(result[0] - 0.575) < distance):
                        distance = abs(result[0] - 0.575)
                        fin = result

        #if (fin != None):
        #    display_data(fin[3], fin[4], fin[5], etalon_marker = True)
        
        return fin
    
    @classmethod
    def count_mode(cls, array):
        mode = {array[i]: 0 for i in range(len(array))}
        for i in array:
            mode[i] += 1
        mode_val = sorted(mode, key=mode.get, reverse=True)[0]
        if(mode_val == -1):
            if(len(mode) > 1):
                mode_val = sorted(mode, key=mode.get, reverse=True)[1]
                
        return mode_val, mode[mode_val]
    
    @classmethod
    def get_average(cls, data):
        x = 0
        y = 0
        for i in data:
            x+= i[0]
            y+= i[1]
        return [x/len(data), y/len(data)]
    
    @classmethod
    def one_way_analize_advanced(cls, data, averaging_segment_len = 5, indenting_segment_len = 5, significant_angle_1 = 0.2, significant_angle_2 = 1.8, noise_angle = 0.05, not_meaning = 7):
        total_indent_len = averaging_segment_len + indenting_segment_len
        data.sort(key=lambda row: (row[0]), reverse=False)
        left_adder_segment = [data[0] for _ in range(averaging_segment_len + indenting_segment_len)]
        right_adder_segment = [data[-1] for _ in range(averaging_segment_len + indenting_segment_len)]
        
        data = left_adder_segment + data
        data = data + right_adder_segment
        
        plots = []
        fractures = [data[0]]
        
        prev_angle = 0
        prev_angle_delta = 0
        current_plot = []
        current_plot += data[0:total_indent_len - 1]
        
        for analize_index in range(total_indent_len, len(data) - total_indent_len):
            left_averaged = cls.get_average(data[analize_index - total_indent_len : analize_index - indenting_segment_len])
            right_averaged = cls.get_average(data[analize_index + indenting_segment_len : analize_index + total_indent_len])
            
            
            
            a1 = (data[analize_index][1] - left_averaged[1])/(data[analize_index][0] - left_averaged[0] + 0.00000001)
            a2 = (data[analize_index][1] - right_averaged[1])/(data[analize_index][0] - right_averaged[0] + 0.00000001)
            
            angle = abs((a1 - a2)/(1 + (a1*a2)))
            #print(f"angle: {angle}")
            #print(f"Prev delta: {prev_angle_delta}")
            
            
            #bug! 
            
            if(prev_angle_delta > 0 and angle <= prev_angle and (abs(angle - prev_angle) > noise_angle or (angle - prev_angle < 0 and abs(angle - prev_angle) > noise_angle*0.5))):
                if (prev_angle > significant_angle_1):
                    if (len(current_plot) > not_meaning):  
                        plots.append(current_plot)
                        if(prev_angle >= significant_angle_2 ):

                            fractures.append(current_plot[-1])
                        current_plot = []   
                        
            current_plot.append(data[analize_index])
            
            
            prev_angle_delta = angle - prev_angle
            #print(f"Delta: {prev_angle_delta}\n")
            prev_angle = angle
            
        current_plot += data[len(data) - total_indent_len:]
        plots.append(current_plot)
        fractures.append(data[-1])
            
        del plots[-1][-(averaging_segment_len + indenting_segment_len):]
        del plots[0][:(averaging_segment_len + indenting_segment_len)] 

        array_c = [[plot_id for point in plots[plot_id]] for plot_id in range(len(plots))]
        
        return plots, array_c, fractures
    
    @classmethod
    def get_artificial_data_cut(cls, center, data_3d):
        #print(f'in center: {center}')
        center1 = center 
        prepared_data = []
        
        real_artificial_cut = [[item[1], item[2], item[0]] for item in data_3d if center - 0.00172 < item[0] < center + 0.00173]
        real_artificial_cut_2D = [[item[1], item[0]]  for item in real_artificial_cut if item[0] > 0.2]

        real_artificial_cut_2D_grabbed = []
        existing_z = []

        for i in real_artificial_cut_2D:
            if( i[0] in existing_z):
                continue
            else:
                real_artificial_cut_2D_grabbed.append(i)
                existing_z.append(i[0])
        #print(len(real_artificial_cut_2D_grabbed))
        #display_data([real_artificial_cut_2D_grabbed], [1 for i in range(len(real_artificial_cut_2D_grabbed))], etalon_marker = False)

        prepared_data, val = cls.get_plot_DBSCAN(real_artificial_cut_2D_grabbed, 0.02, 3)
        prepared_data.sort(key=lambda row: (row[0]), reverse=False)
        
        
        #print(f'plots number: {val}')
        
        
        return prepared_data, center1
    
    @classmethod
    def get_data_cut(cls, center, data_3d_inside):
        real_center = (center//0.0018562291554143687)*0.0018562291554143687
        #print(f'real center: {real_center}')
        #print(data_3d_inside)
        
        correction = 0
        
        while True:
            real_cut = [[item[0], item[1], item[2]] for item in data_3d_inside if real_center-0.00095 + correction < item[2] < real_center+0.00095 + correction] #changed
            real_cut_2D = [[item[0], item[1]]  for item in real_cut]                          
            if(len(real_cut) < 400):
                correction += 0.0002
            else:
                break
            
            
        real_cut_2D_grabbed = []
        existing_z = []

        for i in real_cut_2D:
            if( i[0] in existing_z):
                continue
            else:
                real_cut_2D_grabbed.append(i)
                existing_z.append(i[0])
        #print(len(real_cut_2D_grabbed))
        #display_data([real_cut_2D_grabbed], [1 for i in range(len(real_cut_2D_grabbed))], etalon_marker = False)

        prepared_data, val = cls.get_plot_DBSCAN(real_cut_2D_grabbed, 0.02, 5) #!
        
        prepared_data = [item for item in prepared_data if item[0] > -0.3]
        
        return prepared_data, center
    
    @classmethod
    def get_plot_DBSCAN(data_2D_prepare, max_step = 0.02, min_samples_got=7):
        db = DBSCAN(eps=max_step, min_samples=min_samples_got).fit(data_2D_prepare)
        center_x = 0
        for point in data_2D_prepare:
            center_x+= point[0]
        
        
        plots_unique_val, counts = numpy.unique(db.labels_, return_counts=True)
        plots = []
        plot_color_array = []
        for plot_color in plots_unique_val:
            plot = []
            if(plot_color != 1):
                for point_id in range(len(db.labels_)):
                    if(db.labels_[point_id] == plot_color):
                        plot.append(data_2D_prepare[point_id])
                plots.append(plot)
                plot_color_array.append(plot_color)
        
        min_distance = 0.2
        result_plot_id = 0
        
        max_size = 0
        result_plot = []
        
        for plot in plots:
            if(len(plot) > len(result_plot)):
                result_plot = plot
                
        return result_plot, len(plots_unique_val)

    @classmethod
    def get_iterable_close_data(cls, data, scan_type, point, num_of_scan = 5, delta = 0.005):
    
        result = []
        
        center_1 = 0
        center_2 = 0
        center_3 = 0
        center_4 = 0
        center_5 = 0
        
        point1 = point
        
        point2 = point1 + delta
        point3 = point1 + 2*delta
        
        point4 = point1 - delta
        point5 = point1 - 2*delta
        
        
        
        
        if(scan_type == "artificial"):
            
            first, center_1 = cls.get_artificial_data_cut(point, data)
            #print(f'first len: {len(first)}')
            #print(f'first center: {center_1}')
            
            
            second, center_2 = cls.get_artificial_data_cut(point2, data)
            #print(f'second len: {len(second)}')
            #print(f'second center: {center_2}')
            
            
            third, center_3 = cls.get_artificial_data_cut(point3, data)
            #print(f'third len: {len(third)}')
            #print(f'third center: {center_3}')
            
            
            fourth, center_4 = cls.get_artificial_data_cut(point4, data)
            #print(f'fourth len: {len(fourth)}')
            #print(f'fourth center: {center_4}')
                
            
            fifth, center_5 = cls.get_artificial_data_cut(point5, data)
            #print(f'fifth len: {len(fifth)}')
            #print(f'fifth center: {center_5}')
                
            
            result.append(first)
            result.append(second)
            result.append(third)
            result.append(fourth)
            result.append(fifth)
            
        
        if(scan_type == "normal"):
            
            first, center_1 = cls.get_data_cut(point, data)
            #print(f'first len: {len(first)}')
            #print(f'first center: {center_1}')
            
            
            second, center_2 = cls.get_data_cut(point2, data)
            #print(f'second len: {len(second)}')
            #print(f'second center: {center_2}')
            
            
            third, center_3 = cls.get_data_cut(point3, data)
            #print(f'third len: {len(third)}')
            #print(f'third center: {center_3}')
            
            
            fourth, center_4 = cls.get_data_cut(point4, data)
            #print(f'fourth len: {len(fourth)}')
            #print(f'fourth center: {center_4}')
                
            
            fifth, center_5 = cls.get_data_cut(point5, data)
            #print(f'fifth len: {len(fifth)}')
            #print(f'fifth center: {center_5}')
                
            
            result.append(first)
            result.append(second)
            result.append(third)
            result.append(fourth)
            result.append(fifth)
        
        return result