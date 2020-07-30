import requests
import pandas as pd
from datetime import datetime, timedelta

# CA: canada, CN: china, KR: south-korea, US: united-states
# get_num_of_cases(countries, dur_months, start_year)
#   countries -> String, if you want to get multiple countries data, you can put a list of countries
#   start_month -> optional, the default value is 1
#   dur_months -> optional, duration in months, if you don't put this value, it will be 5 months
#   start_year -> optional, the default value is 2020

# function for getting monthly COVID 19 confirmed cases from Dec., 2019
def get_num_of_cases(countries, dur_months = 5):
    return_df = pd.DataFrame(columns = ["Country", "Date", "New Cases", "Cumulative Cases"])
    df = pd.DataFrame()
    idx = 0
    base_url = "https://api.covid19api.com/total/country/"
    # Start date
    start_date = datetime(2020, 1, 1, 0, 0, 0)
    # Get the end date
    end_year = start_date.year + 1 if (start_date.month - 1 + dur_months) / 12 > 1 else start_date.year
    end_month = (start_date.month - 1 + dur_months) % 12 if (start_date.month - 1 + dur_months) % 12 != 0 else 12
    end_day = (datetime(end_year, end_month + 1, 1) - timedelta(days=1)).day if end_month != 12 else 31
    end_date = datetime(end_year, end_month, end_day, 23, 59, 59)

    if type(countries) == str:
        countries = [countries]

    idx = 0

    for country in countries:
        url = f"{base_url}{country}/status/confirmed?from={start_date.isoformat()}Z&to={end_date.isoformat()}Z"
        response = requests.get(url).json()

        for data in response:
            try:
                df.loc[idx, "Country"] = data["Country"]
                df.loc[idx, "Date"] = data["Date"].split("T")[0]
                df.loc[idx, "Cases"] = data["Cases"]

            except KeyError:
                print(f"{country} is wrong country name. Check this link to find out more information - https://api.covid19api.com/countries")
                break
                
            idx += 1

    month_date = df["Date"].str.split("-", n = 2, expand = True)[1]
    month_year = df["Date"].str.split("-", n = 2, expand = True)[0]

    month_dict = {"01":"Jan", "02":"Feb", "03":"Mar", "04":"Apr", "05":"May", "06":"Jun",
                  "07":"Jul", "08":"Aug", "09":"Sep", "10":"Oct", "11":"Nov", "12":"Dec"}

    for k, v in month_dict.items():
        month_date = month_date.str.replace(k, v)

    df["Date"] = month_date + "/" + month_year

    group_df = df.groupby(["Country", "Date"]).max()
    idx = 0

    for country in df.loc[:, "Country"].unique():
        month = df.loc[df.loc[:, "Country"] == country].sort_index().head(1).iloc[0, 1]
        return_df.loc[idx, "Country"] = country
        return_df.loc[idx, "Date"] = month
        return_df.loc[idx, "New Cases"] = return_df.loc[idx, "Cumulative Cases"] = group_df.loc[(country, month), "Cases"]

        for month in df.loc[df.loc[:, "Country"] == country].loc[:, "Date"].unique()[1:]:
            return_df.loc[idx+1, "Country"] = country
            return_df.loc[idx+1, "Date"] = month
            return_df.loc[idx+1, "Cumulative Cases"] = group_df.loc[(country, month), "Cases"]
            return_df.loc[idx+1, "New Cases"] = return_df.loc[idx+1, "Cumulative Cases"] - return_df.loc[idx, "Cumulative Cases"]
            idx += 1
        idx += 1

    return return_df
