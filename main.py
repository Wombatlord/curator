import urllib3
import os
import json
import sys
from dotenv import load_dotenv
from curator import Curator
from data import Archive, Artifact, People
from curator import Curator

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


currentArchive = Archive.parse(retrieve(apiKey, 1, year))

curator = Curator(1990, apiKey, retrieve)
curatorGallery = curator.exhibit_index(currentArchive, exhibit=[])

print(f"There are {len(curatorGallery)} objects in your gallery. \n")

for i, item in enumerate(curatorGallery):
    print(str(i) + ": " + item)

print(currentArchive.info)

# Dump raw data snapshots if -d or --dump appear in command line args
dump_mode = set(sys.argv) & {"-d", "--dump"} != set()
if dump_mode:
    for i, content in enumerate(raw_data):
        i += 1
        with open(f"./fixtures/page-{i}.json", "w+") as file:
            file.write(
                # load the json from the bytes, and then dump to string with formatting
                json.dumps(
                    json.loads(content.decode()),
                    indent=4,
                    sort_keys=True,
                ),
            )
