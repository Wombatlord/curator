import json
import sys
from src.adaptors.museum import Museum
from src.services.curator import Curator
from src.adaptors.harvard_art_museum import Source
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
        pass


# exhibit = curator.curate_exhibit([
#     Museum.HAM.get_source(),
# ])

source = Source()

source.obj_dump()

# ham.dump(exhibit)

# print(f"There are {len(curatorGallery)} objects in your gallery. \n")

# for i, item in enumerate(curatorGallery):
#     print(str(i) + ": " + item)


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
