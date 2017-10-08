from simple_tools import test_open
import pandas as pd
from windrose import plot_windrose
from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
from numpy.random import random
from numpy import arange

# Code for making windrose originally from http://youarealegend.blogspot.fi/search/label/windrose.
# Modified by Sanna 2.10.2017

def make_wind_rose(sp,dr,i,ww):  # Next xhange my own data into it
    if ww==True:
        if i==99:
            titlestring="Virtausruusu kaikkista tuulen suunnista ja nopeuksista"
        else:
            titlestring="Virtausruusu poijuun "+str(i) +" yhdistetyistä tuulen suunnista ja nopeuksista"
    else:
        if i==99:
            titlestring="Virtausruusu kaikkien poijujen suunnista ja nopeuksista"
        else:
            titlestring="Virtausruusu poijun "+str(i) +" suunnista ja nopeuksista"


    #Create wind speed and direction variables
    #ws = random(500)*6
    #wd = random(500)*360
   # A stacked histogram with normed (displayed in percent) results :

    ax = new_axes()
    ax.bar(dr, sp, normed=True, opening=0.8, edgecolor='white')
    set_legend(ax)
    plt.title(titlestring,fontsize=18,y=1.1)   #loc="left"
    plt.show()

#A quick way to create new windrose axes...
def new_axes():
    fig = plt.figure(figsize=(8, 8.5), dpi=80, facecolor='w', edgecolor='w')
    rect = [0.2, 0.1, 0.6, 0.8] #[0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect, facecolor='w')
    fig.add_axes(ax)
    return ax

    #...and adjust the legend box
def set_legend(ax):
    l = ax.legend(borderaxespad=-5.5)  #-0.10) #Brings legend out of the plot or into the plot, more - -> more out
    plt.setp(l.get_texts(), fontsize=8)





def main():
    sp_all=[]
    dr_all=[]
    wsp_all=[]
    wdr_all=[]
    for i in range(0,9):              #(0,9):           # Change later
        fname=("poiju"+str(i)+"_wind2.txt").strip()
        #openable=test_open(fname)
        #if not openable:
        #    print("Couldn't open file",fname)
        #    exit("Exiting")
        data = pd.read_csv((fname), sep="\t", header=None, names=["year", "month", "day","hour", "minute",
              "time_diff", "time_check", "latitude", "longitude", "distance", "direction", "speed", "wind_speed", "wind_dir"])

        sp=[]
        dr=[]
        wsp=[]
        wdr=[]
        for ind in range(len(data.speed)):
            if not (np.isnan(float(data.direction[ind]))):
                sp.append(float(data.speed[ind]))
                dr.append(int(round(float(data.direction[ind]))))
                sp_all.append(float(data.speed[ind]))
                dr_all.append(int(round(float(data.direction[ind]))))
            if not (np.isnan(float(data.wind_dir[ind]))):
                wsp.append(float(data.wind_speed[ind]))
                wdr.append(int(round(float(data.wind_dir[ind]))))
                wsp_all.append(float(data.wind_speed[ind]))
                wdr_all.append(int(round(float(data.wind_dir[ind]))))
        ww=False
        make_wind_rose(sp,dr,i,ww)              # Making pic for individual buoys and connected wind
        ww=True
        make_wind_rose(wsp,wdr,i,ww)

    # Making pic for all buoys and wind
    i=99
    ww=False
    make_wind_rose(sp_all,dr_all,i,ww)              # Making pic for individual buoys and connected wind
    ww=True
    make_wind_rose(wsp_all,wdr_all,i,ww)


if __name__ == '__main__':
    main()
