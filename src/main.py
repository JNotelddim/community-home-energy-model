# import sys
# import random
import json
import pvlib

from modeling.home import Home
from modeling.home_weather import weather_for_home
from modeling.energy_model import model_home_energy


MODEL_YEAR=2022

if __name__ == '__main__':
    print("Home kit.")

    with open("src/data/homes.json", "r") as read_file:
        homes_data = json.load(read_file)

        homes=[]

        for i, h in enumerate(homes_data["homes"]):
            print(f'Creating home {i}')
            homes.append(Home(
                latitude=h["latitude"],
                longitude=h["longitude"],
                heating_setpoint_c=h["heating_setpoint_c"],
                cooling_setpoint_c=h["cooling_setpoint_c"],
                hvac_capacity_w=h["hvac_capacity_w"],
                hvac_overall_system_efficiency=h["hvac_overall_system_efficiency"],
                conditioned_floor_area_sq_m=h["conditioned_floor_area_sq_m"],
                ceiling_height_m=h["ceiling_height_m"],
                wall_insulation_r_value_imperial=h["wall_insulation_r_value_imperial"],
                ach50=h["ach50"],
                south_facing_window_size_sq_m=h["south_facing_window_size_sq_m"],
                window_solar_heat_gain_coefficient=h["window_solar_heat_gain_coefficient"],
            ))
            print(f'Home {i} lat: {homes[-1].latitude}, wall_insulation_r_value: {homes[-1].wall_insulation_r_value_imperial}')

        # only calculating weather data for the first home in the neighborhood
        # assuming the neighborhood is small enought that they'll all be the same.
        print('Generating solar weather data...')
        [solar_weather_timeseries, solar_position_timeseries, window_irradiance]=weather_for_home(homes[0], MODEL_YEAR)

        for i, home in enumerate(homes):
            print(f'Modeling home {i}\'s energy...')

            home_energy_model=model_home_energy(
                home,
                solar_weather_timeseries,
                window_irradiance
            )
            # TODO:
            # home_annual_hvac_energy_use=get_annual_home_energy_use(home_energy_model)
            # print(f'home {i} annual energy use: {home_annual_hvac_energy_use}')

