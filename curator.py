import urllib3
import os
import json
from dotenv import load_dotenv
from data import Archive, Painting, People

load_dotenv()

apiKey = os.environ.get("KEY")
http = urllib3.PoolManager()

year = 1990

r = http.request('GET', 'https://api.harvardartmuseums.org/object',
                 fields={
                     'apikey': apiKey,
                     'yearmade': year,
                     # 26 is the classification id for paintings in Harvard Art Museum data.
                     # 30 is sculpture, a | allows for multiple classifications.
                     'classification': '26|30',
                     # how many items in a response per page.
                     'size': 25,
                     'hasimage': 1,
                     'page': 1,
                     # fields we want included in the response.
                     'fields': 'objectnumber,title,dated,datebegin,dateend,url,people,accessionyear,medium,primaryimageurl'
                 })

data = json.loads(r.data.decode('utf-8'))
# data_formatted = json.dumps(data, indent=2)
# print(data_formatted)

# for entry in data["records"]:
#     if entry["datebegin"] == entry["dateend"]:
#         name = entry["people"][0]["name"]
#         print(entry["title"] + ": " + name + ": " + entry["dated"])

currentArchive = Archive.parse(data)
# print(currentArchive.records[0]["people"])

def next_page(page):
    page += 1
    print(f"\n\nNEXT PAGE: {page}\n\n")
    r = http.request('GET', 'https://api.harvardartmuseums.org/object',
                     fields={
                         'apikey': apiKey,
                         'yearmade': year,
                         'page': page,
                         # 26 is the classification id for paintings in Harvard Art Museum data.
                         'classification': '26|30',
                         # how many items in a response per page.
                         'size': 25,
                         'hasimage': 1,
                         # fields we want included in the response.
                         'fields': 'objectnumber,title,dated,datebegin,dateend,url,people,accessionyear,medium,primaryimageurl'
                     })
    
    data = json.loads(r.data.decode('utf-8'))

    return Archive.parse(data)

def exhibit_index(archive: Archive):
    for i, painting in enumerate(archive.records):
        paintings = Painting.parse(painting)

        if paintings.strict_date == True:
            title = paintings.title
            artist = People.parse(archive.records[i]["people"])
            date = paintings.dated
            medium = paintings.medium
            url = paintings.url
            imageurl = paintings.primaryimageurl
            year_bought = paintings.accessionyear

            if paintings.primaryimageurl == None:
                imageurl = "No Direct Image Url"

            print(
                f"{title}: {artist.name}: {date}\n{medium}\n{url}\n{imageurl}\nacquired: {year_bought}\n")

            # print(paintings.title + ": " + artist.name + ": " + paintings.dated + "\n" + paintings.medium +
            #       "\n" + paintings.url + "\n" + str(paintings.primaryimageurl) + "\n" + str(paintings.accessionyear) + "\n")

    try:
        if archive.info['next']:
            exhibit_index(next_page(archive.info["page"]))
    except:
        pass


exhibit_index(currentArchive)
print(currentArchive.info)
