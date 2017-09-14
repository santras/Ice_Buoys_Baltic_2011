#!/usr/bin/env python
# coding: utf-8

# The purpose of this is to make simple tools that may occur a lot in other situations
# Function 1:
# test_open(fname,show_file=False) returns boolean true if file given as fname opens
# Function 2:
# make_datetime(year, month=1, day=1, hour=0, min=0, sec=0, mcsec=0) return t_datetime
# make_datetime Month, day.. optional, input as integer
# Function 3:
# make_sdatetime(year, month='1', day='1', hour='0', min='0', sec='0', mcsec='0') return t_datetime
# make_sdatetime Month, day.. optional, input as string, int, float.
# If input is float notice that day=5.6 will count days to 5 without minutes to mach the 0.6, so basically same as floor(5.6)
# Function 4:
# check_tmatch(comp_input,comp_value,yyyy1,mm1=1,dd1=1,hh1=0,min1=0,sec1=0,yyyy2=-9999,mm2=1,dd2=1,hh2=0,min2=0,sec2=0,mcs1=0,mcs2=0) return okey
# Check if time interval match the type compe_input value comp_value for example days,5 returns okey True if match
# Notice time difference is a match no matter wich order times are given, so remember to use a check in your code if it's spesific
# Function 5:
# check_tmore(comp_input,comp_value,yyyy1,mm1=1,dd1=1,hh1=0,min1=0,sec1=0,yyyy2=-9999,mm2=1,dd2=1,hh2=0,min2=0,sec2=0,mcs1=0,mcs2=0) return okey
# Check if time interval is more than the type comp_input value comp_value for example days,5 returns okey True if is over
# Notice time difference is a match no matter wich order times are given, so remember to use a check in your code if it's spesific
# Function 6:
# check_tless(comp_input,comp_value,yyyy1,mm1=1,dd1=1,hh1=0,min1=0,sec1=0,yyyy2=-9999,mm2=1,dd2=1,hh2=0,min2=0,sec2=0,mcs1=0,mcs2=0) return okey
# Check if time interval is less than the type comp_input value comp_value for example days,5 returns okey True if is less
# Notice time difference is a match no matter wich order times are given, so remember to use a check in your code if it's spesific
# Function 7:
# def search_min(numbers) return min, index_of_min
# Function 8:
# def search_max(numbers) return max, index_of_max

import datetime


def test_open(fname,show_file=False):
    # Tests if opening file works, returns boolean True if opens
    okey=False
    try:
        file2=open(fname,"r")
    except FileNotFoundError:
        print("Can't find file " +fname )
    except TypeError:
        print("Something went wrong, and can't open file")
    else:
        if show_file==True:
            print('Opening file: ' +fname)
        file2.close()
        okey=True
    return okey

def make_datetime(year, month=1, day=1, hour=0, min=0, sec=0, mcsec=0):
    t_datetime=datetime.datetime(year,month,day, hour,min,sec,mcsec)
    return t_datetime

def make_sdatetime(year, month='1', day='1', hour='0', min='0', sec='0', mcsec='0'):
    ts_datetime=datetime.datetime(int(year),int(month),int(day),int(hour),int(min),int(sec),int(mcsec))
    return ts_datetime

