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



########## Homology Stuff ###########


point_cloud = np.vstack((yearly_mintemps,yearly_maxtemps)).T

# Call fill_rips to compute the rips filtrations. 5 is the number of dimensions,
# 8 is the radius of the balls. It's an arbitrary value
f = d.fill_rips(point_cloud, 5, 0.5)

# Plot the diagram and barcodes from the vietoris-rips filtrations above. This
# code is pretty much straight ripped from dionysus documentation
p = d.homology_persistence(f)
dgms = d.init_diagrams(p,f)
d.plot.plot_diagram(dgms[1], show=True)
d.plot.plot_bars(dgms[1],show=True)


######################################

### All the code below is for animation ###

fig = plt.figure(figsize=(8,8))
ax = plt.subplot(aspect='equal')
# Plot the static points, no need to animate anything
plt.scatter(yearly_mintemps,yearly_maxtemps, s=10)
ax.set_xlim(26,34)
ax.set_ylim(51,61)
txt = plt.text(26,60,'Radius:', fontsize=10)

# Create a circle array to make the orange circles
circles = []
for min_t, max_t in zip(yearly_mintemps,yearly_maxtemps):
    circle = plt.Circle((min_t,max_t),0.3,alpha=0.2,color='orange')
    ax.add_patch(circle)
    circles.append(circle)


# The main function that is called on each frame of the animation. The only goal
# of the function is to update the radius of the circles in the scatter plot
def update(frame_number):
    for circle in circles:
        circle.set_radius(frame_number*0.005)
    txt.set_text('Radius: {}'.format(frame_number*0.005))

# start animation
animation = FuncAnimation(fig, update, frames = 200,interval=20)
plt.show()
