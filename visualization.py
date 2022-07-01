from this import d
import matplotlib.pyplot as plt
import numpy as np
import requests
import json
from pprint import pp, pprint
from datetime import datetime

data = requests.get("http://192.168.0.19:7500/dados")
data_arr = json.loads(data.text)

# agrupando os dados por hora
data_arr_grouped_per_hour = {}
for i in data_arr:
    time = datetime.strptime(i[3], "%Y-%m-%d %H:%M:%S.%f")

    if time.hour not in data_arr_grouped_per_hour:
        data_arr_grouped_per_hour[time.hour] = []
        data_arr_grouped_per_hour[time.hour].append(i)

    else:
        data_arr_grouped_per_hour[time.hour] 

#ordenar keys do dicionario crescentemente
data_arr_grouped_per_hour_keys = sorted(data_arr_grouped_per_hour.keys())

#reduzindo os dados para apenas os valores da média
for hour in range(0, 24):
    try: 
        arr = data_arr_grouped_per_hour[hour]
        comfort = []
        uberX = []
        moto = []

        for i in arr:
            comfort.append(float(i[0]))
            uberX.append(float(i[1]))
            moto.append(float(i[2]))            

        # calculando a média
        comfort_mean = np.mean(comfort)
        uberX_mean = np.mean(uberX)
        moto_mean = np.mean(moto)

        data_arr_grouped_per_hour[hour] = [comfort_mean, uberX_mean, moto_mean]
    except KeyError:
        pass

plt.plot(data_arr_grouped_per_hour_keys, data_arr_grouped_per_hour.values())
#legend 
plt.legend(['Comfort', 'UberX', 'Moto'])
plt.xlabel('Hora')
plt.ylabel('Valor')
plt.xticks(np.arange(0, 24, 1))
plt.grid(color="grey", linestyle='dotted', linewidth=1)
plt.show()
