import csv 
import dionysus as d 
import numpy as np

# Convert string value to float. Return 0 if value is empty
def string_to_float(value):
    if value == "":
        return 0
    else:
        return float(value)

dailytemps = [] 
maxtemps = [] 
mintemps = [] 
snow = []
snowdepth = []
precipitation = []
with open('tahoe_city.csv', newline='') as csvfile: 
    #Use DictReader so list doesn't contain header row 
    climatereader = csv.DictReader(csvfile)
    # Loop through each row in the file, also getting the index
    for i,row in enumerate(climatereader):
        # Right now, trying to use all the data stalls the program when the
        # fill_rips function is called. So right now we are only considering
        # 100 points in an arbitrarily chosen range. Can definitely mess with this
        if i >= 2000 and i <2100:
            # Get the number of empty values for a row
            num_empty_data = 0
            if row['TMIN'] == "":
                num_empty_data += 1
            if row['TMAX'] == "":
                num_empty_data += 1
            if row['SNOW'] == "":
                num_empty_data += 1
            if row['SNWD'] == "":
                num_empty_data += 1
            if row['PRCP'] == "":
                num_empty_data += 1
            # Only append if there are 3 or more values in the row
            if num_empty_data < 3:
                mintemps.append(string_to_float(row['TMIN']))
                maxtemps.append(string_to_float(row['TMAX']))
                snow.append(string_to_float(row['SNOW']))
                snowdepth.append(string_to_float(row['SNWD']))
                precipitation.append(string_to_float(row['PRCP']))
                dailytemps.append((string_to_float(row['TMIN']),
                                   string_to_float(row['TMAX'])))


print('daily_temp Maxtemp and mintemps len: ', len(dailytemps), len(maxtemps), len(mintemps))

# Turn the 5 one-dimensional arrays into one 5-dimensional array. This is the shape
# that fill_rips expects(I think).
point_cloud = np.vstack((mintemps,maxtemps,snow,snowdepth,precipitation)).T
print(point_cloud.shape)

# Call fill_rips to compute the rips filtrations. 5 is the number of dimensions,
# .3 is the radius of the balls. It's an arbitrary value
f = d.fill_rips(point_cloud, 5, .3)
print(f)
# Not really sure what this is printing
for s in f:
    print(s)
