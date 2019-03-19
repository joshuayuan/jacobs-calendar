import pandas
import utils
import matplotlib.pyplot as plt

# df = pandas.read_csv('data/1-1-19_3-18-19.csv', parse_dates=['Start time', 'Finish time'], usecols=[0, 1, 2])
df = pandas.read_csv('data/3-1-19_3-10-19.csv', parse_dates=['Start time', 'Finish time'], usecols=[0, 1, 2]) 

# Only look at cutter, and respective start/stop times
df.columns = ["Cutter", "Start", "Stop"] 

# Remap cutter names to be more simple
df["Cutter"] = df["Cutter"].map({"Red laser cutter 48x24 in": "Red", "Blue laser cutter 32x18 in": "Blue", "Yellow laser cutter 32x18 in": "Yellow", "Green laser cutter 32x18 in": "Green"})

# group by cutters, then by start times within each cutter grouping
df = df.sort_values(by=["Cutter", "Start"]) 

# create dictionaries. Consider using default dicts later
# {string date: pandas.Timedelta total_time} 
reds = {}
blues = {}
greens = {}
yellows = {}

for index, cutter, start, stop in df.itertuples():
    print(start.day_name())
    date = utils.get_date_str(start)
    # Initialize dictionary with default time deltas of 0
    if date not in reds or date not in blues or date not in greens or date not in yellows:
        reds[date] = pandas.Timedelta(0)
        blues[date] = pandas.Timedelta(0)
        greens[date] = pandas.Timedelta(0)
        yellows[date] = pandas.Timedelta(0)

    # add time deltas to the respective dicts
    if cutter == "Red":
        reds[date] += stop - start
    elif cutter == "Blue":
        blues[date] += stop - start
    elif cutter == "Green":
        greens[date] += stop - start
    elif cutter == "Yellow":
        yellows[date] += stop - start

# In the future do something with matrix calculations.

red_keys = []
red_values = []
for key in sorted(reds.keys()):
    red_keys.append(key)
    red_values.append(reds[key].seconds)
blue_keys= []
blue_values = []
for key in sorted(reds.keys()):
    blue_keys.append(key)
    blue_values.append(blues[key].seconds)

yellow_keys = []
yellow_values = []
for key in sorted(reds.keys()):
    yellow_keys.append(key)
    yellow_values.append(yellows[key].seconds)

green_keys = []
green_values = []
for key in sorted(reds.keys()):
    green_keys.append(key)
    green_values.append(greens[key].seconds)


x = range(0, len(red_values))
plt.plot(x, red_values, 'r')
plt.plot(x, yellow_values, 'y')
plt.plot(x, blue_values, 'b')
plt.plot(x, green_values, 'g')
plt.xticks(x, red_keys)

plt.show()

