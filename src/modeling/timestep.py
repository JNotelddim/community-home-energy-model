import pandas as pd

# We're modeling the effect of three external sources of energy that can affect the temperature of the home: 
#  1. Conductive heat gain or loss through contact with the walls and roof (we ignore the floor), given outdoor temperature
#  2. Air change heat gain or loss through air changes between air in the house and outside, given outdoor temperature
#  3. Radiant heat gain from sun coming in south-facing windows

# Also define a few permanent constants
JOULES_PER_MEGAJOULE = 1e9
JOULES_PER_KWH = 3.6e+6
SECONDS_PER_HOUR = 3600
AIR_VOLUMETRIC_HEAT_CAPACITY = 1200 # Energy in joules per cubic meter of air per degree K. (J/m3/K)

# We then model our HVAC system as heating/cooling/off depending on whether the temperature is above or below desired setpoints

def calculate_next_timestep(
    timestamp,
    indoor_temperature_c,
    outdoor_temperature_c,
    irradiance,
    home, #: HomeCharacteristics,
    dt=pd.Timedelta(minutes=10) # Defaulting to a timestep of 10 minute increments
):
    '''
    This function calculates the ΔT (the change in indoor temperature) during a single timestep given:
      1. Previous indoor temperature
      2. Current outdoor temperature (from historical weather data)
      3. Current solar irradiance through south-facing windows (from historical weather data)
      4. Home and HVAC characteristics
    '''

    temperature_difference_c = outdoor_temperature_c - indoor_temperature_c

    # Calculate energy in to building

    # 1. Energy conducted through walls & roof (in Joules, J)
    # Conduction
    # Q = U.A.dT, where U = 1/R
    # Convection:
    # Q = m_dot . Cp * dT <=> Q = V_dot * Cv * dT (Cv = Rho * Cp)

    power_in_through_surface_w = (
        temperature_difference_c * home.surface_area_to_area_sq_m / home.wall_insulation_r_value_si
    )
    energy_from_conduction_j = power_in_through_surface_w * dt.seconds

    # 2. Energy exchanged through air changes with the outside air (in Joules, J)
    air_change_volume = (
        dt.seconds * home.building_volume_cu_m * home.ach_natural / SECONDS_PER_HOUR
    )
    energy_from_air_change_j = (
        temperature_difference_c * air_change_volume * AIR_VOLUMETRIC_HEAT_CAPACITY
    )

    # 3. Energy radiating from the sun in through south-facing windows (in Joules, J)
    energy_from_sun_j = (
        home.south_facing_window_size_sq_m
        * home.window_solar_heat_gain_coefficient
        * irradiance
        * dt.seconds
    )

    # 4. Energy added or removed by the HVAC system (in Joules, J)
    # HVAC systems are either "on" or "off", so the energy they add or remove at any one time equals their total capacity
    if indoor_temperature_c < home.heating_setpoint_c:
        hvac_mode = "heating"
        energy_from_hvac_j = home.hvac_capacity_w * dt.seconds
    elif indoor_temperature_c > home.cooling_setpoint_c:
        hvac_mode = "cooling"
        energy_from_hvac_j = -home.hvac_capacity_w * dt.seconds
    else:
        hvac_mode = "off"
        energy_from_hvac_j = 0

    total_energy_in_j = (
        energy_from_conduction_j
        + energy_from_air_change_j
        + energy_from_sun_j
        + energy_from_hvac_j
    )

    # ΔT is the change in indoor temperature during this timestep resulting from the total energy input
    delta_t = total_energy_in_j / home.building_heat_capacity

    return pd.Series(
        {
            "timestamp": timestamp,
            "temperature_difference_c": temperature_difference_c,
            "Conductive energy (J)": energy_from_conduction_j,
            "Air change energy (J)": energy_from_air_change_j,
            "Radiant energy (J)": energy_from_sun_j,
            "HVAC energy (J)": energy_from_hvac_j,
            "hvac_mode": hvac_mode,
            "Net energy xfer": total_energy_in_j,
            "ΔT": delta_t,
            "Outdoor Temperature (C)": outdoor_temperature_c,
            "Indoor Temperature (C)": indoor_temperature_c + delta_t,
            # Actual energy consumption from the HVAC system:
            "HVAC energy use (kWh)": abs(energy_from_hvac_j) / (JOULES_PER_KWH * home.hvac_overall_system_efficiency)
        }
    )
