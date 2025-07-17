import requests
import pandas as pd
from datetime import datetime
import os

# Make sure data folder exists
os.makedirs("data", exist_ok=True)

api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API_KEY environment variable not set.")

url = "https://hydrology.gov.np/gss/api/socket/sun_morang_jica/response"
headers = {"x-api-key": api_key}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("✅ Data fetched successfully.")

    rainfall_records = []
    water_level_records = []

    for station in data:
        station_name = station['name']
        observations = station.get('observations', [])

        for obs in observations:
            param_code = obs.get('parameter_code')
            obs_data = obs.get('data')

            if obs_data:
                for record in obs_data:
                    dt = datetime.fromisoformat(record['datetime'].replace("Z", "+00:00"))
                    date = dt.strftime("%Y-%m-%d")
                    time = dt.strftime("%H:%M")

                    if param_code == 'PCPN_10M':
                        rainfall_records.append({
                            "Station Name": station_name,
                            "Date": date,
                            "Time": time,
                            "Rainfall (mm)": record['value']
                        })
                    elif param_code == 'WL_I_10M':
                        water_level_records.append({
                            "Station Name": station_name,
                            "Date": date,
                            "Time": time,
                            "Water Level (m)": record['value']
                        })

    current_time = datetime.now().strftime("%Y%m%d_%H%M")

    if rainfall_records:
        df_rain = pd.DataFrame(rainfall_records)
        rain_csv = f"data/rainfall_{current_time}.csv"
        df_rain.to_csv(rain_csv, index=False)
        print(f"📥 Saved Rainfall data: {rain_csv}")

    if water_level_records:
        df_water = pd.DataFrame(water_level_records)
        wl_csv = f"data/water_level_{current_time}.csv"
        df_water.to_csv(wl_csv, index=False)
        print(f"📥 Saved Water Level data: {wl_csv}")

else:
    print(f"❌ API Error {response.status_code}: {response.text}")
    exit(1)
