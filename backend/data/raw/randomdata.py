import random, csv

rows = []
prev_total = 10

for t in range(2000):
    hour = random.randint(0,23)
    peak = 1 if hour in [6,7,8,18,19,20,21] else 0
    
    houses = [round(random.uniform(0.5,5 if peak else 2.5),2) for _ in range(5)]
    total = round(sum(houses),2)
    
    change = round(total - prev_total,2)
    prev_total = total
    
    overload = 1 if total > 18 else 0
    contributor = houses.index(max(houses)) + 1
    
    rows.append([t,hour,peak,*houses,total,change,overload,contributor])

with open("power_data.csv","w",newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp","hour","is_peak_hour",
                     "house1_current","house2_current","house3_current","house4_current","house5_current",
                     "total_current","current_change_rate",
                     "overload_flag","main_contributor"])
    writer.writerows(rows)
