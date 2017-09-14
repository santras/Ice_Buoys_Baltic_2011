import numpy as np
from count_distdir import count_dist
from simple_tools import test_open, make_sdatetime,check_tmatch
from simple_tools import search_min, search_max
# Takes a file that includes the filenames then opens each file at a time. Loads the contect into variables then counts
# time difference between measurements, the distance and direction with count_dist from count_distdir and finally the speed.

# Sanna: Tämä näyttäisi toimivan ainakin tässä spesifissä tilanteessa kun Kandi kansion alla on Data kansio ja Simple Tools kansio.
# Pitänee vielä tarkistaa miten nimi failin loppu hoidetaan tässä ja kirjoittaa muutama juttu ylös.

def get_names(name):
    # Open file that includes the  filenames needed, names stored as variable names, then file is closed.
    file1 = open(name, "r")
    fnames=file1.readlines()
    file1.close()
    return fnames

def check_time(ye,mon,dat,ho,min):
    t_diff=[99999.99]
    check=[0]                       # This 1 if time difference is okey = 1 hour, else 0
    co=0                            # How many bad time differences in measurements
    for ind in range(len(ye)-1):
        is_tdiff=check_tmatch('hours',1,ye[ind+1],mon[ind+1],dat[ind+1],ho[ind+1],min[ind+1],0,ye[ind],mon[ind],dat[ind],ho[ind],min[ind])
        if is_tdiff:
            check.append(1)
        else:
            co=co+1
            check.append(0)
        t_diff.append((make_sdatetime(ye[ind+1],mon[ind+1],dat[ind+1],ho[ind+1],min[ind+1])-make_sdatetime(ye[ind],mon[ind],dat[ind],ho[ind],min[ind])).total_seconds())
    return t_diff, check


def load_data(name):
    c1, ye, mon, dat, ho, min, pressure, hulltemp, airtemp, c10, c11, c12, c13, c14, lat, lon, c17, c18, c19  = np.loadtxt(name, unpack=True)
    return ye,mon,dat,ho,min,lat,lon

def check_minmax(lat,lon):
    (mini_lat,index_minlat)=search_min(lat)
    (maxi_lat,index_maxlat)=search_max(lat)
    (mini_lon,index_minlon)=search_min(lon)
    (maxi_lon,index_maxlon)=search_max(lon)
    #print('lat',mini_lat, index_minlat, maxi_lat,index_maxlat)
    #print('lon',mini_lon, index_minlon, maxi_lon, index_maxlon)
    minmax=(mini_lat, index_minlat, maxi_lat, index_maxlat, mini_lon, index_minlon, maxi_lon,index_maxlon)
    return minmax

def num_print(ye,mon,dat,ho,min,time_diff,tcheck,lat,lon,travel_dist,travel_dir,travel_speed):
    iye=int(ye)
    imon=int(mon)
    idat=int(dat)
    iho=int(ho)
    imin=int(min)
    itime_diff=int(time_diff)   #:.5 digits :>10 right :10left '{:10.5}'
    #print('here')
    outstring="{}\t{}\t{}\t{}\t{}\t{}\t{}\t{:<10.6}\t{:<10.6}\t{:<15.7}\t{:<15.7}\t{:<15.7}\n".format(iye,imon,idat,iho,imin,itime_diff,tcheck,lat,lon,travel_dist,travel_dir,travel_speed)
    #print(outstring)
    return outstring

def write_file(ind,ye,mon,dat,ho,min,time_diff,tcheck,lat,lon,travel_dist,travel_dir,travel_speed):
    nimi='poiju'+ind.__str__()+'.txt'
    print(nimi)
    try:
        file1=open(nimi,'w')
        for aa in range(len(ye)):
            #print(ye[aa],mon[aa],dat[aa],ho[aa],min[aa],time_diff[aa],tcheck[aa],lat[aa],lon[aa],travel_dist[aa],travel_dir[aa],travel_speed[aa])
            print_string=num_print(ye[aa],mon[aa],dat[aa],ho[aa],min[aa],time_diff[aa],tcheck[aa],lat[aa],lon[aa],travel_dist[aa],travel_dir[aa],travel_speed[aa])
            file1.write(print_string)
        file1.close()
        okey=True
    except:
        okey=False

    return okey


# def check_dataset_minmax(table):
#     (mini_lat,index_minlat)=(search_min(table[:][0]))
#     (maxi_lat,index_maxlat)=search_max(table[:][2])
#     (mini_lon,index_minlon)=search_min(table[:][4])
#     (maxi_lon,index_maxlon)=search_max(table[:][6])
#     return index_minlat, index_maxlat,index_minlon,index_maxlon


