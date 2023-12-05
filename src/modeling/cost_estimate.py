PERIOD_DAYS=62
BASE_DAILY_RATE_CAD=0.2117
STEP_ONE_RATE_CAD=0.0975
STEP_TWO_RATE_CAD=0.1408
STEP_ONE_THRESHOLD=1376


# Calculate cost of energy consumption based on BC Hydro's formula.
# We can expect the array to be length 12 cause there's always 1 val per month.
# See formula here: https://www.bcuc.com/WhatWeDo/ResidentialEnergyRates
def estimate_cost_by_monthly_consumption_bc(monthly_consumption):
    # billing periods are 62-day cycles which I'm just going to simplify to a 2-month cycle.
    # print(f"Estimating consumption costs based on this data: ...")
    # print(monthly_consumption)
    period_charges=[]
    for i in range(6):
        base_charge=62*BASE_DAILY_RATE_CAD # This obviously isn't exact when we simplify the cycle from 62-days to 2 months.
        start_month=(i*2) + 1
        grouped_consumption=monthly_consumption[start_month] + monthly_consumption[start_month+1]
        step_one_charge=(STEP_ONE_RATE_CAD * grouped_consumption) if grouped_consumption <= STEP_ONE_THRESHOLD else STEP_ONE_RATE_CAD * STEP_ONE_THRESHOLD
        step_two_charge=(STEP_TWO_RATE_CAD * (grouped_consumption - STEP_ONE_THRESHOLD)) if grouped_consumption > STEP_ONE_THRESHOLD else 0 
        total_charge=base_charge + step_one_charge + step_two_charge
        # print(f"Estimated charge for cycle {i} = ${total_charge} CAD.")
        # print(f" __ Based on: base: ${base_charge} + step_one: ${step_one_charge} + step_two: ${step_two_charge} with total period consumption: {grouped_consumption} kWh.")
        period_charges.append(total_charge)
    
    return sum(period_charges)
