import temperature_cal
import numpy as np
import matplotlib.pyplot as plt
import torch
import time
import scipy.io
import xlrd

#var_h_initial=[112.5,113.167,61.63,52.36]
#var_h_initial=[163.65,134.36,68.07,46.47]
var_ZNumber = 500 # 拉坯方向网格划分的数量
#var_XNumber=20 # 铸坯厚度方向的网格点数
var_XNumber=32
var_X=0.16 # 铸坯厚度
#var_YNumber=20 # 铸坯厚度方向的网格点数
var_YNumber=32
var_Y=0.16 # 铸坯厚度
var_Z=7.68
deltZ = var_Z/var_ZNumber # 拉皮方向的空间间隔
middle_temp = [([1530]*var_XNumber) for i in range(var_XNumber)]
var_temperatureWater = 30
var_rouS=7800
var_rouL=7200
var_specificHeatS=660
var_specificHeatL=830
var_TconductivityS=31
var_TconductivityL=35
var_liqTemp=1514
var_SodTemp=1475
var_m=7.1
var_latentHeatofSolidification = 268000
var_controlTime=3
var_dis=[0.0,0.9,1.27,3.12,5.32,7.68] # 连铸二冷区各段距弯月面的距离 单位m
var_runningTime=20


def one_example_temp_cal(t_cast,v_cast, var_h_initial):
    var_VcastOriginal = v_cast / 60
    var_castingTemp = t_cast  # 铸坯的浇筑温度
    var_deltTime = 0.4 * 0.6 / v_cast
    MiddleTemp = [([var_castingTemp] * var_YNumber) for i in range(var_XNumber)]
    tl = [0] * len(var_dis);  # 铸坯凝固时间的初值var_dis=[0.0,0.9,1.27,3.12,5.32,7.68] # 连铸二冷区各段距弯月面的距离 单位m
    t_l = np.ones(len(var_dis));
    for i in range(len(var_dis)):
        tl[i] = var_dis[i] / (v_cast / 60)  # var_VcastOriginal=0.6/60

        t_l[i] = int(tl[i] / var_deltTime) - 2
    time_Mold = int((tl[1] - tl[0]) / var_deltTime)
    time_SCZ = int((tl[len(var_dis) - 1] - tl[1]) / var_deltTime)  # var_deltTime=0.4 # 差分计算时间间隔
    #Time_all = time_Mold + time_SCZ
    Time_all=1920
    start_time = time.time()
    MiddleTemp_all, t = temperature_cal.steady_temp_cal(var_dis, var_VcastOriginal, var_deltTime, MiddleTemp, var_XNumber, var_YNumber, var_X, var_Y,
                    var_temperatureWater, var_rouS, var_rouL, var_specificHeatS, var_specificHeatL, var_TconductivityS,
                    var_TconductivityL, var_liqTemp, var_SodTemp, var_m, var_latentHeatofSolidification, Time_all,
                    time_Mold, var_h_initial, var_ZNumber, var_castingTemp)
    end_time = time.time()
    cal_time = end_time - start_time
    print("计算一次温度场时间：", cal_time)
    # print(np.array(MiddleTemp_all).shape)
    # for step in range(0, Time_all, 500):
    #     print(np.array(MiddleTemp_all)[:,:,step])
    #     plt.matshow(np.array(MiddleTemp_all)[:,:,step])
    #     plt.show()
        # plt.matshow(t[step])
        # plt.show()
        # print("time:",step)
        # for i in range(var_XNumber):
        #     for j in range(var_YNumber):
        #         print(t[step][i][j],end="")
        #     print(" ")
    return MiddleTemp_all, t

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data = xlrd.open_workbook('h_v_t.xlsx')
    sheet = data.sheet_by_name('Sheet1')
    all_rows = sheet.get_rows()
    temperature_field_data = torch.empty((240,32,32,1920))
    count = 0
    for row in all_rows:
        var_h_initial = [row[0].value,row[1].value,row[2].value,row[3].value]
        v_cast = row[4].value
        t_cast = row[5].value
        print("第",count,"次运行，参数：",var_h_initial,v_cast,t_cast)
        MiddleTemp_all, t = one_example_temp_cal(t_cast,v_cast, var_h_initial)
        temperature_field_data[count] = torch.Tensor(MiddleTemp_all)
        # print(temperature_field_data[count])
        count  = count + 1
    #     if count > 3:
    #         break
    # print(temperature_field_data.shape)
    # for i in range(4):
    #     for time in range(0,1920,500):
    #         print(temperature_field_data[i,:, :, time])
    #         plt.matshow(temperature_field_data[i,:, :, time])
    #         plt.show()
    print(temperature_field_data.shape)
    scipy.io.savemat('data/temperature_data.mat', mdict={'temperature_field_data':temperature_field_data.cpu().numpy()})

