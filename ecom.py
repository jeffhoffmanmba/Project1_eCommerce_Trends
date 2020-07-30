import pandas as pd

# Function to get a dataframe has monthly sales data of Canada.
# Default file name is "data/(2016-2020)Online&Retail_Sales(CA).csv"
def get_canada_df_m(filename = "data/(2016-2020)Online&Retail_Sales(CA).csv"):
    # Read a csv file and create a returning dataframe
    df = pd.read_csv(filename)
    return_df = pd.DataFrame(columns = ["Date", "Overall Retail", "E-Commerce", "E-Shopping and Mail-Order Houses", "Retail Growth(%)", "E-Commerce Growth(%)",
                                        "E-Shopping Growth(%)", "E-Commerce Share(%)", "E-Shopping Share(%)"])
    month_dict = {"01" : "Jan", "02" : "Feb", "03" : "Mar", "04" : "Apr", "05" : "May", "06" : "Jun",
                  "07" : "Jul", "08" : "Aug", "09" : "Sep", "10" : "Oct", "11" : "Nov", "12" : "Dec"}

    # Set variables. US $1 is CA $1.34, UOM is CA $1,000, Returning UOM is US $1 mil
    cur_ex = 1.34
    uom = 1000
    r_uom = 1000000
    idx_cnt = 0

    group_df = df.groupby(["REF_DATE", "Sales"]).sum()

    # Loop through dates
    for date in df.loc[:, "REF_DATE"].unique():
        # Convert date type to make consistent with the date type on us census data
        month = date.split("-")[1]
        year = date.split("-")[0]
        for k, v in month_dict.items():
            month = month.replace(k, v)
        return_df.loc[idx_cnt, "Date"] = month + "/" + year
        # Convert uom from CAD 1,000 to USD 1mil
        return_df.loc[idx_cnt, "Overall Retail"] = group_df.loc[(date, "Retail trade [44-453]"), "VALUE"] * uom / r_uom / cur_ex
        return_df.loc[idx_cnt, "E-Commerce"] = group_df.loc[(date, "Retail E-commerce sales"), "VALUE"] * uom / r_uom  / cur_ex
        return_df.loc[idx_cnt, "E-Shopping and Mail-Order Houses"] = group_df.loc[(date, "Electronic shopping and mail-order houses [45411]"), "VALUE"] * uom / r_uom / cur_ex
        return_df.loc[idx_cnt, "E-Commerce Share(%)"] = return_df.loc[idx_cnt, "E-Commerce"] / return_df.loc[idx_cnt, "Overall Retail"] * 100
        return_df.loc[idx_cnt, "E-Shopping Share(%)"] = return_df.loc[idx_cnt, "E-Shopping and Mail-Order Houses"] / return_df.loc[idx_cnt, "Overall Retail"] * 100
        idx_cnt += 1
    
    for i in range(1, len(return_df.index)):
        # Calculate MoM growth
        return_df.loc[i, "Retail Growth(%)"] = (return_df.loc[i, "Overall Retail"] - return_df.loc[i-1, "Overall Retail"]) / return_df.loc[i-1, "Overall Retail"] * 100
        return_df.loc[i, "E-Commerce Growth(%)"] = (return_df.loc[i, "E-Commerce"] - return_df.loc[i-1, "E-Commerce"]) / return_df.loc[i-1, "E-Commerce"] * 100
        return_df.loc[i, "E-Shopping Growth(%)"] = (return_df.loc[i, "E-Shopping and Mail-Order Houses"] - return_df.loc[i-1, "E-Shopping and Mail-Order Houses"]) / return_df.loc[i-1, "E-Shopping and Mail-Order Houses"] * 100

    return return_df

