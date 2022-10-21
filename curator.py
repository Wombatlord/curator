import urllib3
import os
import json
from dotenv import load_dotenv

load_dotenv()

apiKey = os.environ.get("KEY")
http = urllib3.PoolManager()

year = 1990

r = http.request('GET', 'https://api.harvardartmuseums.org/object',
                 fields={
                     'apikey': apiKey,
                     'yearmade': year,
                     # 26 is the classification id for paintings in Harvard Art Museum data.
                     'classification': '26',
                     # how many items in a response per page.
                     'size': '50',
                     # fields we want included in the response.
                     'fields': 'objectnumber,title,dated,datebegin,dateend,url,people'
                 })

data = json.loads(r.data.decode('utf-8'))
# data_formatted = json.dumps(data, indent=2)
# print(data_formatted)

for entry in data["records"]:
    if entry["datebegin"] == entry["dateend"]:
        name = entry["people"][0]["name"]
        print(entry["title"] + ": " + name + ": " + entry["dated"])
