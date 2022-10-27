from __future__ import annotations
from dataclasses import dataclass
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
    accessionyear: str
    objectnumber: str
    title: str
    dated: str
    datebegin: int
    dateend: int
    url: str
    medium: str
    primaryimageurl: str
    imagepermissionlevel: int
    people: list

    def __str__(self) -> str:
        title = self.title
        artist = HAM_People.parse(self.people)
        date = self.dated
        medium = self.medium
        url = self.url
        imageurl = self.primaryimageurl
        year_bought = self.accessionyear

        if self.primaryimageurl == None:
            imageurl = "No Direct Image Url"

        return f"{title}: {artist.name}: {date}\n{medium}\n{url}\n{imageurl}\nacquired: {year_bought}\n"

    @classmethod
    def parse(cls, data: dict):
        kwargs = {
            "id": data["id"],
            "objectnumber": data["objectnumber"],
            "title": data["title"],
            "dated": data["dated"],
            "datebegin": data["datebegin"],
            "dateend": data["dateend"],
            "url": data["url"],
            "accessionyear": data["accessionyear"],
            "medium": data["medium"],
            "primaryimageurl": data["primaryimageurl"],
            "imagepermissionlevel": data["imagepermissionlevel"],
            "people": data.get("people", [])
        }
        return cls(**kwargs)

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
            "role": data[0]["role"],
            "name": data[0]["name"],
            "gender": data[0]["gender"],
            "culture": data[0]["culture"]
        }
        return cls(**kwargs)


def _get_raw(page: int, year: int) -> dict:
    http = urllib3.PoolManager()
    fields={
        'apikey': _KEY,
        'yearmade': year,
        'page': page,
        # 26 is the classification id for paintings in Harvard Art Museum data.
        'classification': '26',
        # how many items in a response per page.
        'size': 5,
        'hasimage': 1,
        # fields we want included in the response.
        'fields': 'objectnumber,title,dated,datebegin,dateend,url,people,accessionyear,medium,primaryimageurl,imagepermissionlevel,id'
    }

    r = http.request('GET', 'https://api.harvardartmuseums.org/object', fields=fields)
    # print(r.data)
    return json.loads(r.data.decode('utf-8'))


def _get_archive(*args) -> HAM_Archive:
    return HAM_Archive.parse(_get_raw(*args))


class Source(_Source):
    _cached_iter: Sequence[Result] | None = None

    year: int

    def __init__(self, year=None, **_) -> None:
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
                yield record
            
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