# Function to get a dataframe has annual sales data of Canada.
# Default file name is "data/(2016-2020)Online&Retail_Sales(CA).csv"
def get_canada_df_y(filename = "data/(2016-2020)Online&Retail_Sales(CA).csv"):
    # Read a csv file and create a returning dataframe
    df = pd.read_csv(filename)
    return_df = pd.DataFrame(columns = ["Date", "Overall Retail", "E-Commerce", "E-Shopping and Mail-Order Houses", "Retail Growth(%)", "E-Commerce Growth(%)",
                                        "E-Shopping Growth(%)", "E-Commerce Share(%)", "E-Shopping Share(%)"])

    # Set variables. US $1 is CA $1.34, UOM is CA $1,000, Returning UOM is US $1 mil
    cur_ex = 1.34
    uom = 1000
    r_uom = 1000000
    idx_cnt = 0

    df["Date"] = df.loc[:, "REF_DATE"].str.split("-", n = 1, expand = True)[0]

    group_df = df.groupby(["Date", "Sales"]).sum()

    # Loop through dates
    for date in df.loc[:, "Date"].unique():
        # Convert date type from "%Y-%m" to "%m/%d/%Y" to make consistent with the date type on us census data
        return_df.loc[idx_cnt, "Date"] = date
        # Convert uom from CAD 1,000 to USD 1mil
        return_df.loc[idx_cnt, "Overall Retail"] = group_df.loc[(date, "Retail trade [44-453]"), "VALUE"] * uom / r_uom / cur_ex
        return_df.loc[idx_cnt, "E-Commerce"] = group_df.loc[(date, "Retail E-commerce sales"), "VALUE"] * uom / r_uom  / cur_ex
        return_df.loc[idx_cnt, "E-Shopping and Mail-Order Houses"] = group_df.loc[(date, "Electronic shopping and mail-order houses [45411]"), "VALUE"] * uom / r_uom / cur_ex
        return_df.loc[idx_cnt, "E-Commerce Share(%)"] = return_df.loc[idx_cnt, "E-Commerce"] / return_df.loc[idx_cnt, "Overall Retail"] * 100
        return_df.loc[idx_cnt, "E-Shopping Share(%)"] = return_df.loc[idx_cnt, "E-Shopping and Mail-Order Houses"] / return_df.loc[idx_cnt, "Overall Retail"] * 100
        idx_cnt += 1
    
    for i in range(1, len(return_df.index)-1):
        # Calculate YoY growth
        return_df.loc[i, "Retail Growth(%)"] = (return_df.loc[i, "Overall Retail"] - return_df.loc[i-1, "Overall Retail"]) / return_df.loc[i-1, "Overall Retail"] * 100
        return_df.loc[i, "E-Commerce Growth(%)"] = (return_df.loc[i, "E-Commerce"] - return_df.loc[i-1, "E-Commerce"]) / return_df.loc[i-1, "E-Commerce"] * 100
        return_df.loc[i, "E-Shopping Growth(%)"] = (return_df.loc[i, "E-Shopping and Mail-Order Houses"] - return_df.loc[i-1, "E-Shopping and Mail-Order Houses"]) / return_df.loc[i-1, "E-Shopping and Mail-Order Houses"] * 100

    # Calculate YoY growth for this year
    last_year_idx, this_year_idx = return_df.tail(2).index
    this_year = return_df.loc[this_year_idx, "Date"]
    last_year = return_df.loc[last_year_idx, "Date"]
    this_year_len = df.loc[df.loc[:, "Date"] == this_year].loc[:, "REF_DATE"].count()
    last_year_df = df.loc[df.loc[:, "Date"] == last_year].head(this_year_len).groupby("Sales").sum() * uom / r_uom / cur_ex

    last_year_retail = last_year_df.loc["Retail trade [44-453]", "VALUE"]
    last_year_ecom = last_year_df.loc["Retail E-commerce sales", "VALUE"]
    last_year_eshop = last_year_df.loc["Electronic shopping and mail-order houses [45411]", "VALUE"]

    idx = return_df.tail(1).index
    return_df.loc[idx, "Retail Growth(%)"] = (return_df.loc[idx, "Overall Retail"] - last_year_retail) / last_year_retail * 100
    return_df.loc[idx, "E-Commerce Growth(%)"] = (return_df.loc[idx, "E-Commerce"] - last_year_ecom) / last_year_ecom * 100
    return_df.loc[idx, "E-Shopping Growth(%)"] = (return_df.loc[idx, "E-Shopping and Mail-Order Houses"] - last_year_eshop) / last_year_eshop * 100

    return return_df

