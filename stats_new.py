from simple_tools import test_open
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from count_some_stats import statis
import datetime
from geopy.distance import vincenty


# This is actually about making avearages of day, week and month and writing them into a file
# There is some without speed==0 or wind_speed==0






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
        dates=[]            # datenum of measurement time
        weeknums=[]         # number of week for measurement time
        # Counting day averages
        #print(len(data))
        for ind in range(len(data)):
            dates.append(datetime.datetime(int(data.year[ind]),int(data.month[ind]),int(data.day[ind]),int(data.hour[ind])))
        for ind in range(len(dates)):
            weeknums.append((dates[ind].strftime('%W')))

        thisind=0
        # month_c not actual month but month count, month would be min(np.unique(data.month))+month_c
        monthly_mean=[]
        weekly_mean=[]
        daily_mean=[]
        for month_c in range(max(np.unique(data.month))):
            mmonth=[]           # Montly values
            mweek=[]
            mday=[]
            msp=[]
            mspnonz=[]
            mdr=[]
            mwsp=[]
            mwspnonz=[]
            mwdr=[]
            mlat=[]
            mlon=[]
            mdist=[]


            for ind in range(len(data)):
                if (min(np.unique(data.month))+month_c)==data.month[ind]:
                    #mmonth.append(int((data.month[ind])))
                    mweek.append(int(weeknums[ind]))
                    mday.append(int(data.day[ind]))
                    msp.append(float(data.speed[ind]))
                    if not float(data.speed[ind])==0.0:
                        mspnonz.append(float(data.speed[ind]))
                    else:
                        mspnonz.append(np.nan)
                    mdr.append(float(data.direction[ind]))
                    mwsp.append(float(data.wind_speed[ind]))
                    if not float(data.wind_speed[ind])==0.0:
                        mwspnonz.append(float(data.wind_speed[ind]))
                    else:
                        mwspnonz.append(np.nan)
                    mwdr.append(float(data.wind_dir[ind]))
                    # try:
                    #     print("lat:",float(data.latitude[ind]))
                    # except:
                    #     print("here problem:",i,ind)
                    mlat.append(float(data.latitude[ind]))
                    mlon.append(float(data.longitude[ind]))
                    if data.time_check[ind]==1:
                        mdist.append(float(data.distance[ind]))
                    else:
                        mdist.append(np.nan)


            #print(len(mdist),i,(min(np.unique(data.month))+month_c))
            if len(mweek)>372:  # Half of the measurements needs to be there for the mean to count
                first_coord=(mlat[0],mlon[0])
                second_coord=(mlat[-1],mlon[-1])
                mdirect_dist=(vincenty(first_coord, second_coord).meters)
                #print(msp[0:10])
                monthly_mean.append([(min(np.unique(data.month))+month_c),np.nanmean(msp),np.nanmean(mspnonz),np.nanmean(mdr),np.nanmean(mwsp),np.nanmean(mwspnonz),
                                    np.nanmean(mwdr),np.nanmin(mlat),np.nanmin(mlon),np.nanmax(mlat),np.nanmax(mlon),np.nansum(mdist),mdirect_dist])
            for week_c in range(len(np.unique(mweek))):
                wday=[]         # weekly values
                wsp=[]
                wspnonz=[]
                wdr=[]
                wwsp=[]
                wwspnonz=[]
                wwdr=[]
                wlat=[]
                wlon=[]
                wdist=[]

                for ind in range(len(mweek)):
                    if (min(np.unique(mweek))+week_c)==mweek[ind]:
                        wday.append(mday[ind])
                        wsp.append(msp[ind])
                        wspnonz.append(mspnonz[ind])
                        wdr.append(mdr[ind])
                        wwsp.append(mwsp[ind])
                        wwspnonz.append(mwspnonz[ind])
                        wwdr.append(mwdr[ind])
                        wlat.append(mlat[ind])
                        wlon.append(mlon[ind])
                        wdist.append(mdist[ind])
                if len(wday)>84:
                    #if wlat[0]
                    first_coord=(wlat[0],wlon[0])
                    second_coord=(wlat[-1],wlon[-1])
                    wdirect_dist=(vincenty(first_coord, second_coord).meters)
                    weekly_mean.append([(min(np.unique(mweek))+week_c),np.nanmean(wsp),np.nanmean(wspnonz),np.nanmean(wdr),np.nanmean(wwsp),np.nanmean(wwspnonz),np.nanmean(wwdr),
                                        np.nanmin(wlat),np.nanmin(wlon),np.nanmax(wlat),np.nanmax(wlon),np.nansum(wdist),wdirect_dist])

                for day_c in range(len(np.unique(wday))):
                    dsp=[]          # daily values
                    dspnonz=[]
                    ddr=[]
                    dwsp=[]
                    dwspnonz=[]
                    dwdr=[]
                    for ind in range(len(wday)):
                        if (min(np.unique(wday))+day_c)==wday[ind]:
                            dsp.append(wsp[ind])
                            dspnonz.append(wspnonz[ind])
                            ddr.append(wdr[ind])
                            dwsp.append(wwsp[ind])
                            dwspnonz.append(wwspnonz[ind])
                            dwdr.append(wwdr[ind])
                    if len(dsp)>12:
                        daily_mean.append([(min(np.unique(data.month))+month_c),(min(np.unique(wday))+day_c),np.nanmean(dsp),np.nanmean(dspnonz),np.nanmean(ddr),np.nanmean(dwsp),
                                           np.nanmean(dwspnonz),np.nanmean(dwdr)])

            #print(len(month_val))
        #print(monthly_mean)
        outname="a_poiju_"+str(i)+"monthlymean.txt"
        outname2="b_poiju_"+str(i)+"weeklymean.txt"
        outname3="c_poiju_"+str(i)+"dailymean.txt"

        #transposed=[]
        #    for i in range(7):
         #       transposed.append([row[i] for row in monthly_mean])
        #print(len(monthly_mean))
        #print(np.shape(monthly_mean))
        #print(np.shape(monthly_mean),len(monthly_mean))




        ################ Huomio tuulet eivät ole käännettyjä!



        if not len(monthly_mean)==0:
            f1=open(outname,'w')
            for ind in range(len(monthly_mean)):
                outstring="{:2}\t{:10.6}\t{:10.6}\t{:10.6}\t{:10.6}\t{:10.6}\t{:10.6}\t{:8.4}\t{:8.4}\t{:10.8}\t{:10.8}\n".format(monthly_mean[ind][0],monthly_mean[ind][1],
                    monthly_mean[ind][3],monthly_mean[ind][4],monthly_mean[ind][6],monthly_mean[ind][7],monthly_mean[ind][8],monthly_mean[ind][9],monthly_mean[ind][10],monthly_mean[ind][11],monthly_mean[ind][12])
                f1.write(outstring)
            f1.close()

        if not len(weekly_mean)==0:
            f2=open(outname2,'w')
            for ind in range(len(weekly_mean)):
                outstring2="{:2}\t{:10.6}\t{:10.6}\t{:10.6}\t{:10.6}\t{:10.6}\t{:10.6}\t{:8.4}\t{:8.4}\t{:10.8}\t{:10.8}\n".format(weekly_mean[ind][0],weekly_mean[ind][1],
                        weekly_mean[ind][3],weekly_mean[ind][4],weekly_mean[ind][6],weekly_mean[ind][7],weekly_mean[ind][8],weekly_mean[ind][9],weekly_mean[ind][10],
                                                                                                                                                 weekly_mean[ind][11],weekly_mean[ind][12])
                f2.write(outstring2)
            f2.close()

        if not len(daily_mean)==0:
            f3=open(outname3,'w')
            for ind in range(len(daily_mean)):
                outstring3="{:2}\t{:2}\t{:10.6}\t{:10.6}\t{:10.6}\t{:10.6}\t{:10.6}\t{:10.6}\n".format(daily_mean[ind][0],daily_mean[ind][1],daily_mean[ind][2],daily_mean[ind][3],daily_mean[ind][4],
                        daily_mean[ind][5],daily_mean[ind][6],daily_mean[ind][7])
                f3.write(outstring3)
            f3.close()
        #except:
        #print('We got problems: ',outname,ind)




        #statis(direction,speed,wind_speed,wind_dir,i)
    #statis(all_direction,all_speed,all_wind_speed,all_wind_dir,99)




if __name__ == '__main__':
    main()
