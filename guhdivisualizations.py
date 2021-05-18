
import csv 
import numpy as np
import gudhi
import matplotlib.pyplot as plt 
from ripser import ripser
from persim import plot_diagrams

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
cur_year=""
yearly_maxtemps = []
yearly_mintemps = []

with open('tahoe_city.csv', newline='') as csvfile: 
    #Use DictReader so list doesn't contain header row 
    climatereader = csv.DictReader(csvfile)
    average_yearly_max = 0 
    average_yearly_min = 0
    # keep track of number of dates in year to take average
    num_dates_in_year = 0

    # I'm sure there's a cleaner way to get the average, but this works for now
    for i,row in enumerate(climatereader):
        if row['TMIN'] != "" and row['TMAX'] != "":
            # Another date counted for the current year
            num_dates_in_year += 1  
            average_yearly_min += string_to_float(row['TMIN'])
            average_yearly_max += string_to_float(row['TMAX'])
        
            # Get the year of the current row we are on. Date format is 
            # YYYY-MM-DD, so we split by "-" and get the 0th element(the year)
            row_year = row['DATE'].split("-")[0]
            # If we are starting a new year
            if row_year != cur_year :
                cur_year = row_year
                yearly_maxtemps.append(average_yearly_max / num_dates_in_year)
                yearly_mintemps.append(average_yearly_min / num_dates_in_year)
                num_dates_in_year = 0
                average_yearly_min = 0
                average_yearly_max = 0

            

point_cloud = np.vstack((yearly_mintemps, yearly_maxtemps)).T
rips_complex = gudhi.RipsComplex(points=point_cloud, max_edge_length=7)
simplex_tree = rips_complex.create_simplex_tree(max_dimension=3)
diag = simplex_tree.persistence(min_persistence=0.4)

gudhi.plot_persistence_barcode(diag)

plt.show()

