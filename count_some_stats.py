from simple_tools import test_open
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

smallwind=2.0
smallspeed=0.0125


def statis(direction,speed,wind_speed,wind_dir,i):
    new_speed=[]        #non nans
    new_wspeed=[]       # non nans
    new_dir=[]          # non small speed cases
    new_wdir=[]         # non small wind speed cases
    non_small_speed=[]  # non small speed cases
    non_small_wspeed=[] # non small wind speed cases
    countnan=0          # buoy speed nan
    countnanw=0         # wind speed nan
    countnans=0         # nans with both buyou speed and wind speed
    countzeros=0        # buoy speed =0.0
    countsmall=0        # buoy speed <=0,0125m/s but > 0
    countzerosw=0       # wind speed 0
    countsmallw=0       # wind speed <2m/s but >0
    countsmalls=0       # both wind speed and buoy speed is small
    countzerosmallw=0   # buyou speed 0 and wins speed small
    std=[]
    wstd=[]
    countcount=0
    countcountw=0

    for ind in range(len(speed)):
        if np.isnan(speed[ind]):
            countnan=countnan+1
            if np.isnan(wind_speed[ind]):
                countnans=countnans+1
        else:
            new_speed.append(speed[ind])
            std.append(np.abs(np.nanmean(speed)-speed[ind]))
            countcount=countcount+1
            if speed[ind]==0.0:
                countzeros=countzeros+1
                if wind_speed[ind]<=smallwind:
                    countzerosmallw=countzerosmallw+1
            elif speed[ind]<=smallspeed:
                countsmall=countsmall+1
                if wind_speed[ind]<=smallwind:
                    countsmalls=countsmalls+1
            else:
                new_dir.append(wind_dir[ind])
                non_small_speed.append(speed[ind])
        if np.isnan(wind_speed[ind]):
            countnanw=countnanw+1
        else:
            new_wspeed.append(wind_speed[ind])
            wstd.append(np.abs(np.nanmean(wind_speed)-wind_speed[ind]))
            countcountw=countcountw+1
            if wind_speed[ind]==0.0:
                countzerosw=countzerosw+1
            elif wind_speed[ind]<=smallwind:
                countsmallw=countsmallw+1
            else:
                new_wdir.append(wind_dir[ind])
                non_small_wspeed.append((wind_speed[ind]))

    print("Self counted nan:",countnan,"wind nan;",countnanw,"both nans",countnans)
    print("Self counted zeros:",countzeros,"wind zeros;",countzerosw)
    print("Self counted small:",countsmall,"wind small;",countsmallw,"both small",countsmalls,"speed 0, wind small",countzerosmallw)

    print("Number of measurements in ",i,": ",len(speed))

    print("Max speed ",i,": ",np.nanmax(speed))
    print("Min speed ",i,": ",np.nanmin(speed))

    print("Max wind speed ",i,": ",np.nanmax(wind_speed))
    print("Min wind speed ",i,": ",np.nanmin(wind_speed))

    print("Mean speed ",i,": ",np.nanmean(speed))
    print("Mean wind speed ",i,": ",np.nanmean(wind_speed))

    (histo_speed,bins)=np.histogram(new_speed,bins=[0,0.1,0.2,0.3,0.4,0.5,0.6],range=[0,0.6])
    #plt.hist(speed,bins=bins,range=[0,0.65])
    print("Histogramme speed: ",histo_speed)

    #plt.show()
    print("Moode speed ",i,": ",stats.mode(speed,nan_policy="omit")[0]," with count of: ",stats.mode(speed,nan_policy="omit")[1])
    (histo_dir,bins_d)=np.histogram(direction,bins=[0,30,60,90,120,150,180,210,240,270,300,330],range=[0,360])
    print("Histogramme direction original: ",histo_dir)
    (histo_dir2,bins_d)=np.histogram(new_dir,bins=[0,30,60,90,120,150,180,210,240,270,300,330],range=[0,360])
    print("Histogramme direction no small or stationary: ",histo_dir2)
    print("Moode direction ",i,": ",stats.mode(direction,nan_policy="omit")[0]," with count of: ",stats.mode(direction,nan_policy="omit")[1])

    (histo_speed_w,bins_w)=np.histogram(new_wspeed,bins=[0,1,3,7,13,20,32],range=[0,32])
    print("Histogramme wind speed no small or stationary: ",histo_speed_w)

    print("Moode wind speed ",i,": ",stats.mode(wind_speed,nan_policy="omit")[0]," with count of: ",stats.mode(wind_speed,nan_policy="omit")[1])
    (histo_dir_w,bins_d_w)=np.histogram(wind_dir,bins=[0,30,60,90,120,150,180,210,240,270,300,330],range=[0,360])
    print("Histogramme wind direction original: ",histo_dir_w)
    (histo_dir_w,bins_d_w)=np.histogram(new_wdir,bins=[0,30,60,90,120,150,180,210,240,270,300,330],range=[0,360])
    print("Histogramme wind direction no small or stationary: ",histo_dir_w)
    print("Moode wind direction ",i,": ",stats.mode(wind_dir,nan_policy="omit")[0]," with count of: ",stats.mode(wind_dir,nan_policy="omit")[1])

    print("Percentiles speed: ",np.nanpercentile(speed,[25,50,75]))
    print("Non small count",len(non_small_speed))
    print("Percentiles speed no small or stationary: ",np.percentile(non_small_speed,[25,50,75]))
    print("Percentiles wind speed: ",np.nanpercentile(wind_speed,[25,50,75]))
    print("Non small count",len(non_small_wspeed))
    print("Percentiles speed no small or stationary: ",np.percentile(non_small_wspeed,[25,50,75]))

    print("Standard deviation of speed",np.std(~np.isnan(speed)))
    print("Standard deviation of wind speed",np.std(~np.isnan(wind_speed)))
    print("My std speed:",np.sum(std)/countcount)
    print("My std wind speed:",np.sum(wstd)/countcountw)
    print("--------------------------------------------------------------------")








def main():
    all_poiju=[]
    all_direction=[]
    all_speed=[]
    all_wind_dir=[]
    all_wind_speed=[]
    for i in range(0,9):              #(0,9):           # Change later
        fname="poiju"+str(i)+"_wind2.txt"
        openable=test_open(fname)
        if not openable:
            print("Couldn't open file",fname)
            exit("Exiting")
        data = pd.read_csv((fname), sep="\t", header=None, names=["year", "month", "day","hour", "minute",
                "time_diff", "time_check", "latitude", "longitude", "distance", "direction", "speed", "wind_speed", "wind_dir"])

        direction=[]
        speed=[]
        wind_speed=[]
        wind_dir=[]
        for ind in range(len(data)):
            direction.append(float(data.direction[ind]))
            all_direction.append(float(data.direction[ind]))
            speed.append(float(data.speed[ind]))
            all_speed.append(float(data.speed[ind]))
            wind_speed.append(float(data.wind_speed[ind]))
            all_wind_speed.append(float(data.wind_speed[ind]))
            wind_dir.append(float(data.wind_dir[ind]))
            all_wind_dir.append(float(data.wind_dir[ind]))

        statis(direction,speed,wind_speed,wind_dir,i)
    statis(all_direction,all_speed,all_wind_speed,all_wind_dir,99)






if __name__ == '__main__':
    main()
