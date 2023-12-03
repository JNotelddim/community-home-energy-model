# import os
# import sys
# import random
import json

from modeling.home import Home


if __name__ == '__main__':
    print("Home kit.")

    with open("src/data/homes.json", "r") as read_file:
        homes_data = json.load(read_file)
        # print(homes_data["homes"], " ", "\n")

        # print("... . that was homes. ")

        for h in homes_data["homes"]:
            # print(h)
            home = Home(
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
            )
            print(home.latitude)


