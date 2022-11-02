from __future__ import annotations
from dataclasses import dataclass, asdict, field
from src.adaptors.source import Result, Source as _Source
import urllib3
import json
import typing
from typing import Sequence
import os
from dotenv import load_dotenv

load_dotenv()

_KEY = os.environ.get("KEY")


@dataclass
class HAM_Archive:
    info: dict
    records: list[dict]

    @classmethod
    def parse(cls, data: dict) -> HAM_Archive:
        kwargs = {
            "info": data["info"],
            "records": data["records"]
        }
        return cls(**kwargs)


@dataclass
class HAM_Artifact(Result):
    id: int
    accessionyear: str | None = None
    objectnumber: str | None = None
    title: str | None = None
    dated: str | None = None
    datebegin: int | None = None
    dateend: int | None = None
    url: str | None = None
    medium: str | None = None
    primaryimageurl: str | None = None
    imagepermissionlevel: int | None = None
    people: list[HAM_People] = field(default_factory=lambda: [])

    def __str__(self) -> str:
        artist = HAM_People.parse(self.people[0]) if self.people else None

        return "\n".join((
            f"{self.title}: {artist.name if artist else 'unknown'}: {self.dated}",
            f"{self.medium}",
            f"{self.url or 'none provided'}",
            f"{self.primaryimageurl}",
            f"acquired: {self.accessionyear}",
        ))

    @property
    def __dict__(self):
        """
        get a python dictionary
        """
        return asdict(self)

    @property
    def json(self):
        """
        get the json formated string
        """
        return json.dumps(self.__dict__)

    @classmethod
    def parse(cls, data: dict):
        return cls(**_initialise_artifact_raw(data))

    @property
    def strict_date(self) -> bool:
        return self.datebegin == self.dateend

    @property
    def has_image_links(self) -> bool:
        return self.imagepermissionlevel == 0


@dataclass
class HAM_People:
    role: str
    name: str
    gender: str
    culture: str

    @classmethod
    def parse(cls, data: dict):
        kwargs = {
            **data
        }
        filtered = {
            k: v for k, v in kwargs.items()
            if k in {*cls.__annotations__.keys()}
        }
        return cls(**filtered)


def _get_raw(page: int, year: int) -> dict:
    http = urllib3.PoolManager()
    fields = {
        'apikey': _KEY,
        'yearmade': year,
        'page': page,
        # 26 is the classification id for paintings in Harvard Art Museum data.
        'classification': '26',
        # how many items in a response per page.
        'size': 10,
        'hasimage': 1,
        # fields we want included in the response.
        'fields': 'objectnumber,title,dated,datebegin,dateend,url,people,accessionyear,medium,primaryimageurl,imagepermissionlevel,id'
    }

    r = http.request(
        'GET', 'https://api.harvardartmuseums.org/object', fields=fields)
    # print(r.data)
    return json.loads(r.data.decode('utf-8'))


def _get_archive(*args) -> HAM_Archive:
    return HAM_Archive.parse(_get_raw(*args))


class Source(_Source):
    _cached_iter: Sequence[Result] | None = None

    year: int

    def __init__(self, year=1990, **_) -> None:
        super().__init__()
        self.year = year

    def _next_page(self, page) -> None:
        page += 1
        print(f"NEXT PAGE: {page}\n")
        return _get_archive(page, self.year)

    def _all_items(self, page: HAM_Archive) -> Sequence[HAM_Artifact]:
        current = page
        while True:
            for record in current.records:
                yield HAM_Artifact.parse(record)

            if current.info.get("next", None) and (page_num := current.info.get("page", None)):
                current = self._next_page(page_num)
            else:
                break

    def all(self) -> Sequence[Result]:
        return self._all_items(_get_archive(0, self.year))

    def next(self) -> Result:
        if self._cached_iter is None:
            self._cached_iter = self.all()

        return next(self._cached_iter)

    def obj_dump(self):
        artifacts = {"exhibit": []}
        for i, artifact in enumerate(self.all()):
            artifacts["exhibit"].append({f"HAM_{i}: ": artifact.__dict__})

        print(json.dumps(artifacts, indent=4))

    @staticmethod
    def dump():
        raw_data: dict = _get_raw(0, 1990)
        with open(f"./fixtures/page.json", "w+") as file:
            file.write(
                # load the json from the bytes, and then dump to string with formatting
                json.dumps(
                    raw_data,
                    indent=4,
                    sort_keys=True,
                ),
            )


def _initialise_artifact_raw(json_dict: dict) -> dict:
    default_resource = {
        "id": json_dict["id"],
        "objectnumber": None,
        "title": None,
        "dated": None,
        "datebegin": None,
        "dateend": None,
        "url": None,
        "accessionyear": None,
        "medium":  None,
        "primaryimageurl": None,
        "imagepermissionlevel": None,
        "people": []
    }

    return {**default_resource, **json_dict}
