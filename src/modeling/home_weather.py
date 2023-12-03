import os
import pvlib
from dotenv import load_dotenv

load_dotenv()
NREL_API_KEY=os.getenv('NREL_API_KEY')
NREL_API_EMAIL=os.getenv('NREL_API_EMAIL')

def weather_for_home(home, year):
    solar_weather_timeseries, solar_weather_metadata = pvlib.iotools.get_psm3(
        latitude=home.latitude,
        longitude=home.longitude,
        names=year,
        api_key=NREL_API_KEY,
        email=NREL_API_EMAIL,
        map_variables=True,
        leap_day=True,
    )

    solar_position_timeseries = pvlib.solarposition.get_solarposition(
        time=solar_weather_timeseries.index,
        latitude=home.latitude,
        longitude=home.longitude,
        altitude=100, # Assume close to sea level, this doesn't matter much
        temperature=solar_weather_timeseries["temp_air"],
    )

    window_irradiance = pvlib.irradiance.get_total_irradiance(
        90, # Window tilt (90 = vertical)
        180, # Window compass orientation (180 = south-facing)
        solar_position_timeseries.apparent_zenith,
        solar_position_timeseries.azimuth,
        solar_weather_timeseries.dni,
        solar_weather_timeseries.ghi,
        solar_weather_timeseries.dhi,
    )

    return [solar_weather_timeseries, solar_position_timeseries, window_irradiance]