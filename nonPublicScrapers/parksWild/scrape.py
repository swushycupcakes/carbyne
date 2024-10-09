# CA, CO, CT already done manually by blake

from dotenv import load_dotenv
from firecrawl import FirecrawlApp
import os
import pandas as pd
import re

load_dotenv()

key = os.getenv("FIRECRAWL_KEY")


app = FirecrawlApp(api_key=key)


# parks = {
#     "FL": "https://en.wikipedia.org/wiki/List_of_Florida_state_parks",
#     "GA": "https://en.wikipedia.org/wiki/List_of_Georgia_state_parks",
#     "IL": "https://en.wikipedia.org/wiki/List_of_protected_areas_of_Illinois",
#     "MO": "https://en.wikipedia.org/wiki/List_of_Missouri_state_parks",
#     "NV": "https://en.wikipedia.org/wiki/List_of_Nevada_state_parks" ,
#     "OH": "https://en.wikipedia.org/wiki/List_of_protected_areas_of_Ohio" ,
#     "OK": "https://en.wikipedia.org/wiki/List_of_Oklahoma_state_parks",
#     "PA": "https://en.wikipedia.org/wiki/List_of_Pennsylvania_state_parks" ,
#     "TX": "https://en.wikipedia.org/wiki/List_of_Texas_state_parks",
#     "WA": "https://en.wikipedia.org/wiki/List_of_Washington_state_parks" ,
#     "SC": "https://en.wikipedia.org/wiki/List_of_South_Carolina_state_parks" ,
#     "VA": "https://en.wikipedia.org/wiki/List_of_Virginia_state_parks"
# }

parks_map = {
"VA": "https://en.wikipedia.org/wiki/List_of_Virginia_state_parks"
  
}



def get_park_data(state_name):
    url = parks_map[state_name]

    scrape_status = app.scrape_url(
            url, 
            params={'formats': ['html']}
            )
    dfs = pd.read_html(scrape_status["html"], attrs={"class": "wikitable sortable jquery-tablesorter"})

    # below is needed for some of the tables that don' work with other class
    # dfs = pd.read_html(scrape_status["html"], attrs={"class": "wikitable sortable plainrowheaders"})

    df = dfs[0]


    # need the name of the park name column
    for col in df.columns:
        if type(col) == str:
            if "name" in col.lower():
                park_name_col = col
                break
        elif type(col) == tuple:
            if "name" in col[0].lower():
                park_name_col = col
                break

    for col in df.columns:
        if type(col) == str:
            if "county" in col.lower() or "location" in col.lower():
                park_county_col = col
                break
        elif type(col) == tuple:
            if "county" in col[0].lower() or "location" in col.lower():
                park_county_col = col
                break

    if type(park_name_col) == tuple:
        names = df[park_name_col[0], park_name_col[1]].values
    else:
        names = df[park_name_col].values
    if type(park_county_col) == tuple:
        counties = df[park_county_col[0], park_county_col[1]].values
    else:
        counties = df[park_county_col].values

    data = {"Park Name": names, "County": counties}

    result = pd.DataFrame.from_dict(data)

    print(result)

    return result


#print(scrape_status["html"])


# dfs = pd.read_html(scrape_status["html"], attrs={"class": "wikitable sortable jquery-tablesorter"})

# # Since pd.read_html() returns a list of DataFrames, we take the first one
# # (assuming there's only one table with the specified class)
# df = dfs[0]

# # Display the DataFrame
# print(df)


with pd.ExcelWriter('output/parks_data.xlsx', mode = "a") as writer:
    for state in parks_map:
        parks_df = get_park_data(state)
        parks_df.to_excel(writer, sheet_name=state, index=False)


# for state in parks_map:
#     parks_df = get_park_data(state)
    