import re
from datetime import datetime

def create_log(data,filename):
    f = open(f"modules/logger/{filename}.txt", "a")
    f.write("{0} -- {1}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M"), data))
    f.close()


def log_control(query, filename):
    logData = []

    with open(f'modules/logger/{filename}.txt', 'r') as file:
        for f in file.readlines():
            logData.append(f.strip())
    

    find = str(logData).find(str(query))
    
    if find > 0:
        return True
    else:
        return False