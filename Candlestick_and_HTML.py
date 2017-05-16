#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 14:09:50 2017
@author: ziaulchoudhury

"""
import csv # read and write csv datasets
import matplotlib.pyplot as plt # plotting
import numpy as np # number
from itertools import groupby, zip_longest # goruping and list's longest index 
import urllib.request # access wabsites
from bs4 import BeautifulSoup # extract HTML dataset
from pylab import rcParams # plot figure size incerase or decrease by programmer choice
import time # execuation time clacualitons

start_time = time.time() # start time

#CSV data-sets
def csv_data(dataf): # for analizing csv datasets
    
    #-------------------Read Data/CSV Files---------------------#
    
    file = open(dataf)
    csv_reader = csv.reader(file)
    next(csv_reader)
    
    date = []
    openn = []
    high = []
    low = []
    close = []
    
    for row in csv_reader:
        date.append(row[0])
        openn.append(row[1])
        close.append(row[4])
        high.append(row[2])
        low.append(row[3])
    
    #-----Revese CSV Data sets since they are in decending order----#
    
    date.reverse()
    openn.reverse()
    high.reverse()
    low.reverse()
    close.reverse()
    
    file.close()
    
    print("CSV DATASETS: ")
    
    #-------------------Aanalize CSV Data---------------------#
    """ 
    Conditions in simple from:
        1. For Bullish engulfing:  
           if ( (day2.high >= day1.high) and (day2.low <= day1.low) and (day2.open <= day1.close) and (day2.close >= day1.open) ) 
        2. For Bearish engulfing:
           if ( (day2.high >= day1.high) and (day2.low <= day1.low) and (day2.open >= day1.close) and (day2.close <= day1.open) )
    """
    
    def itrate_and_compare1(this,prev):
        lis = []
        count = 0
        for i,j in zip(range(1,len(this)),range(1,len(prev))):
            count+=1
            if this[i]>=prev[j-1]:
                lis.append(count)
        return(lis)
    
    def itrate_and_compare2(this,prev):
        lis = []
        count = 0
        for i,j in zip(range(1,len(this)),range(1,len(prev))):
            count+=1
            if this[i]<=prev[j-1]:
                lis.append(count)
        return(lis)
    
    def green_candle(close,openn): # find bullish candlestick
        lis = []
        for i,j in zip(range(0,len(close)),range(0,len(openn))):
            if close[i]>openn[j]:
                lis.append(close)
        return(lis)
    
    def red_candle(close,openn): # find bearish candlestick
        lis = []
        for i,j in zip(range(0,len(close)),range(0,len(openn))):
            if close[i]<openn[j]:
                lis.append(close)
        return(lis)
        
    def green_bullishEn_candle(close,openn): # also for varifying true Bullish engulfing
        lis = []
        count = 0
        for i,j in zip(range(1,len(close)),range(1,len(openn))):
            count+=1
            if close[i]>openn[j] and close[i-1]<openn[j-1]:
                lis.append(count)
        return(lis)
    
    def red_bearishEn_candle(close,openn): # also for varifying true Bearish engulfing
        lis = []
        count = 0
        for i,j in zip(range(1,len(close)),range(1,len(openn))):
            count+=1
            if close[i]<openn[j] and close[i-1]>openn[j-1]:
                lis.append(count)
        return(lis)
    
    def get_year(dates):
        year = []
        for number in dates:              
            monthNum =(number[0:4]) # slacing the year values only from dates
            year.append(monthNum)                  
        return year
    
    def engulfing_dates(index,date): # finding date index 
        Dates = []
        print('- '*40)
        my_list2 = list(index)
        for number in my_list2:
            Dates.append(date[number])
        Dates.sort()
        return (Dates)
    
    def unique_val(years): # get rid of multiple same values
        years.sort()
        br = np.unique(years).tolist() 
        uval_br = ([len(list(group)) for key, group in groupby(years)])
        return (br, uval_br)
    
    def error_mixed_issue(l): # making sure analized data are not mixed
        if l==0:
            s1 = "NO ERROR!! Bull and Bear have unique values and their indeces are not mixed."
            return s1
        else:
            s2 = "ERROR!! Bull and Bear index/indeces is/are mathced, smoething is not right!"
            return s2
        
    def linear_regression(x_val1,x_val2,y_val): # calculate linear_regression
        sum_x = np.array([float(x) for x in y_val])
        sum_y = np.array([float(x + y)/2 for x, y in zip(x_val1,x_val2)])
        fit = np.polyfit(sum_x, sum_y, deg=1)
        return sum_x,sum_y,fit
    
             
    #-------------------------Dataset info--------------------------# 
    
    print('--------CSV Dataset info--------')
    print("Total Candle-sticks Found: ",len(openn))
    print("Total Green Candle-sticks found: ",len((green_candle(close,openn))))
    print("Total Red Candle-sticks found: ",len((red_candle(close,openn))))
    print("Excluidng Others types (Doji and etc.).")
    
    #------------Passing data-sets to methods above to analize-------------# 
       
    bull_bear_high = itrate_and_compare1(high,high)
    bull_bear_low = itrate_and_compare2(low,low)
    bull_cond3 = itrate_and_compare2(openn,close)
    bull_cond4 = itrate_and_compare1(close,openn)
    green = green_bullishEn_candle(close,openn)
    
    bull_index = set(bull_bear_high)&set(bull_bear_low)&set(bull_cond3)&set(bull_cond4)&set(green) # finding indeces for all bullish engulfing

    
    bull_bear_high = itrate_and_compare1(high,high)
    bull_bear_low = itrate_and_compare2(low,low)
    bear_cond3 = itrate_and_compare1(openn,close)
    bear_cond4 = itrate_and_compare2(close,openn)
    red = red_bearishEn_candle(close,openn)
    
    bear_index = set(bull_bear_high)&set(bull_bear_low)&set(bear_cond3)&set(bear_cond4)&set(red) # finding indeces for all bearish engulfing
    
    #----------------------Error Detection-------------------------#
    
    same_val = set(bull_index)&set(bear_index)
    l = error_mixed_issue(len(same_val))
    print(l)
    
    #-----------------------Bullish Dates--------------------------#
    
    bullishDates = engulfing_dates(bull_index,date)

    #-----------------------Bearish Dates--------------------------#
    
    bearishDates = engulfing_dates(bear_index,date)
    
    #-----------------------Bullish Years--------------------------#
    
    bullish_years = (get_year(bullishDates))
    bu, uval_bu = unique_val(bullish_years)  
    
    #-----------------------Bearish Years--------------------------#
    
    bearish_years = (get_year(bearishDates))
    br, uval_br = unique_val(bearish_years)      
    
    return bu, uval_bu, br, uval_br, close, bull_index, bear_index, bullishDates, bearishDates

########################******** END CSV ("csv_data") *********##################################

#HTML data-set 
def HTML_file():
    url = 'http://www.theappletimeline.com/'
    a = urllib.request.urlopen(url)
    soup = BeautifulSoup(a,"lxml")
    
    
    print('-'*10)
    print("HTML DATASET: ")
    #divs = soup.find_all("div", class_="ss-left")
    #divs2 = soup.find_all("div", class_="ss-rught")
    #print(divs,divs2)
    
    date = []
    
    h3s = soup.find_all("h3")
    print("Factched HTML data: ")
    for h3 in h3s:
        dates = (h3.findNext('span').text)
        events = (h3.findNext('p').text)
        print(dates, " : ",events)
        if(events == "Product Release"): #want only one with product release
            date.append(dates)
    print(date)
    
    def get_year(dates):
        year = []
        for number in dates:              #reading row 0,1 for date and time
            monthNum =(number[-4:])
            year.append(monthNum)                  #Storing those values as list
        return year
    
    print(get_year(date))
       
    release_years = (get_year(date))
    release_years.sort()
    ry = np.unique(release_years).tolist()           
    print('Unique Values for years: ', ry)
    uval_ry = ([len(list(group)) for key, group in groupby(release_years)])
    print('Number of product release each year: ', uval_ry)
    
    years = ry
    products = uval_ry
    return years, products
    
########################******** END HTML ("HTML_file") *********##################################

#Plots and export as CSV
def Scatter_plot(x, y): 
    
    plt.close('all')
    rcParams['figure.figsize'] = 12, 5  # fig size by prgrammer choice 
    
    plt.plot(x, y ,color='y')
    plt.scatter(x, y ,color='b', label="Product Release")
    plt.title("HTML Results.")       
    plt.xlabel('Years')                     
    plt.ylabel('Product Releases')                  
    plt.legend(loc = 1,fontsize = 'small')
    plt.savefig("HTML_plot.png")
    plt.show()

def linear_regression(x_val1,x_val2,y_val): # linear regression with np.polyfit()
    
    sum_x = np.array([float(x) for x in y_val])
    sum_y = np.array([float(x + y)/2 for x, y in zip(x_val1,x_val2)])
    fit = np.polyfit(sum_x, sum_y, deg=1)
    return sum_x,sum_y,fit

def plots(x,y,a,b, x2,y2,a2,b2): # Apple: x,y,a,b; Microsoft: x2,y2,a2,b2 for subplots plotting
        
    plt.close('all')
    rcParams['figure.figsize'] = 12, 8
    # Three subplots sharing both x/y axes
    f, (ax1, ax2, ax3) = plt.subplots(3)
    
    ax1.plot(x, y, color='g', label="Bullish")
    ax1.plot(a, b, color='r', label="Bearish")
    ax1.legend(loc = 1,fontsize = 'x-small')
    ax1.set_title('Engulfing (Apple).', color='b')
     
    ax2.plot(x2, y2, color='g', label="Bullish")
    ax2.plot(a2, b2, color='r', label="Bearish")
    ax2.legend(loc = 1,fontsize = 'x-small')
    ax2.set_title('Engulfing (Microsoft).', color='b')
    
    sum_x,sum_y,fit=linear_regression(y,b,x) # liniear fit Apple
    x1 = sum_x
    y1 = sum_y 
    m, b = np.polyfit(x1, y1, 1)

    sum_x2,sum_y2,fit2=linear_regression(y2,b2,x2) # liniear fit Microsoft
    x3 = sum_x2
    y3 = sum_y2 
    m2, b2 = np.polyfit(x3, y3, 1)

    ax3.plot(x1, y1, '*',label="Apple Actual") # linear fit line for both
    ax3.plot(x1, m*x1 + b, '-',label="Apple Linear")
    ax3.plot(x3, y3, '*',label="Microsoft Actual")
    ax3.plot(x3, m2*x3 + b2, '-',label="Microsoft Linear")
    ax3.legend(loc = 1,fontsize = 'x-small')
    ax3.set_title('Linear Regression Between Bullish and Bearish on Both.', color='b')

    f.subplots_adjust(hspace=.3) # space between plots
    plt.setp([a.get_xticklabels() for a in f.axes[1:-1]])
    plt.savefig('multiPlots.png')
    plt.show()
    

def bar_plot(product_years, en_years, bull, bear, products): # for bar plot
    
    def make_data_plotable(product_years, en_years, bull, bear, products): # keeping years of data that  
        product_years = list(map(int, product_years))                  # match with porduct release yeras
        product_years_ = product_years[11:]
        
        en_years = list(map(int, en_years))
        en_years_ = en_years[0:-2]
        
        bull = list(map(int, bull))
        bull_ = bull[0:-2]
        
        bear = list(map(int, bear))
        bear_ = bear[0:-3]
        
        products = list(map(int, products))
        products_ = products[11:]
        
        return ((product_years_),(en_years_),(bull_),(bear_),(products_))
    
    
    (product_years_),(en_years_),(bull_),(bear_),(products_) = make_data_plotable(product_years, 
                                                                en_years, bull, bear, products)
    
    plt.close('all')
    rcParams['figure.figsize'] = 12, 5  # fig size by prgrammer choice  
    
    fig, ax = plt.subplots()
    index = np.arange(27)
    bar_width = .30
    opacity = 0.8
     
    plt.bar(index, bull_, bar_width,
                     alpha=opacity,
                     color='g',
                     label='Bullish En.')
     
    plt.bar(index + bar_width, bear_, bar_width,
                     alpha=opacity,
                     color='r',
                     label='Bearish En.')
    
    plt.bar(index + bar_width + bar_width, products_, bar_width,
                     alpha=opacity,
                     color='b',
                     label='Product Release')
     
    plt.xlabel('Years')
    plt.ylabel('Occrances')
    plt.title('Engulfing VS. Product Release.')
    plt.xticks(index + bar_width, en_years_)
    plt.legend()
     
    plt.tight_layout()
    plt.savefig('barPlot.png')
    plt.show()


def save_result_as_csv(a_bu, a_uval_bu, a_br, a_uval_br, m_bu, m_uval_bu, m_br, m_uval_br, 
                   years, products,a_bullishDates, a_bearishDates, m_bullishDates, m_bearishDates ):
    
    with open('output.csv', 'w') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(["Year", "Total Apple Bullish En. Per-Year", "Year", "Total Apple Bearish En. Per-Year", "Year", # title of each row
                         "Total Microsoft Bullish En. Per-Year", "Year", "Total Microsoft Bearish En. Per-Year",
                         "Apple Porduct Year", "Apple Product Released Per-Year", "Bullish Engulfing Dates (Apple)",
                         "Bearish Engulfing Dated (Apple)", "Bullish Engulfing Dates (Microsoft)", 
                         "Bearish Engulfing Dates (Microsoft)"])
        for row in zip_longest(a_bu, a_uval_bu, a_br, a_uval_br, m_bu, m_uval_bu, m_br, m_uval_br, 
                   years, products,a_bullishDates, a_bearishDates, m_bullishDates, m_bearishDates): # writing to csv with longest list index
            writer.writerow(row)
    

    outcsv.close()    


########################******** END of PLOTTING *********##################################    

        
#PASS CSV and Call HTML and other methods to get the disaired output and images
print("\n"*30)
data1 = 'aapl_large.csv'
data2 = 'msft_large.csv'
data3 = 'test.csv'


a_bu, a_uval_bu, a_br, a_uval_br, close,bull_index, bear_index, a_bullishDates, a_bearishDates = csv_data(data1)
m_bu, m_uval_bu, m_br, m_uval_br, close,bull_index, bear_index, m_bullishDates, m_bearishDates = csv_data(data2)
years, products = HTML_file()

print("\n"*30)
print("\n","-"*20," RESULTS ","-"*20,"\n") # Apple results
print("Apple Inc. Results (CSV):\n", "Years: ", a_bu, "\nBullish Engulfing: ",
      a_uval_bu, "\nBeraish Engulfings: ", a_uval_br, "\nTotal Bullish Engulfings: ",
      sum(a_uval_bu), "\nTotal Bearish Engulfings: ", sum(a_uval_br))

print("\n","-"*20,"*"*10,"-"*20,"\n") # Microsoft results
print("Microsoft Corp. Results (CSV):\n", "Years: ",m_bu, "\nBullish Engulfings: ",
      m_uval_bu,"\nBeraish Engulfings: ", m_uval_br, "\nTotal Bullish Engulfings: ",
      sum(m_uval_bu), "\nTotal Bearish Engulfings: ", sum(m_uval_br))

print("\n","-"*20,"*"*10,"-"*20,"\n") # HTML results
print("Apple Inc. Product Results (HTML):\n", "Years: ", years, "\nReleases: ", products,
       "\n Total Amount of Product: ", sum(products))

print("\n","-"*20,"*"*10,"-"*20,"\n")
print("Bullish Engulfing Dates (Apple): ", a_bullishDates, "\nBearish Engulfing Dates (Apple): " , a_bearishDates )
print("Bullish Engulfing Dates (Microsoft): ", a_bullishDates, "\nBearish Engulfing Dates (Microsoft): " , a_bearishDates )

# plotting and saving data as csv by calling each created methods above
plots(a_bu, a_uval_bu, a_br, a_uval_br, m_bu, m_uval_bu, m_br, m_uval_br) 
Scatter_plot(years, products)
bar_plot(years, a_bu, a_uval_bu, a_uval_br, products)
save_result_as_csv(a_bu, a_uval_bu, a_br, a_uval_br, m_bu, m_uval_bu, m_br, m_uval_br, 
                   years, products,a_bullishDates, a_bearishDates, m_bullishDates, m_bearishDates )


print("---Execuation Time: %.4s seconds ---" % (time.time() - start_time)) # print execuation time

#END#
