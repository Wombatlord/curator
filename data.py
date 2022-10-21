from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Gallery:
    info: dict
    records: list[dict]

    @classmethod
    def parse(cls, data: dict) -> Gallery:
        kwargs = {
            "info": data["info"],
            "records": data["records"]
        }
        return cls(**kwargs)


@dataclass
class Painting:
    objectnumber: str
    title: str
    dated: str
    datebegin: int
    dateend: int
    # url: str
    # people: list[dict]

    @classmethod
    def parse(cls, data: Gallery):
        kwargs = {
            "objectnumber": data["objectnumber"],
            "title": data["title"],
            "dated": data["dated"],
            "datebegin": data["datebegin"],
            "dateend": data["dateend"],
            # "url": data[""],
            # people: list[dict]
        }
        return cls(**kwargs)