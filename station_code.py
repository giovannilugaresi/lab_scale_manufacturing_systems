#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
from time import sleep
from datetime import datetime
import time
import random



Simulation_length = 10000000
Global_Time = datetime(2018, 11, 21, 10, 12, 39, 0)
GroupID = 12
Group_Type = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 2]
Group_Seed = [203, 84, 138, 235, 223, 129, 3, 142, 54, 177, 354, 137, 563]

random.seed(Group_Seed[GroupID])
Product_A = 'red'
number_Product_A = 0


motor_block = MediumMotor('outD')
motor_station = LargeMotor('outB')
conveyor_opticalsensor = ColorSensor(INPUT_2)
conveyor_opticalsensor.mode = 'COL-COLOR'
station_opticalsensor = ColorSensor(INPUT_1)
station_opticalsensor.mode = 'COL-COLOR'
blocking_opticalsensor = ColorSensor(INPUT_3)
blocking_opticalsensor.mode = 'COL-COLOR'


colors = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')

i = 0
in_p = 0
out_p = 0
T_in_station = 0
T_out_station = 0

T_start = datetime.now()
Simulation_Start_Time = time.time()
workingA = 0
Current_Simulation_Time = 0
TOT_Load_Time = 0
TOT_Working_Time = 0
TOT_Unload_Time = 0
TOT_Block_Time = 0


file_TW = open('WorkingTime_A_S1.txt', 'w')  
file_time_input = open('time_in_S1.txt', 'w')  
file_time_finish = open('time_finish_S1.txt', 'w')  
file_time_output = open('time_out_S1.txt', 'w') 

while i < Simulation_length:
    color_stat_available = colors[station_opticalsensor.value()]
    color_conv_entering = colors[conveyor_opticalsensor.value()]
    if (color_stat_available == 'black') and (color_conv_entering == Product_A):
        print('A Product in the Buffer')
        in_p = in_p + 1
        T_in_station = Global_Time + (datetime.now() - T_start)
        T_in_station = T_in_station.strftime("%Y %m %d %H %M %S.%f")
        file_time_input.write('{} '.format(T_in_station))
        file_time_input.write('%d\n' % in_p)
        LoadingTime_input = time.time()

        motor_block.run_forever(speed_sp=-750) 
        sleep(0.45)
        motor_block.stop(stop_action='hold')
        motor_block.run_forever(speed_sp=750)
        motor_station.run_forever(speed_sp=825)  
        sleep(0.45)
        motor_block.stop(stop_action='hold')  
        
        a = 0
        b = 0
        T_check_input = time.time()
        while a < 1:
            color_stat_ent = colors[station_opticalsensor.value()]
            if color_stat_ent == Product_A:
                a = 1
            if (time.time() - T_check_input) > 5:
                a = 1
                b = 1
        if b == 1:
            in_p = in_p - 1

        motor_station.stop(stop_action="hold")  
        LoadingTime = time.time() - LoadingTime_input
        TOT_Load_Time = TOT_Load_Time + LoadingTime

    
    color_stat_working = colors[station_opticalsensor.value()]  
    if color_stat_working == Product_A:
        print('Product is being worked by the Station ')
        number_Product_A = number_Product_A + 1
        print('Number of Pieces is: ', number_Product_A)
        if GroupID == 0:
            Tw_Astoc = random.uniform(2, 8)
        elif Group_Type[GroupID] == 1:
            Tw_Astoc = random.triangular(2, 6, 4)
        else:
            Tw_Astoc = random.triangular(2, 6, 4)
        workingA = Tw_Astoc
        sleep(workingA) 
        TOT_Working_Time = TOT_Working_Time + workingA

       
        T_finish_operation = Global_Time + (datetime.now() - T_start)
        T_finish_operation = T_finish_operation.strftime("%Y %m %d %H %M %S.%f")
        file_time_finish.write('{} '.format(T_finish_operation))
        file_time_finish.write('%d\n' % number_Product_A)
        print('Operation is Finished now ')

      
        color_block_available = colors[blocking_opticalsensor.value()]
        if color_block_available == Product_A:
            Block = 1
            BlockingTime_input = time.time()
            BlockingTime = 0
            while Block < 2:
                color_block = colors[blocking_opticalsensor.value()]
                if color_block == Product_A:
                    Block = 1
                else:
                    Block = 2
            BlockingTime = time.time() - BlockingTime_input
            TOT_Block_Time = TOT_Block_Time + BlockingTime

        UnloadingTime_input = time.time()
        motor_station.run_forever(speed_sp=1000)
        sleep(1.4)
        out_p = out_p + 1
        UnloadingTime = time.time() - UnloadingTime_input
        TOT_Unload_Time = TOT_Unload_Time + UnloadingTime

        T_out_station = Global_Time + (datetime.now() - T_start)
        T_out_station = T_out_station.strftime("%Y %m %d %H %M %S.%f")
        file_time_output.write('{} '.format(T_out_station))
        file_time_output.write('%d\n' % out_p)
        motor_station.stop(stop_action='hold')

      
        Current_Simulation_Time = time.time() - Simulation_Start_Time
        file_TW.write('%d ' % number_Product_A)
        file_TW.write('%f ' % workingA)
        file_TW.write('%f ' % Current_Simulation_Time)
        file_TW.write('%f ' % TOT_Load_Time)
        file_TW.write('%f ' % TOT_Working_Time)
        file_TW.write('%f ' % TOT_Block_Time)
        file_TW.write('%f\n' % TOT_Unload_Time)

    i = i + 0.000000000001

file_TW.close()
file_time_finish.close()
file_time_input.close()
file_time_output.close()