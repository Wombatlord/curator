import os
import json
import sys
from dotenv import load_dotenv
from src.adaptors.curator import Curator

raw_data: list[bytes] = []

def get_raw_fixture(_: str, page: int, __: int) -> dict:
    print("FIXTURE\n")
    return json.load(open(f"./fixtures/page-{page}.json"))


test_mode = "-t" in sys.argv

curator = Curator()

# Swaps out retrieve implementation for testing against dumped snapshots
match test_mode:
    case True:
        retrieve = get_raw_fixture
    case False:
        retrieve = curator.prepare_sources(["HAM"], {"year": 1990})


exhibit = curator.curate_exhibit(retrieve)
print(exhibit)

# curatorGallery = curator.exhibit_index(currentArchive, exhibit=[])

# print(f"There are {len(curatorGallery)} objects in your gallery. \n")

# for i, item in enumerate(curatorGallery):
#     print(str(i) + ": " + item)

# print(currentArchive.info)

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
