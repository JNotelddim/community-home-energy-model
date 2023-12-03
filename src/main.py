import math
import json
import pvlib

from modeling.home import Home
from modeling.home_weather import weather_for_home
from modeling.energy_model import model_home_energy
from modeling.home_energy_use_aggregate import get_annual_home_energy_use


MODEL_YEAR=2022

targets={
    "hvac_overall_system_efficiency": 4,
    "ach50": 3,
}

if __name__ == '__main__':
    print("Home kit.")

    with open("src/data/homes.json", "r") as read_file:
        homes_data = json.load(read_file)

        homes=[]

        for i, h in enumerate(homes_data["homes"]):
            print(f'Creating home {i}')
            homes.append(Home(
                id=i+1,
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

        [print(home) for home in homes] 

        # only calculating weather data for the first home in the neighborhood
        # assuming the neighborhood is small enought that they'll all be the same.
        print('Generating solar weather data...')
        [solar_weather_timeseries, solar_position_timeseries, window_irradiance]=weather_for_home(homes[0], MODEL_YEAR)

        models={}
        for home in homes:
            print(f'Modeling home {home.id}\'s energy...')

            models[home.id] = model_home_energy(
                home,
                solar_weather_timeseries,
                window_irradiance
            )

        homes_energy_usage={}
        print("Annual totals for each home's energy use:")
        for home_id in models.keys():
            home_annual_hvac_energy_use=get_annual_home_energy_use(models[home_id])
            homes_energy_usage[home_id]=home_annual_hvac_energy_use
            print(f'home {home_id} annual energy use: {math.floor(home_annual_hvac_energy_use)} kWh')
        
        print("Modeling again with home adjustments...")
        adjusted_models={}
        adjusted_homes_energy_usage={}
        for home in homes:
            print(f"Checking home {home.id} stats...")
            home_altered=False
            for key in targets:
                if home[key] < targets[key]:
                    print(f"Adjusting home {home.id} {key} to {targets[key]}...")
                    home[key]=targets[key]
                    home_altered=True
            
            home_model=models[home.id]
            if home_altered:
                print(f"Re-running model for home {home.id} with adjustments...")
                home_model=model_home_energy(
                    home,
                    solar_weather_timeseries,
                    window_irradiance
                )
                home_annual_hvac_energy_use=get_annual_home_energy_use(home_model)
                adjusted_homes_energy_usage[home.id]=home_annual_hvac_energy_use
                print(f"Adjusted home energy use for home {home.id}: {math.floor(home_annual_hvac_energy_use)} kWh")
            
            adjusted_models[home.id] = home_model
        
        print("_______________________")
        print("Homes' energy use before and after adjustments: ...")
        for home in homes:
            before_energy = homes_energy_usage[home.id]
            after_energy = adjusted_homes_energy_usage[home.id] if home.id in adjusted_homes_energy_usage.keys() else homes_energy_usage[home.id]
            print(f"Home {home.id} [ before: {math.floor(before_energy)} kWh, after: {math.floor(after_energy)} kWh ] = { round((before_energy - after_energy) / before_energy * 100) }% reduction")
        
        
        # TODO:
        # Convert energy savings to $ amount.




            
            