def get_korea_df_m(filename1 = "data/(2015-2020)Retail_Sales(KR).csv", filename2 = "data/(2017-2020)Online_Retail_Sales(KR).csv"):
    # Read csv files and create a returning dataframe
    retail_df = pd.read_csv(filename1)
    ecom_df = pd.read_csv(filename2)

    month_dict = {"01" : "Jan", "02" : "Feb", "03" : "Mar", "04" : "Apr", "05" : "May", "06" : "Jun",
                  "07" : "Jul", "08" : "Aug", "09" : "Sep", "10" : "Oct", "11" : "Nov", "12" : "Dec"}   
    # Set variables. US $1 is about KRW 1200, UOM is KRW 1 mil, Returning UOM is US $1 mil
    cur_ex = 1200

    ret_tot_df = pd.DataFrame(columns = ["Date", "Overall Retail"])
    ecom_tot_df = pd.DataFrame(columns = ["Date", "E-Commerce"])

    # Get overall retail and e-commerce sales data
    ret_tot_df["Date"] = retail_df.columns[1:]
    ret_tot_df["Overall Retail"] = list(map(int, retail_df.iloc[1, 1:]))
    ecom_tot_df["Date"] = ecom_df.columns[2:]
    ecom_tot_df["E-Commerce"] = list(map(int, ecom_df.iloc[0, 2:]))

    # Merge
    return_df = pd.merge(on = "Date", left = ret_tot_df, right = ecom_tot_df)

    # Convert date type to make consistent with the date type on us census data
    return_df["Date"] = return_df.loc[:, "Date"].str.replace(".", "")
    return_df["Month"] = return_df.loc[:, "Date"].str.split(" ", n = 2, expand = True)[1]
    for k, v in month_dict.items():
        return_df["Month"] = return_df["Month"].str.replace(k, v)
    return_df["Year"] = return_df.loc[:, "Date"].str.split(" ", n = 1, expand = True)[0]
    return_df["Date"] = return_df["Month"] + "/" + return_df["Year"]
    return_df = return_df.drop(columns = ["Month", "Year"])

    # Convert uom from KRW 1 mil to USD 1mil
    return_df["Overall Retail"] = return_df.loc[:, "Overall Retail"] / cur_ex
    return_df["E-Commerce"] = return_df.loc[:, "E-Commerce"] / cur_ex

    # Calculate MoM growth
    for i in range(1, len(return_df.index)):
        return_df.loc[i, "Retail Growth(%)"] = (return_df.loc[i, "Overall Retail"] - return_df.loc[i-1, "Overall Retail"]) / return_df.loc[i-1, "Overall Retail"] * 100
        return_df.loc[i, "E-Commerce Growth(%)"] = (return_df.loc[i, "E-Commerce"] - return_df.loc[i-1, "E-Commerce"]) / return_df.loc[i-1, "E-Commerce"] * 100
    
    return_df["E-Commerce Share(%)"] = return_df.loc[:, "E-Commerce"] / return_df.loc[:, "Overall Retail"] * 100

    return return_df

def get_korea_df_y(filename1 = "data/(2015-2020)Retail_Sales(KR).csv", filename2 = "data/(2017-2020)Online_Retail_Sales(KR).csv"):
    # Read csv files and create a returning dataframe
    retail_df = pd.read_csv(filename1)
    ecom_df = pd.read_csv(filename2)
    
    # Set variables. US $1 is about KRW 1200, UOM is KRW 1 mil, Returning UOM is US $1 mil
    cur_ex = 1200

    ret_tot_df = pd.DataFrame(columns = ["Date", "Overall Retail"])
    ecom_tot_df = pd.DataFrame(columns = ["Date", "E-Commerce"])

    # Get overall retail and e-commerce sales data
    ret_tot_df["Date"] = retail_df.columns[1:]
    ret_tot_df["Overall Retail"] = list(map(int, retail_df.iloc[1, 1:]))
    ecom_tot_df["Date"] = ecom_df.columns[2:]
    ecom_tot_df["E-Commerce"] = list(map(int, ecom_df.iloc[0, 2:]))

    # Merge
    df = pd.merge(on = "Date", left = ret_tot_df, right = ecom_tot_df)

    # Convert date type from "%Y. %m" to "%Y"
    df["Date"] = df.loc[:, "Date"].str.replace(".", "").str.split(" ", n = 1, expand = True)[0]

    return_df = df.groupby("Date").sum().reset_index()

    # Convert uom from KRW 1 mil to USD 1mil
    return_df["Overall Retail"] = return_df.loc[:, "Overall Retail"] / cur_ex
    return_df["E-Commerce"] = return_df.loc[:, "E-Commerce"] / cur_ex

    # Calculate YoY growth
    for i in range(1, len(return_df.index)):
        return_df.loc[i, "Retail Growth(%)"] = (return_df.loc[i, "Overall Retail"] - return_df.loc[i-1, "Overall Retail"]) / return_df.loc[i-1, "Overall Retail"] * 100
        return_df.loc[i, "E-Commerce Growth(%)"] = (return_df.loc[i, "E-Commerce"] - return_df.loc[i-1, "E-Commerce"]) / return_df.loc[i-1, "E-Commerce"] * 100
    
    # Calculate YoY growth for this year
    last_year_idx, this_year_idx = return_df.tail(2).index
    this_year = return_df.loc[this_year_idx, "Date"]
    last_year = return_df.loc[last_year_idx, "Date"]
    this_year_len = df.loc[df.loc[:, "Date"] == this_year].loc[:, "Date"].count()
    last_year_df = df.loc[df.loc[:, "Date"] == last_year].head(this_year_len).groupby("Date").sum() / cur_ex

    last_year_retail = last_year_df.iloc[0, 0]
    last_year_ecom = last_year_df.iloc[0, 1]

    idx = return_df.tail(1).index
    return_df.loc[idx, "Retail Growth(%)"] = (return_df.loc[idx, "Overall Retail"] - last_year_retail) / last_year_retail * 100
    return_df.loc[idx, "E-Commerce Growth(%)"] = (return_df.loc[idx, "E-Commerce"] - last_year_ecom) / last_year_ecom * 100

    return_df["E-Commerce Share(%)"] = return_df.loc[:, "E-Commerce"] / return_df.loc[:, "Overall Retail"] * 100

    return return_df