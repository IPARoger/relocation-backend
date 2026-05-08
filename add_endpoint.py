import re

with open("main.py", "r") as f:
    content = f.read()

# Check if endpoint already exists
if "@app.post(\"/relocation-chart\")" in content:
    print("Endpoint already exists")
else:
    # Find the last @app.post or @app.get before the if __name__ block
    new_endpoint = '''

@app.post("/relocation-chart")
def relocation_chart(req: dict):
    from math import floor
    
    birth = req["birth_data"]
    loc = req["location"]
    
    jd = julian_day(birth["year"], birth["month"], birth["day"], birth["hour"] + birth["minute"]/60.0)
    
    cusps, ascmc = swe.houses(jd, loc["lat"], loc["lon"], b'P')
    
    planets = {}
    for name, code in [("sun", swe.SUN), ("moon", swe.MOON), ("mercury", swe.MERCURY),
                       ("venus", swe.VENUS), ("mars", swe.MARS), ("jupiter", swe.JUPITER),
                       ("saturn", swe.SATURN), ("uranus", swe.URANUS),
                       ("neptune", swe.NEPTUNE), ("pluto", swe.PLUTO)]:
        lon = swe.calc_ut(jd, code)[0][0] % 360
        sign_idx = floor(lon / 30)
        sign = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"][sign_idx]
        planets[name] = {"longitude": round(lon, 2), "sign": sign, "degree": round(lon % 30, 2)}
    
    placements = {}
    for name, data in planets.items():
        lon = data["longitude"]
        for i in range(12):
            start = cusps[i]
            end = cusps[(i+1)%12]
            if start <= end:
                if start <= lon < end:
                    placements[name] = i+1
                    break
            else:
                if lon >= start or lon < end:
                    placements[name] = i+1
                    break
    
    return {
        "asc": round(ascmc[0] % 360, 2),
        "mc": round(ascmc[1] % 360, 2),
        "planets": planets,
        "placements": placements
    }
'''

    # Insert before the last `if __name__` or at the end
    if "if __name__" in content:
        content = content.replace('if __name__', new_endpoint + '\n\nif __name__')
    else:
        content = content + new_endpoint
    
    with open("main.py", "w") as f:
        f.write(content)
    print("Endpoint added")
