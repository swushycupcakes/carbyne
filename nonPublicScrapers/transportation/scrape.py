from dotenv import load_dotenv
from firecrawl import FirecrawlApp
import os
import pandas as pd
import re

load_dotenv()

key = os.getenv("FIRECRAWL_KEY")


app = FirecrawlApp(api_key=key)


def extract_county_data(markdown_text):

    county_header_pattern = r'\|\s*([A-Za-z\s]+)\s*County\s*\|'
    
    match = re.search(county_header_pattern, markdown_text["markdown"])
    
    if match:
        start_index = match.start()
        return markdown_text["markdown"][start_index:]
    else:
        return "No county information found."


def segment_counties_and_orgs(data):
    counties = {}
    current_county = None
    current_city = None

    orgs = []

    for line in data.split('\n'):
        line = line.strip()
        if not line:
            continue

        if line.endswith('County |'):
            current_county = line.split('|')[1].strip()
        elif '|' in line:
            parts = [part.strip() for part in line.split('|') if part.strip()]
            if len(parts) == 2:
                current_city = parts[0]
                if parts[1]:
                    parsed_orgs = parse_orgs(parts[1])

                    for x in parsed_orgs:
                        x["city"] = current_city
                        x["county"] = current_county
                        orgs.append(x)
            
        elif current_county and current_city:
    
            parsed_orgs = parse_orgs(line)

            for x in parsed_orgs:
                x["city"] = current_city
                x["county"] = current_county
                orgs.append(x)

    return orgs

def parse_orgs(text):
    orgs = []
    for item in text.split('<br>'):
        item = item.strip()
        if item:
            name_match = re.match(r'\[([^\]]+)\]', item)
            if name_match:
                name = name_match.group(1)
                url_match = re.search(r'\((https?://[^\)]+)\)', item)
                url = url_match.group(1) if url_match else None
                orgs.append({"name": name, "url": url})
            else:
                orgs.append({"name": item, "url": None})
    return orgs


def parse_state_transportation(state_name):

    names = {
    "CA": "California",
    "CO": "Colorado",
    "FL": "Florida",
    "GA": "Georgia",
    "IL": "Illinois",
    "MO": "Missouri",
    "NV": "Nevada",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "PA": "Pennsylvania",
    "SC": "South Carolina",
    "TX": "Texas",
    "VA": "Virginia",
    "WA": "Washington"
    }

    full_name = names[state_name].lower()
    

    URL = f"https://www.apta.com/research-technical-resources/public-transportation-links/{full_name}/"

    scrape_status = app.scrape_url(
        URL, 
        params={'formats': ['markdown', 'html']}
        )
    
    county_data = extract_county_data(scrape_status)
    result = segment_counties_and_orgs(county_data)

    return result





states = ["CA", "CO", "FL", "GA", "IL", "MO", "NV", "OH", "OK", "PA", "SC", "TX", "VA", "WA"]




with pd.ExcelWriter('output/transportation_data.xlsx', mode = 'a') as writer:
    for state in states:
        result = parse_state_transportation(state) 

        df = pd.DataFrame(result)
        
        df.to_excel(writer, sheet_name=state, index=False)