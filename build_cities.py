import json

cities = []

with open("cities500.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split("\t")

        try:
            name = parts[1]
            lat = float(parts[4])
            lng = float(parts[5])
            population = int(parts[14])

            cities.append({
                "name": name,
                "lat": lat,
                "lng": lng,
                "pop": population
            })

        except:
            continue

with open("cities.js", "w", encoding="utf-8") as out:
    out.write("const citiesData = ")
    json.dump(cities, out)
    out.write(";")

print(f"Generated {len(cities)} cities")

