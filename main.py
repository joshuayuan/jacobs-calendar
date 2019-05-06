from SuperSaaS import Client
import datetime as dt
import utils
import Tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from tkcalendar import Calendar
import pandas

weekday_string = {0: "Mon", 1: "Tues", 2: "Wed", 3: "Thurs", 4: "Fri", 5: "Sat", 6: "Sun"}

api_filename = "API_KEY"
Client.instance().configure(
    account_name = "Reservations",
    api_key = utils.get_file_contents(api_filename)
)

while 1:
    user_date = raw_input("Enter date with the format mm-dd-yyyy:\t")
    try:
        starting_date = dt.datetime.strptime(user_date, '%m-%d-%Y')
        break
    except ValueError as e:
        print(e)
ll = Client.instance().appointments.list(schedule_id=289549, start_time=starting_date)
#I think this only gets 2500 appointments max though.

reds = {}
blues = {}
greens = {}
yellows = {}

# number_of_hours_open * 60 * 60 = total seconds
# M-F are 14 hours, Sat is 6.5 hours, Sunday is 3.5 hours.
day_to_seconds = {0: 50400.0, 1: 50400.0, 2: 50400.0, 3: 50400.0, 4: 50400.0, 5: 23400.0, 6: 12600.0} # 0 is Monday 6 is Sunday


i = 0
for l in ll:
    i += 1
    name = l.res_name.split()[0]
    stop = dt.datetime.strptime(l.finish, '%Y-%m-%dT%H:%M')
    start = dt.datetime.strptime(l.start, '%Y-%m-%dT%H:%M')
    day_of_week = stop.weekday()

    date_str = stop.strftime("%Y-%m-%d")# utils.get_date_str(stop)

    if date_str not in reds or date_str not in blues or date_str not in greens or date_str not in yellows:
        print(date_str)
        reds[date_str] = pandas.Timedelta(0)
        greens[date_str] = pandas.Timedelta(0)
        blues[date_str] = pandas.Timedelta(0)
        yellows[date_str] = pandas.Timedelta(0)

    if name  == "Red":
        # red laser cutter
        reds[date_str] += (stop - start) #/ dt.timedelta(seconds=date_to_seconds[day_of_week])
    elif name == "Blue":
        # blue laser cutter
        blues[date_str] += (stop - start)
    elif name == "Green":
        # green laser cutter
        greens[date_str] += (stop - start)
    elif name == "Yellow":
        # yellow laser cutter
        yellows[date_str] += (stop - start)
# print(i)

red_keys = []
red_values = []
for key in sorted(reds.keys()):
    red_keys.append(key)
    red_values.append(reds[key].seconds / day_to_seconds[dt.datetime.strptime(key, "%Y-%m-%d").weekday()])
# print(reds)
blue_keys= []
blue_values = []
for key in sorted(reds.keys()):
    blue_keys.append(key)
    blue_values.append(blues[key].seconds / day_to_seconds[dt.datetime.strptime(key, "%Y-%m-%d").weekday()])

yellow_keys = []
yellow_values = []
for key in sorted(reds.keys()):
    yellow_keys.append(key)
    yellow_values.append(yellows[key].seconds / day_to_seconds[dt.datetime.strptime(key, "%Y-%m-%d").weekday()])

green_keys = []
green_values = []
for key in sorted(reds.keys()):
    green_keys.append(key)
    green_values.append(greens[key].seconds / day_to_seconds[dt.datetime.strptime(key, "%Y-%m-%d").weekday()])


data = range(0, max(len(red_values), len(blue_values), len(yellow_values), len(green_values)))
plt.plot(data, red_values, 'r')
plt.plot(data, yellow_values, 'y')
plt.plot(data, blue_values, 'b')
plt.plot(data, green_values, 'g')
ax = plt.axes()
ax.grid()
ax.xaxis.set_major_locator(plt.MultipleLocator(base=7.0))
ax.xaxis.set_minor_locator(plt.MultipleLocator(base=1.0))
ax.set_xticklabels(["Day: ", weekday_string[starting_date.weekday()]])

plt.show()

