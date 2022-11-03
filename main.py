import json
import sys
from src.adaptors.museum import Museum
from src.services.curator import Curator
from src.adaptors.harvard_art_museum import Source as HAM_Source


def get_raw_fixture(_: str, page: int, __: int) -> dict:
    print("FIXTURE\n")
    return json.load(open(f"./fixtures/page-{page}.json"))


curator = Curator()


exhibit = curator.curate_exhibit([
    Museum.HAM.get_source(),
])


# src = Museum.HAM.get_source()
# source = HAM_Source()
# f = src()

# src().obj_dump()
# source.obj_dump()

# ham.dump(exhibit)


# print(f"There are {len(exhibit)} objects in your gallery. \n")


# for i, item in enumerate(exhibit):
#     print(str(i) + ": " + str(item))
