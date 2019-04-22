import time
def get_date_str(timestamp):
    return time.strftime("%Y-%m-%d", timestamp)

def get_file_contents(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoudnError:
        print("'%s' file not found" % filename)

