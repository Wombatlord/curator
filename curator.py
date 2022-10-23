import urllib3
import os
import json
from dotenv import load_dotenv
from data import Archive, Artifact, People

load_dotenv()

apiKey = os.environ.get("KEY")
http = urllib3.PoolManager()

year = 1990

r = http.request('GET', 'https://api.harvardartmuseums.org/object',
                 fields={
                     'apikey': apiKey,
                     'yearmade': year,
                     'page': 1,
                     # 26 is the classification id for paintings in Harvard Art Museum data.
                     # 30 is sculpture, a | allows for multiple classifications.
                     'classification': '30',
                     # how many items in a response per page.
                     'size': 10,
                     'hasimage': 1,
                     # fields we want included in the response.
                     'fields': 'objectnumber,title,dated,datebegin,dateend,url,people,accessionyear,medium,primaryimageurl,imagepermissionlevel'
                 })


data = json.loads(r.data.decode('utf-8'))
# data_formatted = json.dumps(data, indent=2)
# print(data_formatted)

# for entry in data["records"]:
#     if entry["datebegin"] == entry["dateend"]:
#         name = entry["people"][0]["name"]
#         print(entry["title"] + ": " + name + ": " + entry["dated"])

currentArchive = Archive.parse(data)


def next_page(page):
    page += 1
    print(f"NEXT PAGE: {page}\n")
    r = http.request('GET', 'https://api.harvardartmuseums.org/object',
                     fields={
                         'apikey': apiKey,
                         'yearmade': year,
                         'page': page,
                         # 26 is the classification id for paintings in Harvard Art Museum data.
                         'classification': '30',
                         # how many items in a response per page.
                         'size': 10,
                         'hasimage': 1,
                         # fields we want included in the response.
                         'fields': 'objectnumber,title,dated,datebegin,dateend,url,people,accessionyear,medium,primaryimageurl,imagepermissionlevel'
                     })

    data = json.loads(r.data.decode('utf-8'))

    return Archive.parse(data)


def exhibit_index(archive: Archive, exhibit: list) -> list:
    for i, paintings in enumerate(archive.records):
        painting = Artifact.parse(paintings)

        if painting.strict_date and painting.has_image_links:

            title = painting.title
            artist = People.parse(archive.records[i]["people"])
            date = painting.dated
            medium = painting.medium
            url = painting.url
            imageurl = painting.primaryimageurl
            year_bought = painting.accessionyear

            if painting.primaryimageurl == None:
                imageurl = "No Direct Image Url"

            # print(
            #     f"{i}: {title}: {artist.name}: {date}\n{medium}\n{url}\n{imageurl}\nacquired: {year_bought}\n")
            exhibit.append(
                f"{title}: {artist.name}: {date}\n{medium}\n{url}\n{imageurl}\nacquired: {year_bought}\n")

    try:
        if archive.info['next']:
            exhibit_index(next_page(archive.info["page"]), exhibit)
    except:
        pass
    
    return exhibit

gallery = set(exhibit_index(currentArchive, exhibit=[]))
print(f"There are {len(gallery)} objects in your gallery. \n")

for i, item in enumerate(gallery):
    print(str(i) + ": " + item)

print(currentArchive.info)

# SET is working to prevent duplicate entries. It seems when duplicates are present, they have overwritten another item in the response.
# The overwritten item may not fit the filter criteria in this script (eg, may not have an image url), so could appear as "extra" items
# or as an overwrite of something that would be there normally.