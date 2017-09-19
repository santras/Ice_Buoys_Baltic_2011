#!/usr/bin/env python
# coding: utf-8

# Purpose of code is to add wind data to exsisting data



import numpy as np
import pandas as pd
from simple_tools import test_open
from count_distdir import distance
import datetime

path='E:\Weather_Data\\'
namefile='nimet.txt'


def load_namefile():            # Should be okey
    openable=test_open((path+namefile),True)
    if not openable:
        exit("Can't access namefile for weather stations.")
    stations = pd.read_csv((path+namefile), sep=",", header=None, names=["sta_num", "sta_name", "sta_lat","sta_lon"])
    #print (stations)
    return(stations.sta_num,stations.sta_name,stations.sta_lat,stations.sta_lon)

def get_data(num,name):
        for i in range(len(name)):
            station=""
            station=path+(name[i].strip())
            # here first file open
            station_1=station+"_1.csv"
            #print(station)
            (wind,dir,date)=load_data(station_1)
            if num[i]!=11:
                station_2=station+"_2.csv"
                (wind2,dir2,date2)=load_data(station_2)
            for index in range(len(wind2)):
                wind.append(wind2[index])
                dir.append(dir2[index])
                date.append(date2[index])       # up here all good
            (nwind,ndir,ndate)=fill_missing(wind,dir,date)
            outname=(name[i].strip())+'.txt'
            f1=open(outname,'w')
            for ind in range(len(nwind)):
                try:
                    outstring="{:20}\t{:10.6}\t{:10.6}\n".format(ndate[ind],str(nwind[ind]),str(ndir[ind]))
                    f1.write(outstring)
                except:
                    print('We got problems: ',outname,ind)
            f1.close()

def load_data(name):
    openable=test_open(name,True)
    if not openable:
        exit("Can't open file: ",name)
    (data,opened)=load_file(name)
    if not opened:
        exit("Something went wrong loading data from the file.")
    wdate=[]
    wdate_av=[]
    wind_raw=[]
    wdir_raw=[]
    wind=[]
    wdir=[]
    year=[]
    month=[]
    day=[]
    hour=[]
    min=[]
    for ind in range(0,len(data)):      # Header is of different lengths in each file
        #print((data[ind])[0:28])
        #print(len("time,t2m,ws_10min,wg_10min"))
        if (data[ind])[0:26]=="time,t2m,ws_10min,wg_10min":
            #print("here",ind)
            header=ind
    #print(header)
    for index in range(header+1,len(data)):
        wdate.append(((data[index]).split(','))[0])
        wind_raw.append(float((((data[index]).split(','))[2]).strip()))
        wdir_raw.append(float((((data[index]).split(','))[4]).strip()))
    print("wind_raw/wind_raw div 6: ",len(wind_raw),(len(wind_raw)/6))

    for index in range(0,len(wdate)):
        if (len(wdate[index]))!=0:
            year.append((wdate[index])[0:4])
            month.append(((wdate[index])[5:7]))
            day.append(((wdate[index])[8:10]))
            hour.append(((wdate[index])[11:13]))
            min.append(((wdate[index])[14:16]))
    #print(len(data),len(wdate),len(hour))
    count=0
    start=0
    for inde in range(len(hour)-1):
        if hour[inde]!=hour[inde+1]:
            if count>0:
                count=count+1
                wind.append(np.nanmean(wind_raw[start:start+count]))
                wdir.append(np.nanmean(wdir_raw[start:start+count]))
                wdate_av.append(wdate[start+count])
                #here next average
                count=0
                start=inde+1
                #print("Here", day[start+count],month[start+count])
        else:
            count=count+1
    #print(wind_raw[0:6])
    #print(wind[0])
    #print(len(wind_raw[0:99]))
    for ind2 in range(len(wind)):
        if wind[ind2]==0:
            wdir[ind2]=np.nan
    print("Wind: ",len(wind))
    return(wind,wdir,wdate_av)


def load_file(name):
    try:
        file=open(name,'r')
        data=file.readlines()
        file.close()
        okey=True
    except:
        data=[]
        okey=False

    return data,okey

def fill_missing(wind,wdir,date):
    new_wind=[]
    new_wdir=[]
    new_date=[]
    year=[]
    month=[]
    day=[]
    hour=[]

    for index in range(len(wind)):
        if (len(date[index]))!=0:
            year.append(int((date[index])[0:4]))
            month.append(int(((date[index])[5:7])))
            day.append(int(((date[index])[8:10])))
            hour.append(int(((date[index])[11:13])))

    for ind in range(len(wind)-1):
        if ind == 0:
            new_wind.append(wind[ind])      # when okey, okey for all
            new_wdir.append(wdir[ind])
            new_date.append(date[ind])

        date_index=datetime.datetime(year[ind],month[ind],day[ind],hour[ind])
        date_forward=datetime.datetime(year[ind+1],month[ind+1],day[ind+1],hour[ind+1])
        if (date_forward-date_index) == (datetime.timedelta(seconds=3600)):
            new_wind.append(wind[ind+1])      # when okey, okey for all
            new_wdir.append(wdir[ind+1])
            new_date.append(date[ind+1])
        else:                               # not okey... and keep going untill better
            date_now=date_index
            while (date_forward-date_now) > (datetime.timedelta(seconds=3600)):
                    # if (date_forward-date_now) < (datetime.timedelta(seconds=3600)):        # Just incase I messed up
                    #     print("Warning something weird happened at index: ",ind)
                        #exit("Stopping")
                    # Adding some padding
                day_padding=date_now+datetime.timedelta(seconds=3600)   # Time +1 h
                new_date.append(str(day_padding.date())+"T{:.5}".format(str(day_padding.time())))    # The extra day
                new_wind.append(np.nan)                                          # Here others
                new_wdir.append(np.nan)
                date_now=day_padding    # Last line in while... updating date_now
            new_wind.append(wind[ind+1])      # The normal after while ends..
            new_wdir.append(wdir[ind+1])
            new_date.append(date[ind+1])
    #print(date[len(date)-1])
    #print(new_date[len(new_date)-1])
    # Double check okey
    # year=[]
    # month=[]
    # day=[]
    # hour=[]
    # for isec in range(len(new_date)):
    #     if (len(date[index]))!=0:
    #         year.append(int((date[index])[0:4]))
    #         month.append(int(((date[index])[5:7])))
    #         day.append(int(((date[index])[8:10])))
    #         hour.append(int(((date[index])[11:13])))
    # for isec2 in range(len(year)-1):
    #     date_index=datetime.datetime(year[ind],month[ind],day[ind],hour[ind])
    #     date_forward=datetime.datetime(year[ind+1],month[ind+1],day[ind+1],hour[ind+1])
    #     if (date_forward-date_index) == (datetime.timedelta(seconds=3600)):
    #         print("Warning")

    #print(len(wind),len(new_wind))
    print("Filled: ",len(new_wind))
    return new_wind, new_wdir,new_date







def main():
    (sta_num,sta_name,sta_lat,sta_lon)=load_namefile()
    #print(sta_num,sta_name)
    get_data(sta_num,sta_name)



if __name__ == '__main__':
    main()
