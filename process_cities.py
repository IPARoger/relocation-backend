import json
import sys

with open("cities5000.json", "r") as f:
    data = json.load(f)

cities = []
for city in data:
    lat = city.get("lat")
    lng = city.get("lng")
    name = city.get("name")
    country = city.get("country")
    pop = city.get("population")
    
    if lat and lng and name and country and pop and isinstance(pop, (int, float)) and pop > 0:
        cities.append({
            "name": name,
            "country": country,
            "lat": float(lat),
            "lng": float(lng),
            "pop": int(pop)
        })

# Sort by population descending
cities.sort(key=lambda x: x["pop"], reverse=True)

# Output as JavaScript
with open("cities.js", "w") as f:
    f.write("// Auto-generated from cities5000.json\n")
    f.write("const citiesData = ")
    f.write(json.dumps(cities, indent=2))
    f.write(";\n")

print(f"Created cities.js with {len(cities)} cities")
