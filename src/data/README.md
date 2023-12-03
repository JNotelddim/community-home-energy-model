# "Home" config variables extra info

## HVAC temperature setpoints (i.e. your thermostat settings)

Your HVAC system will start heating your home if the indoor temperature is below HEATING_SETPOINT_C (house is too cold)
It will start cooling your home if the indoor temperature is above COOLING_SETPOINT_C (house is too warm)
Change the two lines below to match your thermostat settings

```py
heating_setpoint_c=20, ## ~65f
cooling_setpoint_c=22, ## ~75f
```

## HVAC system characteristics

```py
hvac_capacity_w=10000,
```

Different types of HVAC systems have different efficiencies (note: this is a hand-wavy approximation):

- Old boiler with uninsulated pipes = ~0.5
- Electric radiator = ~1
- High-efficiency heat pump = ~4 (how can this be higher than 1?? heat pumpts are magical..)

```py
hvac_overall_system_efficiency=1,
```

## Home dimensions

Note: these are in SI units. If you're used to Imperial: one square meter is 10.7639 sq. ft

```py
conditioned_floor_area_sq_m=200, ## ~2200 sqft
ceiling_height_m=3, ## 10ft ceilings (pretty tall)
```

## Wall Insulation

R value (SI): temperature difference (K) required to create 1 W/m2 of heat flux through a surface. Higher = better insulated

```py
wall_insulation_r_value_imperial=15, ## Imperial units: ft^2 °F/Btu
```

## Air changes per hour at 50 pascals.

This is a measure of the "leakiness" of the home: 3 is pretty tight, A "passive house" is < 0.6
This number is measured in a "blower door test", which pressurizes the home to 50 pascals

```py
ach50=1,
```

## Window area

We're only modeling South-facing windows, as they have the largest effect from solar irradiance (in the Northern hemisphere)
We're assuming the window has an R value matching the walls (so we don't have to model it separately)
Change the line below to roughly match the size of your south-facing windows

```py
south_facing_window_size_sq_m=10, ## ~110 sq ft
```

Solar Heat Gain Coefficient (SHGC) is a ratio of how much of the sun's energy makes it through the window (0-1)
Different types of windows have different values, e.g. a Double-pane, Low-E, H-Gain window SHGC=0.56

```py
window_solar_heat_gain_coefficient=0.5,
```
