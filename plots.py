import csv 
import dionysus as d 
import numpy as np
import matplotlib.pyplot as plt 

# Convert string value to float. Return 0 if value is empty
def string_to_float(value):
    if value == "":
        return 0
    else:
        return float(value)

precipitation = [] 
mintemps = []
maxtemps = [] 
with open('tahoe_city.csv', newline='') as csvfile: 
    #Use DictReader so list doesn't contain header row 
    climatereader = csv.DictReader(csvfile)
    # Loop through each row in the file, also getting the index
    year = 1903
    month = 9
    yearly_max_temps = [] 
    yearly_min_temps = [] 
    yearly_precipitation = []
    for i,row in enumerate(climatereader):
        row_month = row['DATE'].strip().split('-')[1]
        row_year = row['DATE'].strip().split('-')[0]
        if int(row_month) != month: 
            month = int(row_month)
        if int(row_year) > year: 
            if(len(yearly_precipitation) > 300): 
                precipitation.append(sum(yearly_precipitation))
            if(len(yearly_max_temps) > 300): 
                maxtemps.append(sum(yearly_max_temps)/len(yearly_max_temps))
            if len(yearly_min_temps) > 300: 
                mintemps.append(sum(yearly_min_temps)/len(yearly_min_temps))
            yearly_precipitation = [] 
            yearly_max_temps = [] 
            yearly_min_temps = [] 
            year += 1

        yearly_max_temps.append(string_to_float(row['TMAX']))
        yearly_min_temps.append(string_to_float(row['TMIN']))
        yearly_precipitation.append(string_to_float(row['PRCP']))

            
plt.figure(figsize=(20,10))

plt.subplot(2, 1, 1)
plt.plot([i+1903 for i in range(len(precipitation))], precipitation)
plt.ylabel('Rain fall (in)')
plt.xlabel('Year')
plt.title('Total Percipitation per year')

plt.subplot(2, 1, 2)
plt.plot([i+1903 for i in range(len(maxtemps))], maxtemps, color='red', label='max temps')# linewidth=1)
plt.plot([i+1903 for i in range(len(maxtemps))], mintemps, color='blue', label='min temps')# linewidth=1)
plt.ylabel('Tmp (F)')
plt.xlabel('Year')
plt.title('Avg Daily Min and Max Tmps')
plt.legend()
plt.show()

