from SuperSaaS import Client
from datetime import datetime
import utils
import tkinter as tk
from tkcalendar import Calendar


api_filename = "API_KEY"
Client.instance().configure(
    account_name = "Reservations",
    api_key = utils.get_file_contents(api_filename)
)



ll = Client.instance().appointments.list(schedule_id=289549, start_time=datetime.now(), limit=5)
print(ll)
for l in ll:
    print(l.start, l.finish, l.res_name)

