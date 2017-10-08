from simple_tools import test_open
import pandas as pd
import numpy as np

all_poiju=[]
# Tämä skripti poisti datasta kaikki yli 0,65m/s nopeudet ja muutti ne nan arvoiksi
for i in range(0,9):              #(0,9):           # Change later
    fname="poiju"+str(i)+"_wind.txt"
    outname="poiju"+str(i)+"_wind2.txt"
    openable=test_open(fname)
    if not openable:
        print("Couldn't open file",fname)
        exit("Exiting")
    data = pd.read_csv((fname), sep="\t", header=None, names=["year", "month", "day","hour", "minute",
            "time_diff", "time_check", "latitude", "longitude", "distance", "direction", "speed", "wind_speed", "wind_dir"])

    new_speed=[]
    new_dir=[]
    new_wind=[]
    new_wind_dir=[]
    for ind in range(len(data.speed)):
        if data.speed[ind]>0.65:
            print(i,ind,data.speed[ind], str(data.wind_speed[ind]),str(data.wind_dir[ind]))
            new_speed.append(np.nan)
            new_dir.append(np.nan)
        else:
            new_speed.append(data.speed[ind])
            new_dir.append(float(data.direction[ind]))
        new_wind_dir.append(float(data.wind_dir[ind]))
        new_wind.append(float(data.wind_speed[ind]))


    f1=open(outname,'w')
    for ind in range(len(data)):
       # try:
        outstring="{:4}\t{:2}\t{:2}\t{:2}\t{:2}\t{:10.6}\t{:2.3}\t{:10.6}\t{:10.6}\t{:10.6}" \
                    "\t{:10.6}\t{:10.6}\t{:10.6}\t{:10.6}\n".format(data.year[ind],data.month[ind],data.day[ind],data.hour[ind],data.minute[ind],data.time_diff[ind],
                    data.time_check[ind],data.latitude[ind],data.longitude[ind],data.distance[ind],new_dir[ind],new_speed[ind],new_wind[ind],new_wind_dir[ind])
        f1.write(outstring)
        #except:
        #print('We got problems: ',outname,ind)
    f1.close()

