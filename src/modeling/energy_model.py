import pandas as pd

from modeling.timestep import calculate_next_timestep

def model_home_energy(
    home,
    solar_weather_timeseries,
    window_irradiance
):
    previous_indoor_temperature_c = home.heating_setpoint_c

    timesteps = []
    for timestamp in solar_weather_timeseries.index:
        new_timestep = calculate_next_timestep(
            timestamp=timestamp,
            indoor_temperature_c=previous_indoor_temperature_c,
            outdoor_temperature_c=solar_weather_timeseries.loc[timestamp].temp_air,
            irradiance=window_irradiance.loc[timestamp].poa_direct,
            home=home,
        )
        timesteps.append(new_timestep)
        previous_indoor_temperature_c = new_timestep["Indoor Temperature (C)"]
    
    energy_model = pd.DataFrame(timesteps)
    return energy_model