from simple_tools import test_open
import pandas as pd
from windrose import plot_windrose
from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
from my_wind_rose import make_wind_rose
from my_scatter_plots import make_scatter, make_diff_test,make_dirtests
from count_some_stats import statis
from numpy.random import random
from numpy import arange
import os

# For making scatter plots from buoy data and some hists
small_speed=0.0125
small_wind_speed=2.0









#Function 1
def check_data(speed,dire,wind,wdir):
    # Turns the wind direcxtion to opposite, wind was given as from where it blows instead of to where it blows
    # Removes nans(except when speed 0)
    # Changes variables to floats
    # Divides variables into components
    # First 4 variables are just cleaned up versions of the data and the second 4 are the components


    # Turning the wind around
    new_dir=[]
    for ind in range(len(wdir)):
        if float(wdir[ind])>=180:
            new_dir.append(float(wdir[ind])-180)
        else:
            new_dir.append(float(wdir[ind])+180)
    wdir=new_dir

    xx=[]
    yy=[]
    wx=[]
    wy=[]
    n_speed=[]
    n_dir=[]
    n_wind=[]
    n_wdir=[]
    cont=True
    cont2=True
    for ind in range(len(speed)):               # components
        if np.isnan(float(speed[ind])):
            dummy=1
        elif np.isnan(float(wind[ind])):
            dunno=1
        else:                           # only continue if both speeds not nans
            if np.isnan(float(dire[ind])):
                cont=False              # False if direction nans other than when speed is 0
                if float(speed[ind])==0:
                    cont=True
            if  np.isnan(float(wdir[ind])):
                cont2=False
                if float(wind[ind])==0:
                    cont2=True
            if (cont==False) or (cont2==False):
                don=1
            else:                               #buoy
                if float(speed[ind])==0:                                    # being lazy with commenting instead of removing
                    xx.append(0.0)               # Speed is 0 case
                    yy.append(0.0)
                    n_speed.append(0.0)
                    n_dir.append(np.nan)
                    a=1
                #elif float(speed[ind])<small_speed:
                   # a=1

                else:
                    xx.append(float(speed[ind])*np.cos(float(dire[ind])))
                    yy.append(float(speed[ind])*np.sin(float(dire[ind])))
                    n_speed.append(float(speed[ind]))
                    n_dir.append(float(dire[ind]))
                if float(wind[ind])==0:                            # wind
                    wx.append(0.0)                          # speed is 0 case
                    wy.append(0.0)
                    n_wind.append(0.0)
                    n_wdir.append(np.nan)
                    a=1
                #elif float(wind[ind])<small_wind_speed:
                  #  a=1
                else:
                    wx.append(float(wind[ind])*np.cos(float(wdir[ind])))
                    wy.append(float(wind[ind])*np.sin(float(wdir[ind])))
                    n_wind.append(float(wind[ind]))
                    n_wdir.append(float(wdir[ind]))




    return n_speed,n_dir,n_wind,n_wdir,xx,yy,wx,wy





















def main():

    # Variables for holding all the data
    sp_all=[]
    dr_all=[]
    wsp_all=[]
    wdr_all=[]
    spx_all=[]
    spy_all=[]
    wsx_all=[]
    wsy_all=[]

    for i in range(0,9):              #(0,9):           # Change later          # Going through all files one by one
        fname=("c_poiju_"+str(i)+"dailymean.txt").strip()
        if os.path.exists(fname):
            openable=test_open(fname)
            if not openable:
                print("Couldn't open file",fname)
                exit("Exiting")
            data = pd.read_csv((fname), sep="\t", header=None, names=["month", "day","speed","speed_nz","direction",  "wind_speed", "wind_nz", "wind_dir"])

        # Turning wind direction around since it was given as from where instead of to where
        # Removing some nans for uknonwn reason, leaving only with speed=0
        # Changing variables into floats
        # Dividing into components spx,spy  wsx,wsy
            (sp,dr,wsp,wdr,spx,spy,wsx,wsy)=check_data(data.speed,data.direction,data.wind_speed,data.wind_dir) # Function 1

        # Adding to variables that hold the whole data
            for ind in range(len(sp)):
                sp_all.append(sp[ind])
                dr_all.append(dr[ind])
                wsp_all.append(wsp[ind])
                wdr_all.append(wdr[ind])
                spx_all.append(spx[ind])
                spy_all.append(spy[ind])
                wsx_all.append(wsx[ind])
                wsy_all.append(wsy[ind])

        # PITÄISKÖ Käännänkö suunnan oikein? Onhan poijun suunta laskettu oikein? Ks kaikki data ensin ennen kuin alat muuttelemaan
        # HERE ALL THE CALLS TO MAKE PICS FROM INDIVIDUAL FILES - Do I need all?
        #Making a scatter plots
            plot_title='Poijun ja tuulen nopeudet, poiju '+str(i)   # Function 2
            plot_title2='Poijun ja tuulen suunnat, poiju '+str(i)
        #make_scatter(wsp,sp,'Nopeus [m/s]',my_title=plot_title)
        #make_scatter(wdr,dr,'Suunta [astetta]',my_title=plot_title2)
            plot_title='Poijun ja tuulen x- komponentin nopeudet, poiju '+str(i)
            plot_title2='Poijun ja tuulen y- komponentin nopeudet, poiju '+str(i)
        #make_scatter(wsx,spx,'x-komponentin nopeus [m/s]',my_title=plot_title)  # Function 2
        #make_scatter(wsy,spy,'y-komponentin nopeus [m/s]',my_title=plot_title2)
        #make_wind_rose(sp,dr,ww=False,i=i)
        #make_wind_rose(wsp,wdr,ww=True,i=i)
        #statis(dr,sp,wsp,wdr,i)

    # HERE ALL THE CALLS TO MAKE PICS FROM THE WHOLE DATASET
    # Check also pictures folder... all updated?
    make_scatter(wsp_all,sp_all,'Nopeus [m/s]',my_title="Poijun ja tuulen nopeudet")         # Function 2
    make_scatter(wdr_all,dr_all,'Suunta [astetta]', my_title="Poijun ja tuulen suunnat")
    make_scatter(wsx_all,spx_all,'x-komponentin nopeus [m/s]',my_title="Poijun ja tuulen x- komponentin nopeudet")  # Function 2
    make_scatter(wsy_all,spy_all,'y-komponentin nopeus [m/s]',my_title="Poijun ja tuulen y- komponentin nopeudet")
    make_diff_test(sp_all,spx_all,spy_all,wsp_all,wsx_all,wsy_all,label_str1="Poijun",label_str2="tuulen",scaler=0.02)    # Function 3
    make_dirtests(wdr_all,dr_all,"tuulen","poijun",dirturn=20,rr=[-180,180])
    make_wind_rose(sp_all,dr_all,ww=False,i=99)
    make_wind_rose(wsp_all,wdr_all,ww=True,i=99)
    statis(dr_all,sp_all,wsp_all,wdr_all,99)

if __name__ == '__main__':
    main()