# def compare_maxminlat(lat_maxmin,lat_dataset_maxmin,lon_maxmin,lon_dataset_maxmin,ind):
#     if ind==0:
#         print(lat_maxmin)
#         lat_dataset_maxmin=[ind,lat_maxmin[0],lat_maxmin[1],ind,lat_maxmin[2],lat_maxmin[3]]
#         lon_dataset_maxmin=[ind,lon_maxmin[0],lon_maxmin[1],ind,lon_maxmin[2],lon_maxmin[3]]
#     else:
#         if lat_maxmin[0]<lat_dataset_maxmin[1]:         #update lat min
#             lat_dataset_maxmin=[ind,lat_maxmin[0],lat_maxmin[1],lat_dataset_maxmin[3],lat_dataset_maxmin[4],lat_dataset_maxmin[5]]
#         if lat_maxmin[2]>lat_dataset_maxmin[4]:         #update lat max
#             lat_dataset_maxmin=[lat_dataset_maxmin[0],lat_dataset_maxmin[1],lat_dataset_maxmin[2],ind,lat_maxmin[2],lat_maxmin[3]]
#         if lon_maxmin[0]<lon_dataset_maxmin[1]:         #update lon min
#             lon_dataset_maxmin=[ind,lon_maxmin[0],lon_maxmin[1],lon_dataset_maxmin[3],lon_dataset_maxmin[4],lon_dataset_maxmin[5]]
#         if lon_maxmin[2]>lon_dataset_maxmin[4]:         #update lon max
#             lon_dataset_maxmin=[lon_dataset_maxmin[0],lon_dataset_maxmin[1],lon_dataset_maxmin[2],ind,lon_maxmin[2],lon_maxmin[3]]
#
#     return lat_dataset_maxmin,lon_dataset_maxmin


def data_prepare():
    #For real
    names=get_names("nimet.txt")
    #For test
    #names=['../Data/asc_JB3850.txt']
    #minmaxes = np.full([9,8], np.nan)   #### I think this is a problem
    #minmaxes=[]
    for i in range(len(names)):                                                            # Going through the list of names 1 by 1
        name=(names[i].strip())                                                                 # Cleaning whitespace
        if name and not name.isspace():                                                         #If name is not empty line or whitespace
            openable=test_open(name,True)                                                            # Testing if file can be opened and opening it if possible
            if openable:                                                                        # Unpacking to variables
                (year,month,date,hour,minutes,latitude,longitude)=load_data(name)
                (time_difference,tcheck)=check_time(year,month,date,hour,minutes)
                travel_distance=[99999.99]
                travel_speed=[99999.99]
                travel_direction=[99999.99]

                (aaa,bbb)=count_dist(latitude,longitude)
                for index2 in range(len(aaa)):                                                  # Travel distance + Direction
                    travel_distance.append(aaa[index2])
                    travel_direction.append(bbb[index2])
                #print(travel_direction[0:3])

                for index3 in range(1,len(aaa)+1):
                    if (time_difference[index3] != 0.0):                                                  # Travel Speed
                        if time_difference[index3]==0.0:
                            print('böö',time_difference[index3])
                        bunny=(travel_distance[index3]/time_difference[index3])
                        travel_speed.append(bunny)
                    else:
                        print('Double measurement or something wrong here',[index3])

                file_minmax=check_minmax(latitude,longitude)
                #print('fileminmax: ',file_minmax)
                #minmaxes.append(file_minmax)
                #minmaxes[i,:]=file_minmax[:]
                #print('table: ',minmaxes)

                write_ok=write_file(i,year,month,date,hour,minutes,time_difference,tcheck,latitude,longitude,travel_distance,travel_direction,travel_speed)
                print('Write to file: ',i,write_ok)



        else:
            # the string is empty
            print('This line of names file is empty.')



    #print(minmaxes)
    #print(minmaxes[:,3])
    #(find_minlat,find_maxlat,find_minlon,find_maxlon)=check_dataset_minmax(minmaxes)
    #print('Minimum lat file:',find_minlat,' index:',minmaxes[find_minlat,1],' value:',minmaxes[find_minlat,0])
    #print('Maximum lat file:',find_maxlat,' index:',minmaxes[find_maxlat,1],' value:',minmaxes[find_maxlat,0])
    #print('Minimum lon file:',find_minlon,' index:',minmaxes[find_minlon,1],' value:',minmaxes[find_minlon,0])
    #print('Maximum lon file:',find_maxlon,' index:',minmaxes[find_maxlon,1],' value:',minmaxes[find_maxlon,0])

    #Something is wrong with this part

    # Jatkosuunnitelmat osuutta:
    # Tämän voisi vielä ehkä yleistää niin että failien nimet voi antaa failina tai paramerina listalta sekä toisesta tiedostosta
    # tieto mikä on mikäkin sarake ja lisäksi parametrina funktiolle mitä sieltä halutaan hakea.



def main():
    data_prepare()




if __name__ == '__main__':
    main()
