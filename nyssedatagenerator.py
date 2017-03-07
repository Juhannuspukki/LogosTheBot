import json
one = {}

stoptimes = []
c = open("stop_times.txt", "r", encoding="utf-8")
for line in c:
    stoptimes.append(line)

for i in range(1, len(stoptimes), 1):
    tripinfo = stoptimes[i]  # of form 4917824002,09:29:00,09:29:00,4011,17,0
    keyone = tripinfo.split(",")[0]  # of form 4917824002
    if keyone not in one.keys():
        one[keyone] = []
    stopinfo = {"stopid": tripinfo.split(",")[3], "departtime": tripinfo.split(",")[2]}
    one[keyone].append(stopinfo)

with open('exec.json', 'w') as file:
    json.dump(one, file, sort_keys=True, indent=4, separators=(',', ': '))
