import math

#计算下一时刻温度场
def two_densonal_diff(h, var_deltTime, middle_temp, var_XNumber, var_YNumber, var_X, var_Y, var_temperatureWater,
                      var_rouS, var_rouL, var_specificHeatS, var_specificHeatL, var_TconductivityS, var_TconductivityL,
                      var_liqTemp, var_SodTemp, var_m, var_latentHeatofSolidification):
    deltX = var_X / var_XNumber  # 铸坯在厚度方向的空间间隔
    deltY = var_Y / var_YNumber  # 铸坯在宽度方向的空间间隔
    BOLTZMAN = 0.000000056684  # 玻尔兹曼常数
    EMISSIVITY = 0.8  # 辐射系数
    next_temp = [[0] * var_YNumber for i in range(var_XNumber)]
    #### equation strat #####
    for i in range(var_XNumber):
        for j in range(var_YNumber):
            if middle_temp[i][j] >= var_liqTemp:
                rou = var_rouL
                specificHeat = var_specificHeatL
                Tconductivity = var_TconductivityL
            if middle_temp[i][j] <= var_SodTemp:
                rou = var_rouS
                specificHeat = var_specificHeatS
                Tconductivity = var_TconductivityS
            if (var_SodTemp < middle_temp[i][j]) & (var_liqTemp > middle_temp[i][j]):
                rou = (var_rouS - var_rouL) * (var_liqTemp -
                                               middle_temp[i][j]) / (var_liqTemp - var_SodTemp) + var_rouL
                Tconductivity = (var_TconductivityS) * (var_liqTemp - middle_temp[i][j]) / (
                            var_liqTemp - var_SodTemp) + var_m * (
                                        1 - (var_liqTemp - middle_temp[i][j]) / (
                                            var_liqTemp - var_SodTemp)) * var_TconductivityL
                specificHeat = (var_specificHeatS - var_specificHeatL) * (var_liqTemp - middle_temp[i][j]) / (
                        var_liqTemp - var_SodTemp) + var_specificHeatL + var_latentHeatofSolidification / (
                                           var_liqTemp - var_SodTemp)
            # a1 = Tconductivity/(rou*specificHeat)
            a = (Tconductivity * var_deltTime) / (rou * specificHeat * deltX * deltX)
            b = (Tconductivity * var_deltTime) / (rou * specificHeat * deltY * deltY)
            ##### 四个边的温度 start ######
            if i == 0 and (j != 0 and j != var_YNumber - 1):  # 情况1
                next_temp[i][j] = middle_temp[i][j] + 2 * a * (middle_temp[i + 1][j] - middle_temp[i][j]) + b * (
                            middle_temp[i][j + 1] - 2 * middle_temp[i][j] + middle_temp[i][j - 1])
            if j == 0 and (i != var_XNumber - 1 and i != 0):  # 情况2
                next_temp[i][j] = middle_temp[i][j] + 2 * a * (middle_temp[i][j + 1] - middle_temp[i][j]) + b * (
                            middle_temp[i + 1][j] - 2 * middle_temp[i][j] + middle_temp[i - 1][j])
            if i == var_XNumber - 1 and (j != var_YNumber - 1 and j != 0):  # 情况3
                h_int = h + EMISSIVITY * BOLTZMAN * (
                            middle_temp[i][j] * middle_temp[i][j] + var_temperatureWater * var_temperatureWater) * (
                                    middle_temp[i][j] + var_temperatureWater)
                next_temp[i][j] = middle_temp[i][j] + 2 * a * (middle_temp[i - 1][j] - middle_temp[i][j]) + b * (
                            middle_temp[i][j + 1] - 2 * middle_temp[i][j] + middle_temp[i][j - 1]) - (
                                              2 * h_int * deltX * a * (
                                                  middle_temp[i][j] - var_temperatureWater) / Tconductivity)
            if j == var_YNumber - 1 and (i != var_XNumber - 1 and i != 0):  # 情况4
                h_int = h + EMISSIVITY * BOLTZMAN * (
                            middle_temp[i][j] * middle_temp[i][j] + var_temperatureWater * var_temperatureWater) * (
                                    middle_temp[i][j] + var_temperatureWater)
                next_temp[i][j] = middle_temp[i][j] + 2 * b * (middle_temp[i][j - 1] - middle_temp[i][j]) + a * (
                            middle_temp[i + 1][j] - 2 * middle_temp[i][j] + middle_temp[i - 1][j]) - (
                                              2 * h_int * deltY * b * (
                                                  middle_temp[i][j] - var_temperatureWater) / Tconductivity)
            ##### 四个边的温度 end ######
            ##### 四个角的温度 start ####
            if i == 0 and j == 0:  # 情况5
                next_temp[i][j] = middle_temp[i][j] + 2 * a * (middle_temp[i + 1][j] - middle_temp[i][j]) + 2 * b * (
                            middle_temp[i][j + 1] - middle_temp[i][j])
            if i == 0 and j == var_YNumber - 1:  # 情况6
                h_int = h + EMISSIVITY * BOLTZMAN * (
                            middle_temp[i][j] * middle_temp[i][j] + var_temperatureWater * var_temperatureWater) * (
                                    middle_temp[i][j] + var_temperatureWater)
                next_temp[i][j] = middle_temp[i][j] + 2 * a * (middle_temp[i + 1][j] - middle_temp[i][j]) + 2 * b * (
                            middle_temp[i][j - 1] - middle_temp[i][j]) - (2 * h_int * deltY * b * (
                            middle_temp[i][j] - var_temperatureWater) / Tconductivity)
            if i == var_XNumber - 1 and j == 0:  # 情况7
                h_int = h + EMISSIVITY * BOLTZMAN * (
                            middle_temp[i][j] * middle_temp[i][j] + var_temperatureWater * var_temperatureWater) * (
                                    middle_temp[i][j] + var_temperatureWater)
                next_temp[i][j] = middle_temp[i][j] + 2 * a * (middle_temp[i - 1][j] - middle_temp[i][j]) + 2 * b * (
                            middle_temp[i][j + 1] - middle_temp[i][j]) - (2 * h_int * deltX * a * (
                            middle_temp[i][j] - var_temperatureWater) / Tconductivity)
            if i == var_XNumber - 1 and j == var_YNumber - 1:  # 情况8
                h_int = h + EMISSIVITY * BOLTZMAN * (
                            middle_temp[i][j] * middle_temp[i][j] + var_temperatureWater * var_temperatureWater) * (
                                    middle_temp[i][j] + var_temperatureWater)
                next_temp[i][j] = middle_temp[i][j] + 2 * a * (middle_temp[i - 1][j] - middle_temp[i][j]) + 2 * b * (
                            middle_temp[i][j - 1] - middle_temp[i][j]) - (2 * h_int * deltY * b * (
                            middle_temp[i][j] - var_temperatureWater) / Tconductivity) - (2 * h_int * deltX * a * (
                            middle_temp[i][j] - var_temperatureWater) / Tconductivity)
            ##### 四个角的温度 end ####
            ##### 内部温度 start ####
            if (i != 0 and i != var_XNumber - 1) and (j != 0 and j != var_YNumber - 1):  # 情况9
                next_temp[i][j] = middle_temp[i][j] + a * (
                            middle_temp[i + 1][j] - 2 * middle_temp[i][j] + middle_temp[i - 1][j]) + b * (
                                              middle_temp[i][j + 1] - 2 * middle_temp[i][j] + middle_temp[i][j - 1])
            ##### 内部温度 end ####
    #### equation end #####
    #    print("一次开始")
    #    print( next_temp)
    #    print("一次结束")
    return next_temp