def check_tmatch(comp_input,comp_value,yyyy1,mm1=1,dd1=1,hh1=0,min1=0,sec1=0,yyyy2=-9999,mm2=1,dd2=1,hh2=0,min2=0,sec2=0,mcs1=0,mcs2=0):
    if yyyy2==-9999:
        print('Second year needed, give in format yyyy2=year')
        exit()
    if comp_input=='days':
        time1=make_sdatetime(yyyy1,mm1,dd1,hh1,min1,sec1,mcs1)
        time2=make_sdatetime(yyyy2,mm2,dd2,hh2,min2,sec2,mcs2)
        if time1>=time2:
            if (time1-time2)==datetime.timedelta(days=comp_value):
                okey=True
            else:
                okey=False
        else:
            if (time2-time1)==datetime.timedelta(days=comp_value):
                okey=True
            else:
                okey=False

    elif comp_input=='hours':
        time1=make_sdatetime(yyyy1,mm1,dd1,hh1,min1,sec1,mcs1)
        time2=make_sdatetime(yyyy2,mm2,dd2,hh2,min2,sec2,mcs2)
        if time1>=time2:
            if (time1-time2)==datetime.timedelta(hours=comp_value):
                okey=True
            else:
                okey=False
        else:
            if (time2-time1)==datetime.timedelta(hours=comp_value):
                okey=True
            else:
                okey=False
    elif comp_input=='minutes':
        time1=make_sdatetime(yyyy1,mm1,dd1,hh1,min1,sec1,mcs1)
        time2=make_sdatetime(yyyy2,mm2,dd2,hh2,min2,sec2,mcs2)
        if time1>=time2:
            if (time1-time2)==datetime.timedelta(minutes=comp_value):
                okey=True
            else:
                okey=False
        else:
            if (time2-time1)==datetime.timedelta(minutes=comp_value):
                okey=True
            else:
                okey=False
    elif comp_input=='seconds':
        time1=make_sdatetime(yyyy1,mm1,dd1,hh1,min1,sec1,mcs1)
        time2=make_sdatetime(yyyy2,mm2,dd2,hh2,min2,sec2,mcs2)
        if time1>=time2:
            if (time1-time2)==datetime.timedelta(seconds=comp_value):
                okey=True
            else:
                okey=False
        else:
            if (time2-time1)==datetime.timedelta(seconds=comp_value):
                okey=True
            else:
                okey=False
    elif comp_input=='microseconds':
        time1=make_sdatetime(yyyy1,mm1,dd1,hh1,min1,sec1,mcs1)
        time2=make_sdatetime(yyyy2,mm2,dd2,hh2,min2,sec2,mcs2)
        if time1>=time2:
            if (time1-time2)==datetime.timedelta(microseconds=comp_value):
                okey=True
            else:
                okey=False
        else:
            if (time2-time1)==datetime.timedelta(microseconds=comp_value):
                okey=True
            else:
                okey=False
    return okey

def check_tmore(comp_input,comp_value,yyyy1,mm1=1,dd1=1,hh1=0,min1=0,sec1=0,yyyy2=-9999,mm2=1,dd2=1,hh2=0,min2=0,sec2=0,mcs1=0,mcs2=0):
    if yyyy2==-9999:
        print('Second year needed, give in format yyyy2=year')
        exit()
    if comp_input=='days':
        time1=make_sdatetime(yyyy1,mm1,dd1,hh1,min1,sec1,mcs1)
        time2=make_sdatetime(yyyy2,mm2,dd2,hh2,min2,sec2,mcs2)
        if time1>=time2:
            if (time1-time2)>datetime.timedelta(days=comp_value):
                okey=True
            else:
                okey=False
        else:
            if (time2-time1)>datetime.timedelta(days=comp_value):
                okey=True
            else:
                okey=False

    elif comp_input=='hours':
        time1=make_sdatetime(yyyy1,mm1,dd1,hh1,min1,sec1,mcs1)
        time2=make_sdatetime(yyyy2,mm2,dd2,hh2,min2,sec2,mcs2)
        if time1>=time2:
            if (time1-time2)>datetime.timedelta(hours=comp_value):
                okey=True
            else:
                okey=False
        else:
            if (time2-time1)>datetime.timedelta(hours=comp_value):
                okey=True
            else:
                okey=False
    elif comp_input=='minutes':
        time1=make_sdatetime(yyyy1,mm1,dd1,hh1,min1,sec1,mcs1)
        time2=make_sdatetime(yyyy2,mm2,dd2,hh2,min2,sec2,mcs2)
        if time1>=time2:
            if (time1-time2)>datetime.timedelta(minutes=comp_value):
                okey=True
            else:
                okey=False
        else:
            if (time2-time1)>datetime.timedelta(minutes=comp_value):
                okey=True
            else:
                okey=False
    elif comp_input=='seconds':
        time1=make_sdatetime(yyyy1,mm1,dd1,hh1,min1,sec1,mcs1)
        time2=make_sdatetime(yyyy2,mm2,dd2,hh2,min2,sec2,mcs2)
        if time1>=time2:
            if (time1-time2)>datetime.timedelta(seconds=comp_value):
                okey=True
            else:
                okey=False
        else:
            if (time2-time1)>datetime.timedelta(seconds=comp_value):
                okey=True
            else:
                okey=False
    elif comp_input=='microseconds':
        time1=make_sdatetime(yyyy1,mm1,dd1,hh1,min1,sec1,mcs1)
        time2=make_sdatetime(yyyy2,mm2,dd2,hh2,min2,sec2,mcs2)
        if time1>=time2:
            if (time1-time2)>datetime.timedelta(microseconds=comp_value):
                okey=True
            else:
                okey=False
        else:
            if (time2-time1)>datetime.timedelta(microseconds=comp_value):
                okey=True
            else:
                okey=False
    return okey

