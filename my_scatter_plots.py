from simple_tools import test_open
import pandas as pd
from windrose import plot_windrose
from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
from my_wind_rose import make_wind_rose
from numpy.random import random
from numpy import arange

# For making scatter plots from buoy data and some hists

#Function 1
def check_data(speed,dire,wind,wdir):
    # Turns the wind direcxtion to opposite, wind was given as from where it blows instead of to where it blows
    # Removes nans(except when speed 0)
    # Changes variables to floats
    # Divides variables into components
    # First 4 variables are just cleaned up versions of the data and the second 4 are the components
    countnan=0

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
                if float(speed[ind])==0:
                    xx.append(0.0)               # Speed is 0 case
                    yy.append(0.0)
                    n_speed.append(0.0)
                    n_dir.append(np.nan)
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
                else:
                    wx.append(float(wind[ind])*np.cos(float(wdir[ind])))
                    wy.append(float(wind[ind])*np.sin(float(wdir[ind])))
                    n_wind.append(float(wind[ind]))
                    n_wdir.append(float(wdir[ind]))




    return n_speed,n_dir,n_wind,n_wdir,xx,yy,wx,wy


#Function 2
def make_scatter(xval,yval,tolabel,label_s=[],my_title=[]):
    if label_s==[]:
        xlabel_string='Tuulen '+tolabel
        ylabel_string='Poijun '+tolabel
    elif len(label_s)==1:
        xlabel_string=label_s+tolabel
        ylabel_string=label_s+tolabel
    elif len(label_s)>2:
        print("label_s variable should be of length 1 or 2")
        return
    else:
        xlabel_string=label_s[0]+tolabel
        ylabel_string=label_s[1]+tolabel
    if my_title!=[]:
        plt.title(my_title)
    plt.xlabel(xlabel_string)
    plt.ylabel(ylabel_string)
    plt.plot(xval,yval, 'bo')
    plt.show()



#Function 3
def make_diff_test(axy_item,a_item_x,a_item_y,bxy_item,b_item_x,b_item_y,label_str1="",label_str2="", my_title="nopeusero",scaler=1):
    # Here a_item = buoy, b_item=wind
    dx=[]
    dy=[]
    dxy=[]
    for ind in range (len(a_item_x)):
        dx.append(a_item_x[ind]-(scaler*b_item_x[ind]))             # Here example: wind speed 2,5% of buoy speed -> scaler=0.025
        dy.append(a_item_y[ind]-(scaler*b_item_y[ind]))
        dxy.append(axy_item[ind]-(scaler*bxy_item[ind]))
    if scaler!=1:
        x_label=label_str1+" x-nopeus - "+str(scaler*100)+"% "+label_str2+" x-nopeudesta"
        y_label=label_str1+" y-nopeus - "+str(scaler*100)+"% "+label_str2+" y-nopeudesta"
        xxy_label=label_str1+" nopeus"
        yxy_label=label_str1+" nopeus - " +str(scaler*100)+"% "+label_str2+" nopeudesta"
    else:
        x_label=label_str1+" x-nopeus - "+label_str2+" x-nopeus"
        y_label=label_str1+" y-nopeus - "+label_str2+" y-nopeus"
        xxy_label=label_str1+" nopeus - "+label_str2+" nopeudesta"
        yxy_label=label_str1+" nopeus"

    if (label_str1!="") and (label_str2!=""):
        my_title_komp=label_str1+" ja "+label_str2+" "+my_title+" komponenteittain"
        my_title=label_str1+" ja "+label_str2+" "+my_title
    else:
        my_title_komp=my_title.title()+" komponenteittain"
        my_title=my_title.title()
    plt.title(my_title_komp)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(dx,dy, 'bo')
    #plt.plot([-0.8,0.0,0.8],[0,0,0],'r')
    #plt.plot([0,0,0],[-0.8,0,0.8],'r')
    plt.show()
    plt.title(my_title)
    plt.xlabel(xxy_label)
    plt.ylabel(yxy_label)
    plt.plot(axy_item,dxy,'bo')

    string_hist1="Histogrammi: "+x_label
    string_hist2="Histogrammi: "+y_label
    make_hist(dx,string_hist1,x_label)       # Function4
    make_hist(dy,string_hist2,y_label)

    string_hist_a="Histogrammi: "+yxy_label
    make_hist(dxy,string_hist_a,yxy_label)




