import pandas as pd
from datetime import datetime

df = pd.read_csv('incidents.csv')

arr = []
for a in list(df['Reported']):
    t1 = datetime.strptime(a.split(' ')[1], '%H:%M')
    if t1 >= datetime.strptime('06:00', '%H:%M') and t1 < datetime.strptime('12:00', '%H:%M'):
        arr.append("Morning")
    
    elif t1 >= datetime.strptime('12:00', '%H:%M') and t1 < datetime.strptime('18:00', '%H:%M'):
        arr.append("Afternoon")
    
    elif t1 >= datetime.strptime('18:00', '%H:%M') and t1 <= datetime.strptime('23:59', '%H:%M'):
        arr.append("Night")

    else:
        arr.append("Late Night")

df['Times'] = arr

df.to_csv('incidents.csv')