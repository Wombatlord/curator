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
class Artifact:
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
            "imagepermissionlevel": data["imagepermissionlevel"]
        }
        return cls(**kwargs)

    @property
    def strict_date(self) -> bool:
        return self.datebegin == self.dateend
    
    @property
    def has_image_links(self) -> bool:
        return self.imagepermissionlevel == 0

@dataclass
class People:
    role: str
    name: str
    gender: str
    culture: str

    @classmethod
    def parse(cls, data: Artifact):
        kwargs = {
            "role": data[0]["role"],
            "name": data[0]["name"],
            "gender": data[0]["gender"],
            "culture": data[0]["culture"]
        }
        return cls(**kwargs)
