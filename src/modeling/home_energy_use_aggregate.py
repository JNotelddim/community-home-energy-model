def get_annual_home_energy_use(home_energy_model):
    energy_use=sum(home_energy_model["HVAC energy use (kWh)"])
    return energy_use