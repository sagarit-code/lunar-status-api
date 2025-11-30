import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENCAGE_KEY = os.getenv("OPENCAGE_KEY")
IPGEO_KEY = os.getenv("IPGEO_KEY")

def get_lunar_data():
    # 1. NOAA KPI
    kpi_url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
    kpi_data = requests.get(kpi_url).json()

    # 2. Get geolocation by IP
    res = requests.get("http://www.geoplugin.net/json.gp").json()
    state = res.get("geoplugin_region")
    country = res.get("geoplugin_countryName")
    q = f"{state}, {country}"

    # 3. Lat/long using OpenCage
    location_url = f"https://api.opencagedata.com/geocode/v1/json?q={q}&key={OPENCAGE_KEY}"
    json_file = requests.get(location_url).json()

    for each in json_file["results"]:
        if "geometry" in each:
            lat = each["geometry"]["lat"]
            lon = each["geometry"]["lng"]

    # 4. Lunar data
    lunar_url = f"https://api.ipgeolocation.io/astronomy?apiKey={IPGEO_KEY}&lat={lat}&long={lon}"
    lunar_data = requests.get(lunar_url).json()

    azimuth = lunar_data["moon_azimuth"]
    angle = 180 + azimuth
    if angle >= 360: angle -= 360
    if angle < 0: angle += 360

    def dir_of(a):
        if 0 < a <= 22.5: return "N"
        if a <= 67.5: return "NE"
        if a <= 112.5: return "E"
        if a <= 157.5: return "SE"
        if a <= 202.5: return "S"
        if a <= 247.5: return "SW"
        if a <= 292.5: return "W"
        if a <= 337.5: return "NW"
        return "N"

    reaction_angle_direction = f"{angle} {dir_of(angle)}"
    actual_direction = f"{azimuth} {dir_of(azimuth)}"

    horizon_status = (
        "below the horizon" if lunar_data["moon_altitude"] < 0 else "above the horizon"
    )

    return {
        "reaction_angle": reaction_angle_direction,
        "actual_angle": actual_direction,
        "lat": lunar_data["location"]["latitude"],
        "lon": lunar_data["location"]["longitude"],
        "horizon": horizon_status
    }

