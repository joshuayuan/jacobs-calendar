def get_date_str(timestamp):
    return str(timestamp.month) + "-" + str(timestamp.day) + "-" + str(timestamp.year)
def get_file_contents(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoudnError:
        print("'%s' file not found" % filename)

