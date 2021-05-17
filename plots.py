import csv 
import dionysus as d 
import numpy as np
import matplotlib.pyplot as plt 

# Convert string value to float. Return 0 if value is empty
def string_to_float(value):
    value.strip()
    if value == "":
        return 0
    else:
        return float(value)


mintemps = []
maxtemps = [] 
maxtemp_avgs = [] 
mintemp_avgs = [] 
maxtemp_avgs_annual={0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []} 
precipitation = [] 
snow = [] 
with open('tahoe_city.csv', newline='') as csvfile: 
    #Use DictReader so list doesn't contain header row 
    climatereader = csv.DictReader(csvfile)
    # Loop through each row in the file, also getting the index
    year = 1903
    month = 9
    monthly_max_temps = [] 
    yearly_max_temps = [] 
    yearly_min_temps = [] 
    yearly_precipitation = []
    yearly_snow = [] 
    day = 0 
    for row in climatereader:
        row_month = row['DATE'].strip().split('-')[1]
        row_year = row['DATE'].strip().split('-')[0]

        if int(row_month) != month: 
            month = int(row_month)
            valid_month = True
            if(len(monthly_max_temps) < 27): 
                #Disregard month, not enough points to avg
                valid_month = False

            if valid_month: 
                max_avg = sum(monthly_max_temps)/len(monthly_max_temps)
                maxtemp_avgs_annual[int(row_month)].append(max_avg)

            monthly_max_temps = [] 

        if int(row_year) > year: 
            year += 1
            #If any of the dimesnions are empty, do not avg year
            #Ignore all these
            #1904, 1905, 1906, 1907 has no min and max temps
            #1908, 1909 has 1 temp 
            #1910 has 164 temps 
            valid_year = True
            cloud = {0: yearly_max_temps, 1: yearly_min_temps, 2: yearly_precipitation, 3: yearly_snow}
            for key, dimension in cloud.items(): 
                if len(dimension) < 360: 
                    valid_year = False 
                    break 

            if valid_year: 
                maxtemps.append(yearly_max_temps)
                mintemps.append(yearly_min_temps)
                max_avg = sum(yearly_max_temps)/len(yearly_max_temps)
                min_avg = sum(yearly_min_temps)/len(yearly_min_temps)
                rain_total = sum(yearly_precipitation)
                snow_total = sum(yearly_snow)/12
                maxtemp_avgs.append(max_avg)
                mintemp_avgs.append(min_avg)
                precipitation.append(rain_total)
                snow.append(snow_total)

            yearly_max_temps = [] 
            yearly_min_temps = [] 
            yearly_precipitation = [] 
            yearly_snow = [] 

        if row['TMAX'] != "": 
            monthly_max_temps.append(int(row['TMAX']))
            yearly_max_temps.append(int(row['TMAX']))
        if row['TMIN'] != "": 
            yearly_min_temps.append(int(row['TMIN']))
        yearly_precipitation.append(string_to_float(row['PRCP']))
        yearly_snow.append(string_to_float(row['SNOW']))

#Total Rainfall
fig, axes = plt.subplots(2, figsize=(20,10))
axes[0].plot([i+1903 for i in range(len(precipitation))], precipitation)
axes[0].set_ylabel('Rain fall (in)')
axes[0].set_xlabel('Year')
axes[0].set_title('Total Percipitation per year')

#Min and Max temps plot graph 
axes[1].plot([i+1903 for i in range(len(maxtemp_avgs))], maxtemp_avgs, color='red', label='max temps')# linewidth=1)
axes[1].plot([i+1903 for i in range(len(mintemp_avgs))], mintemp_avgs, color='blue', label='min temps')# linewidth=1)
axes[1].set_ylabel('Tmp (F)')
axes[1].set_xlabel('Year')
axes[1].set_title('Avg Daily Min and Max Tmps')
axes[1].legend()
plt.show()

#Example of sinsoildal shape for temperatures
maxtemp_span = []
for year in range(1950-1910, 1956-1910): 
    for day in maxtemps[year]: 
        maxtemp_span.append(day)
fig, ax = plt.subplots(figsize=(20,10))
days = [i for i, day in enumerate(maxtemp_span)]
ax.scatter(days, maxtemp_span, color='red')
xtick_labels = [str(year) for year in range(1950, 1955+1)]
ax.set_xticklabels(xtick_labels)
ax.set_ylabel('Temperature Farenheight')
ax.set_xlabel('Year')
ax.set_title('Maximum Temperatures 1950-1955')
#plt.show()

#Monthly Temperatures
fig, ax = plt.subplots(figsize=(20,10))
#Code for all 12 months 
#for month, values in maxtemp_avgs_annual.items(): 
#    ax.scatter([month for i in range(len(values))], values, color='red')
monthly_year_avgs = maxtemp_avgs_annual[11]
ax.plot([year+1903 for year in range(len(monthly_year_avgs))], monthly_year_avgs, color='red')
ax.set_xlabel('Month')
ax.set_ylabel('Maximum Temperatures (F)')
ax.set_title('Monthly Avg Max Temps')

#The point cloud 
fig, ax = plt.subplots(figsize=(20,10))
maxtemp_years = [day for day in range(len(maxtemp_avgs))]
mintemp_years = [day for day in range(len(mintemp_avgs))]
precipitation_years = [day for day in range(len(precipitation))]
snow_years = [day for day in range(len(snow))]
ax.scatter(maxtemp_years, maxtemp_avgs, color='red', label='max temps')
ax.scatter(mintemp_years, mintemp_avgs, color='blue', label='min temps')
ax.scatter(precipitation_years, precipitation, color='green', label='rain')
ax.scatter(snow_years, snow, color='orange', label='snow')
ax.set_xlabel('Year')
ax.set_ylabel('temperatures (F), rain (inches), snow (feet)')
ax.set_title('Point Cloud')
num_years = 2021-1903
num_ticks = 6
tick_distance = int(num_years/num_ticks)
xtick_labels = [1903+(x*tick_distance) for x in range(0, num_ticks+1)]#, 1903+tick_distance, 1903+2*tick_distance] 
ax.set_xticklabels(xtick_labels)
ax.legend()
plt.show()
