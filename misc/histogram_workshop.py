"""
Exercise 1: Download the file salary.txt and read it into an
array called x. Create an array, y, of the same length with all the
entries set to 1. Make a scatter plot of x against y and give each
point a low transparency (alpha) value.
"""
import numpy as np
import matplotlib.pyplot as plt

with open("salary.txt", 'r') as infile:
    x = np.array([float(s) for s in infile.readlines()])

"""
Exercise 1: Download the file salary.txt and read it into an
array called x. Create an array, y, of the same length with all the
entries set to 1. Make a scatter plot of x against y and give each
point a low transparency (alpha) value.
"""
# y = np.ones(np.shape(x))
#
# fig, ax = plt.subplots()
#
# ax.scatter(x, y, alpha=0.1)
#
# fig.savefig('ex_1')
# plt.close()

"""
Exercise 2 onwards
Exercise 4: Produce the plot above. Look at the documenta-
tion for label and legend. Restrict the range of the x-axis to only
show salaries between £0 and £100000 and put the legend in a diffferent place.
Exercise 5: Minimum wage laws make an annual salary of less
than £5000 per year unlikely. Using bins of size 500, plot the his-
togram in the range 0 to 10000. What do you think is going on? 6 jobs < 5000 -
maybe part-time jobs???
Exercise 6: Use the cumulative frequency distribution to esti-
mate (you don’t have to be exact) the 1% salary i.e. the amount
of money you have to earn per year so that you make more than
99% of people.
"""

fig, ax = plt.subplots()

# plt.hist(x, bins=500, label="Salaries")
plt.hist(x, bins=500, cumulative=True, histtype='step', density=True)
plt.xlabel("GBP")
plt.ylabel("Number of Jobs")
ax.set_xlim(0, 100000)
# ax.set_ylim(0, 20)

plt.legend(loc='upper center', bbox_to_anchor=(1.15, 0.9))
# Shrink current axis by 10%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.title("Histogram of Salary Data")
fig.savefig('salary_histogram.png')
plt.close()

print('Finished')
