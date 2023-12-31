from dataclasses import dataclass
from dataclasses_json import dataclass_json
import math

# To keep things tidier, we define a Home dataclass to bunch all the defined and calculated attributes together
@dataclass_json
@dataclass
class Home:
    id: str
    latitude: float
    longitude: float
    heating_setpoint_c: int
    cooling_setpoint_c: int
    hvac_capacity_w: int
    hvac_overall_system_efficiency: int
    conditioned_floor_area_sq_m: int
    ceiling_height_m: int
    wall_insulation_r_value_imperial: int
    ach50: int
    south_facing_window_size_sq_m: int
    window_solar_heat_gain_coefficient: int

    @property
    def building_volume_cu_m(self) -> int:
        return self.conditioned_floor_area_sq_m * self.ceiling_height_m

    @property
    def building_perimeter_m(self) -> float:
        # Assume the building is a 1-story square
        return math.sqrt(self.conditioned_floor_area_sq_m) * 4
    
    @property
    def surface_area_to_area_sq_m(self) -> float:
        # Surface area exposed to air = wall area + roof area (~= floor area, for 1-story building)
        return self.building_perimeter_m * self.ceiling_height_m + self.conditioned_floor_area_sq_m

    @property
    def ach_natural(self) -> float:
        # "Natural" air changes per hour can be roughly estimated from ACH50 with an "LBL_FACTOR"
        # https://building-performance.org/bpa-journal/ach50-achnat/
        LBL_FACTOR = 17
        return self.ach50 / LBL_FACTOR

    @property
    def wall_insulation_r_value_si(self) -> float:
        # The R-values you typically see on products in the US will be in imperial units (ft^2 °F/Btu)
        # But our calculations need SI units (m^2 °K/W)
        return self.wall_insulation_r_value_imperial / 5.67 # SI units: m^2 °K/W

    @property
    def building_heat_capacity(self) -> int:
        # Building heat capacity
        # How much energy (in kJ) do you have to put into the building to change the indoor temperature by 1 degree?
        # Heat capacity unit: Joules per Kelvin degree (kJ/K)
        # A proper treatment of these factors would include multiple thermal mass components,
        # because the walls, air, furniture, foundation, etc. all store heat differently.
        # More info: https://www.greenspec.co.uk/building-design/thermal-mass/
        HEAT_CAPACITY_FUDGE_FACTOR = 1e5
        return self.building_volume_cu_m * HEAT_CAPACITY_FUDGE_FACTOR

    # @property
    def __str__(self):
        output='''Home {id}:
            lat: {latitude}, long: {longitude},
            heating: {heating_setpoint}, cooling: {cooling_setpoint},
            hvac_capacity_w: {hvac_capacity_w}, hvac_overall_system_efficiency: {hvac_overall_system_efficiency},
            conditioned_floor_area_sq_m: {conditioned_floor_area_sq_m}, ceiling_height_m: {ceiling_height_m}, 
            wall_insulation_r_value_imperial: {wall_insulation_r_value_imperial}, ach50: {ach50},
            south_facing_window_size_sq_m: {south_facing_window_size_sq_m}, window_solar_heat_gain_coefficient: {window_solar_heat_gain_coefficient}
        '''.format(
            id=self.id,
            latitude=self.latitude, longitude=self.longitude,
            heating_setpoint=self.heating_setpoint_c, cooling_setpoint=self.cooling_setpoint_c,
            hvac_capacity_w=self.hvac_capacity_w, hvac_overall_system_efficiency=self.hvac_overall_system_efficiency,
            conditioned_floor_area_sq_m=self.conditioned_floor_area_sq_m, ceiling_height_m=self.ceiling_height_m, 
            wall_insulation_r_value_imperial=self.wall_insulation_r_value_imperial, ach50=self.ach50,
            south_facing_window_size_sq_m=self.south_facing_window_size_sq_m, window_solar_heat_gain_coefficient=self.window_solar_heat_gain_coefficient
        )
        return output
    
    def __getitem__(self,key):
        return getattr(self, key)
    # def __getitem__(self,key):
    #     match key:
    #         case "hvac_overall_system_efficiency":
    #             return self.hvac_overall_system_efficiency
    #         case "ach50":
    #             return self.ach50
    #         case _:
    #             return None

    def __setitem__(self,key, value):
        setattr(self, key, value)