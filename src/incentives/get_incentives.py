import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Query Rewiring America API to summarize incentives

load_dotenv()
REWIRINGAMERICA_API_KEY=os.getenv('REWIRINGAMERICA_API_KEY')

def get_incentives_for_scenario(params, scenario_label):
    url = "https://api.rewiringamerica.org/api/v0/calculator"
    headers = {"Authorization": "Bearer " + REWIRINGAMERICA_API_KEY}
    try:
        response = requests.get(url, headers=headers, params=params)
        incentives = response.json()
        incentive_detail = ""
        incentive_summary = pd.Series(
            {
                "tax_scenario": scenario_label,
                "is_under_80_ami": incentives["is_under_80_ami"],
                "is_under_150_ami": incentives["is_under_150_ami"],
                "is_over_150_ami": incentives["is_over_150_ami"],
                "pos_savings": incentives["pos_savings"],
                "tax_savings": incentives["tax_savings"],
                "performance_rebate_savings": incentives["performance_rebate_savings"],
                "estimated_annual_savings": incentives["estimated_annual_savings"],
            }
        )
        
        incentive_details = {
            "pos_rebates": incentives["pos_rebate_incentives"],
            "tax_credits": incentives["tax_credit_incentives"]
        }

        return {"summary": incentive_summary,
        "detail" : incentive_details}
    except Exception as e:
        print("Received response error code", e)
        print(response.headers)
        raise