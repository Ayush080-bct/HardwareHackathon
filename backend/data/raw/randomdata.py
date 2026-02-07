import random, csv

rows = []

for t in range(2000):              
    hour = t % 24
    peak = hour in [6,7,8,18,19,20,21]

    for house_id in range(1, 6):   
        current = round(
            random.uniform(0.5, 5 if peak else 2.5),
            2
        )

        rows.append([t, hour, house_id, current])

with open("./power_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "timestamp",
        "hour",
        "house_id",
        "current"
    ])
    writer.writerows(rows)

print("✅ Raw sensor-style dataset created: data/raw/raw_currents.csv")
