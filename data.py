from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Archive:
    info: dict
    records: list[dict]

    @classmethod
    def parse(cls, data: dict) -> Archive:
        kwargs = {
            "info": data["info"],
            "records": data["records"]
        }
        return cls(**kwargs)


@dataclass
class Painting:
    accessionyear: str
    objectnumber: str
    title: str
    dated: str
    datebegin: int
    dateend: int
    url: str
    medium: str
    primaryimageurl: str

    @classmethod
    def parse(cls, data: Archive):
        kwargs = {
            "objectnumber": data["objectnumber"],
            "title": data["title"],
            "dated": data["dated"],
            "datebegin": data["datebegin"],
            "dateend": data["dateend"],
            "url": data["url"],
            "accessionyear": data["accessionyear"],
            "medium": data["medium"],
            "primaryimageurl": data["primaryimageurl"]
        }
        return cls(**kwargs)

    @property
    def strict_date(self) -> bool:
        return self.datebegin == self.dateend

@dataclass
class People:
    role: str
    name: str
    gender: str
    culture: str

    @classmethod
    def parse(cls, data: Painting):
        kwargs = {
            "role": data[0]["role"],
            "name": data[0]["name"],
            "gender": data[0]["gender"],
            "culture": data[0]["culture"]
        }
        return cls(**kwargs)
