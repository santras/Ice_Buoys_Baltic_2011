#!/usr/bin/env python
# coding: utf-8

# Purpose of code is to add wind data to exsisting data

# What if the match is not found?


import numpy as np
import pandas as pd
from simple_tools import test_open
from count_distdir import distance

path='E:\Weather_Data\\'
namefile='nimet.txt'


def load_namefile():    # In use, should be okey
    openable=test_open((path+namefile),True)
    if not openable:
        exit("Can't access namefile for weather stations.")
    stations = pd.read_csv((path+namefile), sep=",", header=None, names=["sta_num", "sta_name", "sta_lat","sta_lon"])
    #print (stations)
    return(stations.sta_num,stations.sta_name,stations.sta_lat,stations.sta_lon)

def process_buoy(nam,s_num,s_lat,s_lon,s_name):    # In use... need checking
    name=nam+".txt"
    openable=test_open(name,True)
    if not openable:
        print("Can't open file: ",name)
        return
    #print(openable)
    #data = pd.read_csv(name, sep="\t", header=None, names=["year", "month", "day", "hour","min","t_dif","t_check", "lat","lon","dist","speed","dir"])
    data = pd.read_csv(name, sep="\t", header=None, usecols=[0,1,2,3,4,7,8],names=["year", "month", "day", "hour","min","lat","lon"])

    #variables:
    bad_counter=0
    good_counter=0
    #station_numbers=[]
    station_old=""
    stored_index=0
    list_wind=[]
    list_dir=[]
    list_date=[]

    for ii in range(len(data)):
        station=""
        dist_min=9999999                        # So that at least 1 will match in length
        for jj in range (len(s_lat)):           # Counting distance to stations
            ci=(data.lat[ii],data.lon[ii])
            cj=(s_lat[jj],s_lon[jj])
            (dist,gg)=distance(ci,cj)
            if dist<dist_min:                   # update only if smaller
                dist_min=dist
                #station_numbers.append(s_num[jj])           # This is not correct... updates everytime, usage?
                station=('.\\'+(s_name[jj]).strip())+'.txt'
        #print(station)
        if station!=station_old:                #File only opened if not already open
            (wdate,wyear,wmonth,wday,whour,wind,wdir)=open_station(station)
            stored_index=0
            print("Station ",station)
        # Some variables
        #print(wmonth[0:5])
            # here match finding... need checking

        #print(data.month[ii],data.day[ii],data.hour[ii])
        #while not (repeat):
        for index in range(stored_index,len(wind)):       #(len(wind)):
            check=False
            #print(wmonth[index],wday[index])
            if (data.month[ii] == wmonth[index]):
                if (data.day[ii] == wday[index]):
                    if (data.hour[ii]==whour[index]):
                        check=True
                        #print(check)
                        good_counter=good_counter+1
                        list_wind.append(wind[index])
                        #print(wind[index])
                        list_dir.append(wdir[index])
                        list_date.append(wdate[index])
                        stored_index=index
            if not check:
                bad_counter=bad_counter+1
        station_old=station
    print("Bad: ",bad_counter)
    print("Good: ",good_counter)
    print(len(list_date),len(data))          # THIS IS A PROBLEM

    write_out(nam,list_date,list_wind,list_dir)


def open_station(station):
    opened=test_open(station)
    if not opened:
        exit('Problem finding wind data files')
    (wdata,okey)=load_file(station)
    if not okey:
        print("Something went wrong opening file: ",station)
        exit("File opening problematick")

    #print(wdata[12:15])
    # Some variables
    wdate=[]
    wind=[]
    wdir=[]
    wyear=[]
    wmonth=[]
    wday=[]
    whour=[]
    for ind in range(len(wdata)):
        wdate.append(((wdata[ind]).split())[0])
        wind.append(float((((wdata[ind]).split())[1]).strip()))
        wdir.append(float((((wdata[ind]).split())[2]).strip()))
    #print(wdate[0:5]))
    for w_ind in range(len(wdate)):
        wyear.append(int((wdate[w_ind])[0:4]))
        wmonth.append(int(((wdate[w_ind])[5:7])))
        wday.append(int(((wdate[w_ind])[8:10])))
        whour.append(int(((wdate[w_ind])[11:13])))

    return wdate,wyear,wmonth,wday,whour,wind,wdir


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

def write_out(nam,list_date,list_wind,list_dir):
    name=nam+"_wind.txt"
    name_orig=nam+".txt"
    print(name)
    print(name_orig)
    okey=test_open(name_orig)
    if not okey:
        print("Loading file problematic")
        exit()
    #(data,okey)=load_file(name_orig)
    [year,month,day,hour,minute,t_dif,t_check,lat,lon,dist,dire,speed] = np.loadtxt(name_orig, delimiter="\t", unpack=True)
    print(year[0:2])
    f1=open(name,'w')
    for ind in range(len(month)):
        try:
            outstring="{}\t{}\t{}\t{}\t{}\t{:<10}\t{:4}\t{:<10.6}\t{:<10.6}\t{:<15.7}\t{:<15.7}\t{:<15.7}\t{:<15.7}\t{:<15.7}\n".format((str(int((year[ind])))).strip(),
            (str(int((month[ind])))).strip(),(str(int((day[ind])))).strip(),(str(int((hour[ind])))).strip(),(str(int((minute[ind])))).strip(),t_dif[ind],t_check[ind],lat[ind],lon[ind],dist[ind],dire[ind],
            speed[ind],list_wind[ind],list_dir[ind])
            #outstring="{:110}\t{:10.6}\t{:10.6}\t{:10.6}\n".format(data[ind],str(list_wind[ind]),str(list_dir[ind]),list_date[ind])
            f1.write(outstring)
        except:
            print('We got problems: ',name,ind)
    f1.close()



def main():
    (sta_num,sta_name,sta_lat,sta_lon)=load_namefile()  # so far okey
    #print(sta_num, sta_name)

    for i in range(0,9):
        name='poiju'+str(i)
        process_buoy(name,sta_num,sta_lat,sta_lon,sta_name)


if __name__ == '__main__':
    main()
