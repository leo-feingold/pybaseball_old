from pybaseball import statcast
data = statcast(start_dt='2017-06-24', end_dt='2017-06-27')
print(data.head(2))