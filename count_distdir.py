import math
import numpy as np
from geopy.distance import vincenty


def mid_point(k1,k2):               # Counts middle point between 2 coordinate pairs
    if k2>=k1:
        mid=((k2-k1)*0.5)+k1
    else:
        mid=((k1-k2)*0.5)+k2
    return mid

def lat_change(lat1,lat2,lon):      # Distance if only lat would change
    coor1=(lat1,lon)
    coor2=(lat2,lon)
    lat_dis=(vincenty(coor1,coor2).m)
    return lat_dis

def lon_change(lon1,lon2,lat):                   # Distance if only lon would change
    coor1=(lat,lon1)
    coor2=(lat,lon2)
    lon_dis=(vincenty(coor1,coor2).m)
    return lon_dis


def distance(c1,c2):
    tan_dist=(vincenty(c1,c2).m)       # Actual distance
    #print(tan_dist)
    mid_lat=mid_point(c2[0],c1[0])
    mid_lon=mid_point(c2[1],c1[1])
    lat_dist=lat_change(c1[0],c2[0],mid_lon)
    lon_dist=lon_change(c1[1],c2[1],mid_lat)
    #print(lat_dist, lon_dist)

    # DOES THIS PART WOKR RIGHT TEST?
    if (lat_dist == 0.0) and (lon_dist == 0.0):                             # No movement
        alpha=np.nan
    elif lat_dist==0:                                                       # Only lon movement:
        if c2[1]>c1[1]:                                                     # Eastwardly
            alpha=0.0
        else:                                                               # Westwardly
            alpha=180.0
    elif lon_dist==0:                                                       # Only lat movement:
        if c2[0]>c1[0]:                                                     # Northwardly
            alpha=90.0
        else:                                                               # Southwardly
            alpha=270.0
    elif (lon_dist != 0.0) and (lat_dist != 0.0):
        if (c2[0]>c1[0]) and c2[1]>c1[1]:                                   # north east direction
            alpha=math.degrees(math.atan(lat_dist/lon_dist))
        elif (c2[0]>c1[0]):                                                 # north west direction
            alpha=180-(math.degrees(math.atan(lat_dist/lon_dist)))
        elif c2[1]>c1[1]:                                                   # south east direction
            alpha=360-(math.degrees(math.atan(lat_dist/lon_dist)))
        else:                                                               # south west direction
            alpha=180+(math.degrees(math.atan(lat_dist/lon_dist)))
    else:
        print('Something weird happened')
        exit

    return(tan_dist,alpha)

def count_dist(lat,lon):
    dist=[]
    angle=[]
    for ind in range(len(lat)-1):       # Takes 1 coordinate pair at a time
        coor1=(lat[ind],lon[ind])
        coor2=(lat[ind+1],lon[ind+1])
        (aa,bb)=distance(coor1,coor2)
        dist.append(aa)
        angle.append(bb)
    #print(dist[0:5],angle[0:5])
    return(dist,angle)




def main():
    print('Main of Count distance and direction')
    lati=[65.0,70.0,65.0,70.0,65.0,65.0,70.0,65.0,65.0,65.0]
    loni=[40.0,45.0,40.0,35.0,40.0,40.0,40.0,40.0,45.0,40.0]
    (dd,gg)=count_dist(lati,loni)
    print(gg)
    print(dd)


if __name__ == '__main__':
    main()
