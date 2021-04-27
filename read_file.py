import csv 
import dionysus as d 

dailytemps = [] 
maxtemps = [] 
mintemps = [] 
with open('tahoe_city.csv', newline='') as csvfile: 
    #Use DictReader so list doesn't contain header row 
    climatereader = csv.DictReader(csvfile)
    for row in climatereader: 
        dailytemps.append((row["TMIN"], row["TMIN"])) 
        maxtemps.append(row['TMAX'])
        mintemps.append((row['TMIN']))


print('daily_temp Maxtemp and mintemps len: ', len(dailytemps), len(maxtemps), len(mintemps))
