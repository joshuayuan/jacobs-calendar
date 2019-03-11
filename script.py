import pandas
import utils
import matplotlib.pyplot as plt

df = pandas.read_csv('3-1-19_3-10-19.csv', parse_dates=['Start time', 'Finish time'], usecols=[0, 1, 2]) 

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

keys = []
values = []
for key in sorted(reds.keys()):
    keys.append(key)
    values.append(reds[key].seconds)

print(keys)
print(values)
x = range(0,10)
plt.plot(x, values)
plt.xticks(x, keys)

plt.show()

