from dataclasses import dataclass
from dataclasses_json import dataclass_json
from geopy.geocoders import Nominatim

@dataclass
class NeighborhoodProperties:

    def __init__(self, latitude, longitude, household_income_min, household_income_max):
        self.latitude = latitude
        self.longitude = longitude
        self.household_income_max = household_income_max
        self.household_income_min = household_income_min


    def get_currency_code(self) -> str:
        if self.get_country() == "us":
            return "USD"
        elif self.get_country() == "ca":
            return "CAD"
        else:
            return "USD"

    # Nominatum Location lookup: https://nominatim.org/release-docs/develop/api/Lookup/
    def get_location(self) -> object:
        geoLoc = Nominatim(user_agent="GetLoc")
        return geoLoc.reverse(str(self.latitude) + ", " + str(self.longitude))

    def get_postcode(self) -> str:
        return self.get_location().raw["address"]["postcode"]

    def get_state_province(self) -> str:
        return self.get_location().raw["address"]["state"]

    def get_country(self) -> str:
        return self.get_location().raw["address"]["country_code"]