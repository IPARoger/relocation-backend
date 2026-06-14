#!/usr/bin/env python3
"""
build_cities.py — GeoNames cities500.txt → enriched JSON + JS

Parses GeoNames cities500.txt (tab-separated) and emits:
  - cities5000_enriched.json  (canonical, compact JSON)
  - cities.js                 (browser bundle: const citiesData = [...])

Each city record includes:
  name, lat, lng, pop, country_code, country, admin1_code, admin1, timezone, geoname_id

Optional reference files (download from geonames.org if you want admin1 names):
  - countryInfo.txt      (overrides built-in ISO country names)
  - admin1CodesASCII.txt (resolves admin1 codes → region names)

Usage:
  python3 build_cities.py
  python3 build_cities.py --min-pop 5000
  python3 build_cities.py --input cities1000.txt
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Built-in ISO 3166-1 alpha-2 → English country name (GeoNames countryInfo
# overrides this if countryInfo.txt is present in the working directory).
# ---------------------------------------------------------------------------
ISO_COUNTRIES: dict[str, str] = {
    "AD": "Andorra", "AE": "United Arab Emirates", "AF": "Afghanistan",
    "AG": "Antigua and Barbuda", "AI": "Anguilla", "AL": "Albania",
    "AM": "Armenia", "AO": "Angola", "AQ": "Antarctica", "AR": "Argentina",
    "AS": "American Samoa", "AT": "Austria", "AU": "Australia", "AW": "Aruba",
    "AX": "Åland Islands", "AZ": "Azerbaijan", "BA": "Bosnia and Herzegovina",
    "BB": "Barbados", "BD": "Bangladesh", "BE": "Belgium", "BF": "Burkina Faso",
    "BG": "Bulgaria", "BH": "Bahrain", "BI": "Burundi", "BJ": "Benin",
    "BL": "Saint Barthélemy", "BM": "Bermuda", "BN": "Brunei", "BO": "Bolivia",
    "BQ": "Bonaire, Sint Eustatius and Saba", "BR": "Brazil", "BS": "Bahamas",
    "BT": "Bhutan", "BV": "Bouvet Island", "BW": "Botswana", "BY": "Belarus",
    "BZ": "Belize", "CA": "Canada", "CC": "Cocos Islands", "CD": "DR Congo",
    "CF": "Central African Republic", "CG": "Congo", "CH": "Switzerland",
    "CI": "Côte d'Ivoire", "CK": "Cook Islands", "CL": "Chile", "CM": "Cameroon",
    "CN": "China", "CO": "Colombia", "CR": "Costa Rica", "CU": "Cuba",
    "CV": "Cape Verde", "CW": "Curaçao", "CX": "Christmas Island",
    "CY": "Cyprus", "CZ": "Czechia", "DE": "Germany", "DJ": "Djibouti",
    "DK": "Denmark", "DM": "Dominica", "DO": "Dominican Republic", "DZ": "Algeria",
    "EC": "Ecuador", "EE": "Estonia", "EG": "Egypt", "EH": "Western Sahara",
    "ER": "Eritrea", "ES": "Spain", "ET": "Ethiopia", "FI": "Finland",
    "FJ": "Fiji", "FK": "Falkland Islands", "FM": "Micronesia", "FO": "Faroe Islands",
    "FR": "France", "GA": "Gabon", "GB": "United Kingdom", "GD": "Grenada",
    "GE": "Georgia", "GF": "French Guiana", "GG": "Guernsey", "GH": "Ghana",
    "GI": "Gibraltar", "GL": "Greenland", "GM": "Gambia", "GN": "Guinea",
    "GP": "Guadeloupe", "GQ": "Equatorial Guinea", "GR": "Greece",
    "GS": "South Georgia", "GT": "Guatemala", "GU": "Guam", "GW": "Guinea-Bissau",
    "GY": "Guyana", "HK": "Hong Kong", "HM": "Heard Island", "HN": "Honduras",
    "HR": "Croatia", "HT": "Haiti", "HU": "Hungary", "ID": "Indonesia",
    "IE": "Ireland", "IL": "Israel", "IM": "Isle of Man", "IN": "India",
    "IO": "British Indian Ocean Territory", "IQ": "Iraq", "IR": "Iran",
    "IS": "Iceland", "IT": "Italy", "JE": "Jersey", "JM": "Jamaica", "JO": "Jordan",
    "JP": "Japan", "KE": "Kenya", "KG": "Kyrgyzstan", "KH": "Cambodia",
    "KI": "Kiribati", "KM": "Comoros", "KN": "Saint Kitts and Nevis",
    "KP": "North Korea", "KR": "South Korea", "KW": "Kuwait", "KY": "Cayman Islands",
    "KZ": "Kazakhstan", "LA": "Laos", "LB": "Lebanon", "LC": "Saint Lucia",
    "LI": "Liechtenstein", "LK": "Sri Lanka", "LR": "Liberia", "LS": "Lesotho",
    "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia", "LY": "Libya",
    "MA": "Morocco", "MC": "Monaco", "MD": "Moldova", "ME": "Montenegro",
    "MF": "Saint Martin", "MG": "Madagascar", "MH": "Marshall Islands",
    "MK": "North Macedonia", "ML": "Mali", "MM": "Myanmar", "MN": "Mongolia",
    "MO": "Macao", "MP": "Northern Mariana Islands", "MQ": "Martinique",
    "MR": "Mauritania", "MS": "Montserrat", "MT": "Malta", "MU": "Mauritius",
    "MV": "Maldives", "MW": "Malawi", "MX": "Mexico", "MY": "Malaysia",
    "MZ": "Mozambique", "NA": "Namibia", "NC": "New Caledonia", "NE": "Niger",
    "NF": "Norfolk Island", "NG": "Nigeria", "NI": "Nicaragua", "NL": "Netherlands",
    "NO": "Norway", "NP": "Nepal", "NR": "Nauru", "NU": "Niue", "NZ": "New Zealand",
    "OM": "Oman", "PA": "Panama", "PE": "Peru", "PF": "French Polynesia",
    "PG": "Papua New Guinea", "PH": "Philippines", "PK": "Pakistan", "PL": "Poland",
    "PM": "Saint Pierre and Miquelon", "PN": "Pitcairn", "PR": "Puerto Rico",
    "PS": "Palestine", "PT": "Portugal", "PW": "Palau", "PY": "Paraguay",
    "QA": "Qatar", "RE": "Réunion", "RO": "Romania", "RS": "Serbia", "RU": "Russia",
    "RW": "Rwanda", "SA": "Saudi Arabia", "SB": "Solomon Islands", "SC": "Seychelles",
    "SD": "Sudan", "SE": "Sweden", "SG": "Singapore", "SH": "Saint Helena",
    "SI": "Slovenia", "SJ": "Svalbard and Jan Mayen", "SK": "Slovakia",
    "SL": "Sierra Leone", "SM": "San Marino", "SN": "Senegal", "SO": "Somalia",
    "SR": "Suriname", "SS": "South Sudan", "ST": "São Tomé and Príncipe",
    "SV": "El Salvador", "SX": "Sint Maarten", "SY": "Syria", "SZ": "Eswatini",
    "TC": "Turks and Caicos Islands", "TD": "Chad", "TF": "French Southern Territories",
    "TG": "Togo", "TH": "Thailand", "TJ": "Tajikistan", "TK": "Tokelau",
    "TL": "Timor-Leste", "TM": "Turkmenistan", "TN": "Tunisia", "TO": "Tonga",
    "TR": "Turkey", "TT": "Trinidad and Tobago", "TV": "Tuvalu", "TW": "Taiwan",
    "TZ": "Tanzania", "UA": "Ukraine", "UG": "Uganda", "UM": "US Minor Outlying Islands",
    "US": "United States", "UY": "Uruguay", "UZ": "Uzbekistan", "VA": "Vatican City",
    "VC": "Saint Vincent and the Grenadines", "VE": "Venezuela", "VG": "British Virgin Islands",
    "VI": "US Virgin Islands", "VN": "Vietnam", "VU": "Vanuatu", "WF": "Wallis and Futuna",
    "WS": "Samoa", "XK": "Kosovo", "YE": "Yemen", "YT": "Mayotte", "ZA": "South Africa",
    "ZM": "Zambia", "ZW": "Zimbabwe",
}


def load_country_info(path: Path) -> dict[str, str]:
    """Load countryInfo.txt if present; merge over built-in ISO map."""
    countries = dict(ISO_COUNTRIES)
    if not path.exists():
        return countries
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.strip().split("\t")
            if len(parts) >= 5:
                countries[parts[0]] = parts[4]
    print(f"  Loaded {path.name} ({len(countries)} countries)")
    return countries


def load_admin1(path: Path) -> dict[str, str]:
    """Load admin1CodesASCII.txt → {'US.CA': 'California', ...}"""
    admin1: dict[str, str] = {}
    if not path.exists():
        return admin1
    with path.open(encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                admin1[parts[0]] = parts[1]
    # Manually reviewed overrides: apply after loading to ensure correct display names.
    admin1["DE.16"] = "Berlin"  # GeoNames says "State of Berlin"; "Berlin" is more natural.
    print(f"  Loaded {path.name} ({len(admin1)} admin1 regions, +overrides)")
    return admin1


def parse_cities(
    input_path: Path,
    countries: dict[str, str],
    admin1: dict[str, str],
    min_pop: int = 0,
) -> list[dict]:
    cities: list[dict] = []
    skipped = 0

    with input_path.open(encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 18:
                skipped += 1
                continue
            try:
                geoname_id = parts[0]
                name = parts[1]
                lat = float(parts[4])
                lng = float(parts[5])
                country_code = parts[8]
                admin1_code = parts[10] if len(parts) > 10 else ""
                population = int(parts[14]) if parts[14] else 0
                timezone = parts[17] if len(parts) > 17 else ""
            except (ValueError, IndexError):
                skipped += 1
                continue

            if population < min_pop:
                continue

            admin1_key = f"{country_code}.{admin1_code}" if admin1_code else ""
            admin1_name = admin1.get(admin1_key, admin1_code) if admin1_code else ""

            cities.append({
                "geoname_id": geoname_id,
                "name": name,
                "lat": lat,
                "lng": lng,
                "pop": population,
                "country_code": country_code,
                "country": countries.get(country_code, country_code),
                "admin1_code": admin1_code,
                "admin1": admin1_name,
                "timezone": timezone,
            })

    cities.sort(key=lambda c: c["pop"], reverse=True)
    if skipped:
        print(f"  Skipped {skipped} malformed lines")
    return cities


def main() -> None:
    parser = argparse.ArgumentParser(description="Build enriched city dataset from GeoNames")
    parser.add_argument("--input", default="cities500.txt", help="GeoNames cities file (tab-separated)")
    parser.add_argument("--min-pop", type=int, default=0, help="Minimum population filter (default: 0 = all rows)")
    parser.add_argument("--json-out", default="cities5000_enriched.json", help="Output JSON path")
    parser.add_argument("--js-out", default="cities.js", help="Output JS bundle path")
    args = parser.parse_args()

    root = Path(".")
    input_path = root / args.input
    if not input_path.exists():
        print(f"ERROR: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Parsing {input_path} (min_pop={args.min_pop})...")
    countries = load_country_info(root / "countryInfo.txt")
    admin1 = load_admin1(root / "admin1CodesASCII.txt")
    cities = parse_cities(input_path, countries, admin1, min_pop=args.min_pop)
    print(f"  → {len(cities)} cities")

    # JSON (canonical)
    json_path = root / args.json_out
    with json_path.open("w", encoding="utf-8") as out:
        json.dump(cities, out, separators=(",", ":"))
    print(f"Wrote {json_path} ({json_path.stat().st_size // 1024} KB)")

    # JS bundle (browser)
    js_path = root / args.js_out
    with js_path.open("w", encoding="utf-8") as out:
        out.write("// Auto-generated by build_cities.py — do not edit by hand\n")
        out.write("const citiesData = ")
        json.dump(cities, out, separators=(",", ":"))
        out.write(";\n")
    print(f"Wrote {js_path} ({js_path.stat().st_size // 1024} KB)")

    # Sample for sanity
    if cities:
        s = cities[0]
        print(f"\nTop city: {s['name']}, {s['admin1']}, {s['country']} ({s['country_code']}) — pop {s['pop']:,}, tz {s['timezone']}")
        # Find a US city for disambiguation demo
        us = next((c for c in cities if c["country_code"] == "US" and c["admin1"]), None)
        if us:
            print(f"US sample: {us['name']}, {us['admin1']}, {us['country']} — pop {us['pop']:,}")


if __name__ == "__main__":
    main()
