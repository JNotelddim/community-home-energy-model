ENERGY_USE_COLUMN="HVAC energy use (kWh)"

def get_annual_home_energy_use(home_energy_model):
    energy_use=sum(home_energy_model[ENERGY_USE_COLUMN])
    return energy_use

def get_monthly_home_energy_use(home_energy_model):
    get_month=lambda idx: home_energy_model.loc[idx]['timestamp'].month
    monthly_energy_use=home_energy_model.groupby(by=get_month)[ENERGY_USE_COLUMN].sum()
    # print(monthly_energy_use)
    return monthly_energy_use