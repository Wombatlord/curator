import urllib3
import os
import json
import sys
from dotenv import load_dotenv
from data import Archive, Artifact, People

load_dotenv()

apiKey = os.environ.get("KEY")
http = urllib3.PoolManager()

year = 1990
raw_data: list[bytes] = []

def get_raw(key: str, page: int, year_: int) -> dict:
    r = http.request('GET', 'https://api.harvardartmuseums.org/object',
                     fields={
                         'apikey': key,
                         'yearmade': year_,
                         'page': page,
                         # 26 is the classification id for paintings in Harvard Art Museum data.
                         'classification': '26',
                         # how many items in a response per page.
                         'size': 5,
                         'hasimage': 1,
                         # fields we want included in the response.
                         'fields': 'objectnumber,title,dated,datebegin,dateend,url,people,accessionyear,medium,primaryimageurl,imagepermissionlevel,id'
                     })
    raw = r.data
    raw_data.append(raw)
    return json.loads(r.data.decode())

def get_raw_fixture(_: str, page: int, __: int) -> dict:    
    print("FIXTURE\n")
    return json.load(open(f"./fixtures/page-{page}.json"))

test_mode = "-t" in sys.argv

# Swaps out retrieve implementation for testing against dumped snapshots
match test_mode:
    case True: 
        retrieve = get_raw_fixture
    case False: 
        retrieve = get_raw


def next_page(page):
    page += 1
    print(f"NEXT PAGE: {page}\n")
    data = retrieve(apiKey, page, year)

    return Archive.parse(data)


def exhibit_index(archive: Archive, exhibit: list) -> list[str]:
    for i, paintings in enumerate(archive.records):
        painting = Artifact.parse(paintings)

        if painting.strict_date and painting.has_image_links:
            print("LOG:", f"{painting.id=}")

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


currentArchive = Archive.parse(retrieve(apiKey, 1, year))

gallery = exhibit_index(currentArchive, exhibit=[])
print(f"There are {len(gallery)} objects in your gallery. \n")

for i, item in enumerate(gallery):
    print(str(i) + ": " + item)

print(currentArchive.info)

# Dump raw data snapshots if -d or --dump appear in command line args
dump_mode = set(sys.argv) & {"-d", "--dump"} != set()
if dump_mode:
    for i, content in enumerate(raw_data):
        i+=1
        with open(f"./fixtures/page-{i}.json", "w+") as file:
            file.write(
                # load the json from the bytes, and then dump to string with formatting
                json.dumps(
                    json.loads(content.decode()), 
                    indent=4, 
                    sort_keys=True,
                ),
            )