#Function4
def make_hist(data,tittle_str,label_str,rr=[],):

    #x_label="Histogrammi "+label_str+" x-nopeudesta"
    #y_label="Histogrammi "+label_str2+" x-nopeudesta"

    #label_string='Histogrammi poijun - 2,5% tuulen nopeuden erosta / '+ii
    fig = plt.figure()
    plt.xlabel(label_str,fontsize=18)
    plt.ylabel('Havaintojen määrä',fontsize=18)

    plt.title(tittle_str,fontsize=20)
    plt.grid(True)
    #sns.distplot(data,bins='auto',label=label_string,kde=False,hist_kws={'histtype': 'stepfilled','color':'#1E4033'})
    if rr==[]:
        plt.hist(data,bins='auto',color='#8E9F99')    # Can also test to add cumulative and density, bins='auto' log=True
    else:
        plt.hist(data,bins='auto',color='#8E9F99',range=rr)    # Can also test to add cumulative and density, bins='auto' log=True
    plt.show()


# Functio 5
def make_dirtests(x_data,y_data,label_x,label_y,dirturn=0 ,rr=[]):

    if dirturn==0:
        title_string="Histogrammi "+label_y+" ja "+label_x+" suunnan erotuksesta"
        xlabel=label_y+" - "+label_x
    else:
        title_string="Histogrammi "+label_y+" ja "+label_x+" suunnan erotuksesta, kun "+label_x+\
                     " suuntaa on käännetty "+str(dirturn)+" astetta oikealle"
        xlabel=label_y+" suunta - "+label_x+" suunta, kun "+label_x+" suuntaa on käännetty oikealle "+str(dirturn)+" astetta"

    new_xdata=[]
    new_ydata=[]
    for ind in range(len(y_data)):
        if (not np.isnan(y_data[ind])) or (not np.isnan(x_data[ind])):
            new_xdata.append(x_data[ind])
            new_ydata.append(y_data[ind])

    x_data=new_xdata
    y_data=new_ydata



    if dirturn!=0:
        new_xdata=[]
        for ind in range (len(x_data)):
            if x_data[ind]>=dirturn:
                new_xdata.append(x_data[ind]-dirturn)
            else:
                new_xdata.append(360-(dirturn-x_data[ind]))
        x_data=new_xdata
    diff=[]
    for ind in range(len(y_data)):
        #if y_data[ind]>=x_data[ind]:
        diff.append(y_data[ind]-x_data[ind])
    for ind in range(len(y_data)):
        if diff[ind]>180:
            diff[ind]=-(360-diff[ind])
        if diff[ind]<(-180):
            diff[ind]=360+diff[ind]




    fig = plt.figure()


    plt.xlabel(xlabel,fontsize=18)
    plt.ylabel('Havaintojen määrä',fontsize=18)

    plt.title(title_string,fontsize=20)
    plt.grid(True)
    #sns.distplot(data,bins='auto',label=label_string,kde=False,hist_kws={'histtype': 'stepfilled','color':'#1E4033'})
    if rr==[]:
        plt.hist(diff,bins='auto',color='#8E9F99')    # testing to add cumulative and density, bins='auto' log=True
    else:
        plt.hist(diff,bins='auto',color='#8E9F99',range=rr)    # testing to add cumulative and density, bins='auto' log=True
    plt.show()










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
        fname=("poiju"+str(i)+"_wind2.txt").strip()
        openable=test_open(fname)
        if not openable:
            print("Couldn't open file",fname)
            exit("Exiting")
        data = pd.read_csv((fname), sep="\t", header=None, names=["year", "month", "day","hour", "minute",
              "time_diff", "time_check", "latitude", "longitude", "distance", "direction", "speed", "wind_speed", "wind_dir"])

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

    # HERE ALL THE CALLS TO MAKE PICS FROM THE WHOLE DATASET
    # Check also pictures folder... all updated?
    #make_scatter(wsp_all,sp_all,'Nopeus [m/s]',my_title="Poijun ja tuulen nopeudet")         # Function 2
    #make_scatter(wdr_all,dr_all,'Suunta [astetta]', my_title="Poijun ja tuulen suunnat")
    #make_scatter(wsx_all,spx_all,'x-komponentin nopeus [m/s]',my_title="Poijun ja tuulen x- komponentin nopeudet")  # Function 2
    #make_scatter(wsy_all,spy_all,'y-komponentin nopeus [m/s]',my_title="Poijun ja tuulen y- komponentin nopeudet")
    make_diff_test(sp_all,spx_all,spy_all,wsp_all,wsx_all,wsy_all,label_str1="Poijun",label_str2="tuulen")    # Function 3
    make_dirtests(wdr_all,dr_all,"tuulen","poijun",dirturn=-10,rr=[-180,180])
    #make_wind_rose(sp_all,dr_all,ww=False,i=99)
    #make_wind_rose(wsp_all,wdr_all,ww=True,i=99)

if __name__ == '__main__':
    main()
