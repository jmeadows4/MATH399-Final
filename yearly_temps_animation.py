import csv 
import dionysus as d 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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


# First, a static plot of the points
plt.xlabel("Minimum temp(Fahrenheit)")
plt.ylabel("Maxmimum temp(Fahrenheit)")
plt.scatter(yearly_mintemps,yearly_maxtemps, s=20)
plt.title("Average yearly max and min temperatures in Tahoe")
plt.ylim(51, 61)
plt.xlim(26, 34)
plt.show()


### All the code below is for animation ###

fig = plt.figure()
ax = plt.axes()
# Plot the static points, no need to animate anything
plt.scatter(yearly_mintemps,yearly_maxtemps, s=10)
ax.set_xlim(26,34)
ax.set_ylim(51,61)
# Create a scatter object, which we will update. The orange circles are actually
# just scattered points with low alpha value and increasing size
scat = ax.scatter(yearly_mintemps, yearly_maxtemps, s=10, alpha=0.3)

# Create an array of radius sizes. This is the format that the set_sizes function
# below expects
radius_sizes = len(yearly_mintemps) * [10]

# The main function that is called on each frame of the animation. The only goal
# of the function is to update the radius of the balls in the scatter plot
def update(frame_number):
    for i in range(len(radius_sizes)):
        radius_sizes[i] = 5*frame_number+10
    scat.set_sizes(radius_sizes)

# start animation
animation = FuncAnimation(fig, update, frames = 500,interval=10)
plt.show()
