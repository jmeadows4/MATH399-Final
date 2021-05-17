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
    average_max = 0
    average_min = 0
    # keep track of number of dates in year to take average
    num_dates_in_year = 0

    for i,row in enumerate(climatereader):
        if row['TMIN'] != "" and row['TMAX'] != "":
            # Another date counted for the current year
            num_dates_in_year += 1
            average_min += string_to_float(row['TMIN'])
            average_max += string_to_float(row['TMAX'])

            # Get the year of the current row we are on. Date format is 
            # YYYY-MM-DD, so we split by "-" and get the 0th element(the year)
            row_year = row['DATE'].split("-")[0]
            # If we are starting a new year
            if row_year != cur_year :
                cur_year = row_year
                yearly_maxtemps.append(average_max / num_dates_in_year)
                yearly_mintemps.append(average_min / num_dates_in_year)
                num_dates_in_year = 0
                average_min = 0
                average_max = 0


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

# Call fill_rips to compute the rips filtrations. 3 is the number of dimensions,
# 2 is the maximum radius of the balls.
f = d.fill_rips(point_cloud, 3, 2)

# Plot the diagram and barcodes from the vietoris-rips filtrations above. This
# code is pretty much straight ripped from dionysus documentation
p = d.homology_persistence(f)
dgms = d.init_diagrams(p,f)
d.plot.plot_diagram(dgms[1], show=True)
d.plot.plot_bars(dgms[1],show=True)


######################################

### All the code below is for the rips animation ###

fig = plt.figure(figsize=(8,8))
ax = plt.subplot(aspect='equal')
ax.set_xlim(25,35)
ax.set_ylim(51,62)

# Create a circle array to make the orange circles
circles = []
for min_t, max_t in zip(yearly_mintemps,yearly_maxtemps):
    circle = plt.Circle((min_t,max_t),0.3,alpha=0.2,color='orange')
    ax.add_patch(circle)
    circles.append(circle)

txt = plt.text(26,60,'Radius:', fontsize=10)
plt.scatter(yearly_mintemps,yearly_maxtemps, s=10)
    
lines_plotted = []
line_objects = []

# The main function that is called on each frame of the animation. The only goal
# of the function is to update the radius of the circles in the scatter plot
def update(frame_number):
    radius_size = frame_number*0.005
    for circle in circles:
        circle.set_radius(radius_size)
    txt.set_text('Radius: {:.2f}'.format(radius_size))
    for x1,y1,circle1 in zip(yearly_mintemps,yearly_maxtemps,circles):
        for x2,y2,circle2 in zip(yearly_mintemps,yearly_maxtemps,circles):
            if circle1 is not circle2 and \
               np.sqrt(np.abs(x1-x2)**2+np.abs(y1-y2)**2) < radius_size*2:

                if [(x1,x2),(y1,y2)] not in lines_plotted:
                    lines_plotted.append([(x1,x2),(y1,y2)])
                    line_objects.append(plt.plot([x1,x2],[y1,y2],'m'))
    if num_frames == frame_number+1:
        for line_obj in line_objects:
            line=line_obj.pop(0)
            line.remove()
        lines_plotted.clear()
        line_objects.clear()
    
# start animation
num_frames=200
animation = FuncAnimation(fig, update, frames = num_frames,interval=20)
plt.show()
