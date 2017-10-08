
#!/usr/bin/env python
# coding: utf-8

# Purpose of code is to add wind data to exsisting data

# What if the match is not found?


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from simple_tools import test_open


def load_file(name):            # Used should be okey
    try:
        file=open(name,'r')
        data=file.readlines()
        file.close()
        okey=True
    except:
        data=[]
        okey=False

    return data,okey


def make_hist(data,poiju):
    if poiju==99:
        label_string='Histogrammi kaikista nopeuksista' #muutettu tuuli
    elif poiju==88:
        label_string='Histogrammi kaikkien poijujen nopeuksista, täysin paikallaan olleet  nopeus=0 m/s poistettu'
    else:
         label_string='Histogrammi poijun '+str(poiju+1)+' nopeuksista' # muutettu tuuli

    fig = plt.figure()
    plt.xlabel('Nopeus m/s',fontsize=18)
    plt.ylabel('Havaintojen määrä',fontsize=18)

    plt.title(label_string,fontsize=20)
    plt.grid(True)
    #sns.distplot(data,bins='auto',label=label_string,kde=False,hist_kws={'histtype': 'stepfilled','color':'#1E4033'})
    plt.hist(data,bins='auto',color='#8E9F99')    # testing to add cumulative and density, bins='auto' log=True
    plt.show()


def prepare_histdata(data):
    old_data=[]             # This for wind
    try:
        for ii in range(len(data)):
            old_data.append(float(data[ii]))
    except:
        print("Here problem: prepare_histdata")
    new_data=[]
    for ind in range(len(old_data)):
        if (old_data[ind]<90000):
            if np.isfinite(old_data[ind]):
                new_data.append(old_data[ind])
    # This is very dirty to get the bins work, makes everything outside to be in the limit
    #new_data=np.clip(new_data,0,(np.percentile(new_data,99.3)))
    #print(new_data[0:3])
    #print(len(data),len(new_data))
    return new_data

def non_zero_prepare(data):
    new_data=[]
    for ind in range(len(data)):
        if data[ind]!=0:
            new_data.append(data[ind])
    return new_data

def time_okey(data, time_ok):
    new_data=[]
    for ind in range(len(data)):
        if time_ok[ind]==1:
            new_data.append(data[ind])
    return new_data



def main():
    all_poiju=[]
    for i in range(0,9):              #(0,9):           # Change later
        fname="poiju"+str(i)+"_wind2.txt"
        openable=test_open(fname)
        if not openable:
            print("Couldn't open file",fname)
            exit("Exiting")
        data = pd.read_csv((fname), sep="\t", header=None, names=["year", "month", "day","hour", "minute",
              "time_diff", "time_check", "latitude", "longitude", "distance", "direction", "speed", "wind_speed", "wind_dir"])
        hist_speed=prepare_histdata(data.speed)    # Changed to wind
        hist_speed=time_okey(hist_speed,data.time_check)
        print(i,len(hist_speed))
        for ind in range(len(hist_speed)):
            all_poiju.append(hist_speed[ind])
        make_hist(hist_speed,i)

        #hist_speed=non_zero_prepare(hist_speed)
        #make_hist(hist_speed)

        #make_hist(data.direction)
        #make_hist(data.wind_speed,i)
        #make_hist(data.wind_dir)
        #print(data.longitude[0:3])
    print('Kaikki poijut',len(all_poiju))
    all_poiju=prepare_histdata(all_poiju)
    make_hist(all_poiju,99)
    #all_poiju=non_zero_prepare(all_poiju)
    #make_hist(all_poiju,88)

if __name__ == '__main__':
    main()