def steady_temp_cal(var_dis, var_VcastOriginal, var_deltTime, MiddleTemp, var_XNumber, var_YNumber, var_X, var_Y,
                    var_temperatureWater, var_rouS, var_rouL, var_specificHeatS, var_specificHeatL, var_TconductivityS,
                    var_TconductivityL, var_liqTemp, var_SodTemp, var_m, var_latentHeatofSolidification, Time_all,
                    time_Mold, var_h_initial, var_sliceNumber, var_castingTemp):
    NextTemp = [([0] * var_YNumber) for i in range(var_XNumber)]
    # MiddleTemp_all =[([([var_castingTemp]*Time_all)]*var_YNumber) for i in range(var_XNumber)]

    MiddleTemp_all = [0] * var_XNumber
    for i in range(var_XNumber):
        MiddleTemp_all[i] = [0] * var_YNumber
    for i in range(var_XNumber):
        for j in range(var_YNumber):
            MiddleTemp_all[i][j] = [0] * Time_all
    t = []
    for i in range(Time_all):
        t.append([[0 for i in range(var_XNumber)] for j in range(var_YNumber)])

    for stepTime in range(Time_all):
        if stepTime <= time_Mold:
            tTime = var_deltTime * (stepTime + 1);
            h = 1000 * (0.07128 * math.exp(-tTime) + 2.328 * math.exp(-tTime / 9.5) + 0.698)
            # print("h",h)
            NextTemp = two_densonal_diff(h, var_deltTime, MiddleTemp, var_XNumber, var_YNumber, var_X, var_Y,
                                         var_temperatureWater, var_rouS, var_rouL, var_specificHeatS, var_specificHeatL,
                                         var_TconductivityS, var_TconductivityL, var_liqTemp, var_SodTemp, var_m,
                                         var_latentHeatofSolidification)
        else:
            disNow = var_dis[0] + stepTime * var_VcastOriginal * var_deltTime
            # print("disNow",disNow)
            if var_dis[1] <= disNow <= var_dis[2]:
                h = var_h_initial[0]
                # print("23123",h)
            if var_dis[2] < disNow <= var_dis[3]:
                h = var_h_initial[1]
                # print("21111123",h)
            if var_dis[3] < disNow <= var_dis[4]:
                h = var_h_initial[2]
            if var_dis[4] < disNow <= var_dis[5]:
                h = var_h_initial[3]
            NextTemp = two_densonal_diff(h, var_deltTime, MiddleTemp, var_XNumber, var_YNumber, var_X, var_Y,
                                         var_temperatureWater, var_rouS, var_rouL, var_specificHeatS, var_specificHeatL,
                                         var_TconductivityS, var_TconductivityL, var_liqTemp, var_SodTemp, var_m,
                                         var_latentHeatofSolidification)
        for i in range(var_XNumber):
            for j in range(var_YNumber):
                MiddleTemp[i][j] = NextTemp[i][j]
                MiddleTemp_all[i][j][stepTime] = NextTemp[i][j]
                t[stepTime][i][j] = NextTemp[i][j]
    return MiddleTemp_all, t