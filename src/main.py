import math
import json
import pvlib
import locale
import pandas as pd
from tabulate import tabulate


from modeling.home import Home
from modeling.home_weather import weather_for_home
from modeling.energy_model import model_home_energy
from modeling.home_energy_use_aggregate import get_annual_home_energy_use, get_monthly_home_energy_use
from modeling.cost_estimate import estimate_cost_by_monthly_consumption_bc
from modeling.equivalencies import *
from incentives.NeighborhoodProperties import *
from incentives.build_tax_scenarios import build_tax_scenarios
from incentives.get_incentives import get_incentives_for_scenario
MODEL_YEAR=2022

targets={
    "hvac_overall_system_efficiency": 4,
    "ach50": 3,
}

if __name__ == '__main__':
    print("Home kit.")
    homes_file = "src/data/average_us_homes.json"
    with open(homes_file, "r") as read_file:
        homes_data = json.load(read_file)

        canada_incentives = json.load(open("src/data/canada_incentives.json", "r"))

        homes=[]
        household_incomes=[]
        household_sizes=[]
        ownership_statuses=[]


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
            household_incomes.append(h["household_income"])
            household_sizes.append(h["household_size"])
            ownership_statuses.append(h["owner_status"])
            household_income_min = min(household_incomes)
            household_income_max = max(household_incomes)
            average_household_size = round(sum(household_sizes) / len(household_sizes))
            scenarios = build_tax_scenarios(household_income_min,household_income_max,ownership_statuses)
        
        neighborhood = NeighborhoodProperties(homes[0]["latitude"],homes[0]["longitude"],int(household_income_min),int(household_income_max), len(homes_data["homes"]))


        print("_______________________")
        [print(home) for home in homes] 


        print("_______________________")
        print("Neighborhood Data")
        print("Number of Homes in Neighborhood: "+str(neighborhood.homes_count))
        print("Household Incomes range from $"+str(household_income_min)+" to $"+str(household_income_max))
        print("Average Household Size: "+str(average_household_size))

        # only calculating weather data for the first home in the neighborhood
        # assuming the neighborhood is small enought that they'll all be the same.
        print("_______________________")
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
        homes_monthly_energy_usage={}
        print("_______________________")
        print("Annual totals for each home's energy use:")
        for home_id in models.keys():
            print(f"Home {home_id}")
            home_annual_hvac_energy_use=get_annual_home_energy_use(models[home_id])
            home_monthly_hvac_energy_use=get_monthly_home_energy_use(models[home_id])
            homes_energy_usage[home_id]=home_annual_hvac_energy_use
            homes_monthly_energy_usage[home_id]=home_monthly_hvac_energy_use
            print(f'home {home_id} annual energy use: {math.floor(home_annual_hvac_energy_use)} kWh')
        
        print("_______________________")
        print("Modeling again with home adjustments...")
        adjusted_models={}
        adjusted_homes_energy_usage={}
        adjusted_homes_monthly_energy_usage={}
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
                home_monthly_hvac_energy_use=get_monthly_home_energy_use(home_model)
                adjusted_homes_energy_usage[home.id]=home_annual_hvac_energy_use
                adjusted_homes_monthly_energy_usage[home.id]=home_monthly_hvac_energy_use
                print(f"Adjusted home energy use for home {home.id}: {math.floor(home_annual_hvac_energy_use)} kWh")
            
            adjusted_models[home.id] = home_model
        
        print("_______________________")
        print("Homes' energy use before and after adjustments: ...")
        neighborhood_sum_consumption_before=0
        neighborhood_sum_consumption_after=0
        neighborhood_sum_cost_before=0
        neighborhood_sum_cost_after=0
        for home in homes:
            before_energy = homes_energy_usage[home.id]
            after_energy = adjusted_homes_energy_usage[home.id] if home.id in adjusted_homes_energy_usage.keys() else homes_energy_usage[home.id]
            before_cost=estimate_cost_by_monthly_consumption_bc(homes_monthly_energy_usage[home.id])
            after_cost=estimate_cost_by_monthly_consumption_bc(adjusted_homes_monthly_energy_usage[home.id]) if home.id in adjusted_homes_monthly_energy_usage.keys() else estimate_cost_by_monthly_consumption_bc(homes_monthly_energy_usage[home.id])
            print(f"__ Home {home.id}")
            print(f"CONSUMPTION: [ before: {math.floor(before_energy)} kWh, after: {math.floor(after_energy)} kWh ] = { round((before_energy - after_energy) / before_energy * 100) }% reduction")
            print(f"$COST(CAD)$: [ before: ${round(before_cost, 2)}, after: ${round(after_cost, 2)} ] = { round((before_cost - after_cost) / before_cost * 100) }% reduction")
            neighborhood_sum_consumption_before+=before_energy
            neighborhood_sum_consumption_after+=after_energy
            neighborhood_sum_cost_before+=before_cost
            neighborhood_sum_cost_after+=after_cost
        
        print("_______________________")
        neighborhood_consumption_difference=round(neighborhood_sum_consumption_before - neighborhood_sum_consumption_after)
        neighborhood_cost_difference=round(neighborhood_sum_cost_before - neighborhood_sum_cost_after, 2)
        print(f"Total Neighborhood energy consumption savings per year: {neighborhood_consumption_difference} kWh ({round((neighborhood_consumption_difference / neighborhood_sum_consumption_before) * 100)}%)")
        print(f"Total Neighborhood energy cost savings per year: ${neighborhood_cost_difference} ({round((neighborhood_cost_difference / neighborhood_sum_cost_before) * 100)}%)")
        print(f"Carbon emissions avoided per year: {round(kwh_to_mtco2(neighborhood_consumption_difference),2)} metric tons of CO2" )
        print(f"Equivalent to {round(mtco2_to_10_year_trees(kwh_to_mtco2(neighborhood_consumption_difference)),0)} tree seedlings grown for 10 years" )
        print(f"Equivalent to {round(mtco2_to_gallons_of_gas(kwh_to_mtco2(neighborhood_consumption_difference)),2)} gallons of gas saved per year" )
        print(f"Equivalent to carbon sequestered by {round(mtco2_to_forest_acre_year(kwh_to_mtco2(neighborhood_consumption_difference)),2)} acres of forest per year" )

        print("_______________________")
        print("Potential Neighborhood Rebates and Credits Summary")
        neighborhood_incentives = [] 
        rebates = []
        tax_credits = []
        incentive_table = pd.DataFrame(neighborhood_incentives)
        rebate_detail = pd.DataFrame(rebates)
        tax_credit_detail = pd.DataFrame(tax_credits)
        if (neighborhood.get_country() == "us"):

            locale.setlocale(locale.LC_ALL, 'en_US')

            for scenario_label, scenario_item in scenarios.items():
                params = {
                    "label": scenario_label,
                    "zip": neighborhood.get_postcode(),
                    "owner_status": scenario_item["owner_status"],
                    "household_income": scenario_item["household_income"],
                    "tax_filing": scenario_item["tax_filing"],
                    "household_size": average_household_size,
                }
                new_incentive = get_incentives_for_scenario(params, scenario_label)
                neighborhood_incentives.append(new_incentive["summary"])
                
                for i in new_incentive["detail"]["pos_rebates"]:
                    rebates.append(pd.Series({
                        "type": i["type"],
                        "item": i["item"],
                        "program": i["program"],
                        "more_info_url": "https://rewiringamerica.org"+i["more_info_url"],
                        "amount": i["amount"],
                        "start_date": i["start_date"],
                        "end_date": i["end_date"],
                        "short_description": i["short_description"],
                        "ami_qualification": i["ami_qualification"],
                        "agi_max_limit": i["agi_max_limit"],
                        "filing_status_required": i["filing_status"]
                    }))
                for i in new_incentive["detail"]["tax_credits"]:
                    tax_credits.append(pd.Series({
                        "type": i["type"],
                        "item": i["item"],
                        "program": i["program"],
                        "more_info_url": "https://rewiringamerica.org"+i["more_info_url"],
                        "amount": i["amount"],
                        "start_date": i["start_date"],
                        "end_date": i["end_date"],
                        "short_description": i["short_description"],
                        "ami_qualification": i["ami_qualification"],
                        "agi_max_limit": i["agi_max_limit"],
                        "filing_status_required": i["filing_status"]
                    }))

            incentive_table = pd.DataFrame(neighborhood_incentives)
            rebate_detail = pd.DataFrame(rebates)
            tax_credit_detail = pd.DataFrame(tax_credits)
            
            print (locale.currency(incentive_table.iloc[0]["pos_savings"], grouping=True)+" USD in savings for each income-qualified home")
            print (locale.currency(incentive_table.iloc[0]["pos_savings"] * neighborhood.homes_count, grouping=True)+" USD total potential savings for Neighborhood")
            print (locale.currency(incentive_table.iloc[1]["tax_savings"], grouping=True)+" USD additional in tax credits available")
            print (locale.currency(incentive_table.iloc[1]["tax_savings"] * neighborhood.homes_count, grouping=True)+" USD total potential tax credits for Neighborhood")
            print (locale.currency(incentive_table.iloc[1]["performance_rebate_savings"], grouping=True)+" Rebates for high-efficiency upgrades")
            if (incentive_table.iloc[2]["performance_rebate_savings"] > incentive_table.iloc[1]["performance_rebate_savings"]):
                print (locale.currency(incentive_table.iloc[2]["performance_rebate_savings"], grouping=True)+" for income-qualified homes")
            print (locale.currency(incentive_table.iloc[2]["performance_rebate_savings"] * neighborhood.homes_count, grouping=True)+" USD additional rebates available for Neighborhood")

            print("_______________________")
            print("Rebates and Credits Detail")
            print(tabulate(rebate_detail, headers='keys', tablefmt='psql'))
            print(tabulate(tax_credit_detail, headers='keys', tablefmt='psql'))


        if (neighborhood.get_country() == "ca"):
            print("Find rebates for your province at "+canada_incentives[str(neighborhood.get_state_province())]["url"])