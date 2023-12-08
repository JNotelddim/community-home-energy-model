# build a range of tax scenarios given the average values of the neighborhood
# head of household and married filing separately statuses tend to overlap with single,
# so are not included in testing API calls.
def build_tax_scenarios(household_income_min = 10000, household_income_max = 250000, ownership_statuses=["homeowner"]):
    scenarios = {}
    if ("homeowner" in ownership_statuses):
        scenarios["single_lowincome_homeowner"] = {"owner_status": "homeowner", "tax_filing": "single", "household_income": household_income_min}
        scenarios["single_highincome_homeowner"] = {"owner_status": "homeowner", "tax_filing": "single", "household_income": household_income_max}
        scenarios["joint_lowincome_homeowner"] = {"owner_status": "homeowner", "tax_filing": "joint", "household_income": household_income_min}
        scenarios["joint_highincome_homeowner"] = {"owner_status": "homeowner", "tax_filing": "joint", "household_income": household_income_max}
        # "hoh_low": {"tax_filing": "hoh", "household_income": household_income_min},
        # "hoh_high": {"tax_filing": "hoh", "household_income": household_income_max},
        # "mseparate_low": {"tax_filing": "married_filing_separately", "household_income": household_income_min},
        # "mseparate_high": {"tax_filing": "married_filing_separately", "household_income": household_income_max}
    if ("renter" in ownership_statuses):
        scenarios["single_lowincome_renter"] = {"owner_status": "renter", "tax_filing": "single", "household_income": household_income_min}
        scenarios["single_highincome_renter"] =  {"owner_status": "renter", "tax_filing": "single", "household_income": household_income_max}
        scenarios["joint_lowincome_renter"] =  {"owner_status": "renter", "tax_filing": "joint", "household_income": household_income_min}
        scenarios["joint_highincome_renter"] =  {"owner_status": "renter", "tax_filing": "joint", "household_income": household_income_max}
    
    return scenarios