def check_tless(comp_input,comp_value,yyyy1,mm1=1,dd1=1,hh1=0,min1=0,sec1=0,yyyy2=-9999,mm2=1,dd2=1,hh2=0,min2=0,sec2=0,mcs1=0,mcs2=0):
    if yyyy2==-9999:
        print('Second year needed, give in format yyyy2=year')
        exit()
    if comp_input=='days':
        time1=make_sdatetime(yyyy1,mm1,dd1,hh1,min1,sec1,mcs1)
        time2=make_sdatetime(yyyy2,mm2,dd2,hh2,min2,sec2,mcs2)
        if time1>=time2:
            if (time1-time2)<datetime.timedelta(days=comp_value):
                okey=True
            else:
                okey=False
        else:
            if (time2-time1)<datetime.timedelta(days=comp_value):
                okey=True
            else:
                okey=False

    elif comp_input=='hours':
        time1=make_sdatetime(yyyy1,mm1,dd1,hh1,min1,sec1,mcs1)
        time2=make_sdatetime(yyyy2,mm2,dd2,hh2,min2,sec2,mcs2)
        if time1>=time2:
            if (time1-time2)<datetime.timedelta(hours=comp_value):
                okey=True
            else:
                okey=False
        else:
            if (time2-time1)<datetime.timedelta(hours=comp_value):
                okey=True
            else:
                okey=False
    elif comp_input=='minutes':
        time1=make_sdatetime(yyyy1,mm1,dd1,hh1,min1,sec1,mcs1)
        time2=make_sdatetime(yyyy2,mm2,dd2,hh2,min2,sec2,mcs2)
        if time1>=time2:
            if (time1-time2)<datetime.timedelta(minutes=comp_value):
                okey=True
            else:
                okey=False
        else:
            if (time2-time1)<datetime.timedelta(minutes=comp_value):
                okey=True
            else:
                okey=False
    elif comp_input=='seconds':
        time1=make_sdatetime(yyyy1,mm1,dd1,hh1,min1,sec1,mcs1)
        time2=make_sdatetime(yyyy2,mm2,dd2,hh2,min2,sec2,mcs2)
        if time1>=time2:
            if (time1-time2)<datetime.timedelta(seconds=comp_value):
                okey=True
            else:
                okey=False
        else:
            if (time2-time1)<datetime.timedelta(seconds=comp_value):
                okey=True
            else:
                okey=False
    elif comp_input=='microseconds':
        time1=make_sdatetime(yyyy1,mm1,dd1,hh1,min1,sec1,mcs1)
        time2=make_sdatetime(yyyy2,mm2,dd2,hh2,min2,sec2,mcs2)
        if time1>=time2:
            if (time1-time2)<datetime.timedelta(microseconds=comp_value):
                okey=True
            else:
                okey=False
        else:
            if (time2-time1)<datetime.timedelta(microseconds=comp_value):
                okey=True
            else:
                okey=False
    return okey

def search_min(numbers):
    mymin=numbers[0]
    min_ind=0
    for index in range(len(numbers)):
        if numbers[index]<mymin:
            mymin=numbers[index]
            min_ind=index
    return mymin,min_ind

def search_max(numbers):
    mymax=numbers[0]
    max_ind=0
    for index in range(len(numbers)):
        if numbers[index]>mymax:
            mymax=numbers[index]
            max_ind=index
    return mymax,max_ind

def main():
    print('Main of simple tools.')

if __name__ == '__main__':
    main()
