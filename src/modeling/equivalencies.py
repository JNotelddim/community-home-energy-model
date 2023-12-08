# Equivalencies Calculations from https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references#gasoline

# Convert 1 kwh avoided to Metric Tons of CO2
def kwh_to_mtco2(kwh):
    return (kwh * .000709)

# Convert 1 Metric Ton of CO2 to a gallon of gas
def mtco2_to_gallons_of_gas(mt):
    return (mt / .008887)

# Convert 1 Metric Ton of CO2 to number of tree seedlings grown for 10 years
def mtco2_to_10_year_trees(mt):
    return (mt / 0.06)

# Convert 1 Metric Ton of CO2 to acres of US Forests sequestering carbon for 1 year
def mtco2_to_forest_acre_year(mt):
    return (mt / 0.84)

