from SuperSaaS import Client
from datetime import datetime
import utils
import Tkinter as tk
import matplotlib.pyplot as plt
from tkcalendar import Calendar
import pandas


api_filename = "API_KEY"
Client.instance().configure(
    account_name = "Reservations",
    api_key = utils.get_file_contents(api_filename)
)

while 1:
    user_date = raw_input("Enter date with the format mm-dd-yyyy:\t")
    try:
        starting_date = datetime.strptime(user_date, '%m-%d-%Y')
        break
    except ValueError as e:
        print(e)
ll = Client.instance().appointments.list(schedule_id=289549, start_time=starting_date)
reds = {}
blues = {}
greens = {}
yellows = {}

i = 0
for l in ll:
    i += 1
    name = l.res_name.split()[0]
    stop = datetime.strptime(l.finish, '%Y-%m-%dT%H:%M')
    start= datetime.strptime(l.start, '%Y-%m-%dT%H:%M')
    date = utils.get_date_str(stop)

    if date not in reds or date not in blues or date not in greens or date not in yellows:
        reds[date] = pandas.Timedelta(0)
        greens[date] = pandas.Timedelta(0)
        blues[date] = pandas.Timedelta(0)
        yellows[date] = pandas.Timedelta(0)

    if name  == "Red":
        # red laser cutter
        reds[date] += stop - start
    elif name == "Blue":
        # blue laser cutter
        blues[date] += stop - start
    elif name == "Green":
        # green laser cutter
        greens[date] += stop - start
    elif name == "Yellow":
        # yellow laser cutter
        yellows[date] += stop - start
print(i)

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


x = range(0, max(len(red_values), len(blue_values), len(yellow_values), len(green_values)))
plt.plot(x, red_values, 'r')
plt.plot(x, yellow_values, 'y')
plt.plot(x, blue_values, 'b')
plt.plot(x, green_values, 'g')
ax = plt.axes()
ax.xaxis.set_major_locator(plt.MultipleLocator(base=7.0))
ax.xaxis.set_minor_locator(plt.MultipleLocator(base=1.0))
ax.xaxis.set_major_formatter(plt.NullFormatter())

plt.show()

