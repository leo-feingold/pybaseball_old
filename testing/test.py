from pybaseball import playerid_lookup
from pybaseball import statcast_pitcher
playerid_lookup('kershaw', 'clayton')

kershaw_stats = statcast_pitcher('2023-06-01', '2023-07-01', 477132)
print(kershaw_stats.head(2))

