from data import Archive, Artifact, People


class Curator:
    def __init__(self, year: int, key: str, archives: list[Archive], retrieve) -> None:
        self.archives = archives
        self.year = year
        self.key = key
        self.retrieve = retrieve

    def exhibit_index(self, archive: Archive, exhibit: list) -> list[str]:
        for i, record in enumerate(archive.records):
            artifact = Artifact.parse(record)
            # print(artifact)

            if artifact.strict_date & artifact.has_image_links:
                print("LOG:", f"{artifact.id=}")

                title = artifact.title
                artist = People.parse(archive.records[i]["people"])
                date = artifact.dated
                medium = artifact.medium
                url = artifact.url
                imageurl = artifact.primaryimageurl
                year_bought = artifact.accessionyear

                if artifact.primaryimageurl == None:
                    imageurl = "No Direct Image Url"

                # print(
                #     f"{i}: {title}: {artist.name}: {date}\n{medium}\n{url}\n{imageurl}\nacquired: {year_bought}\n")
                exhibit.append(
                    f"{title}: {artist.name}: {date}\n{medium}\n{url}\n{imageurl}\nacquired: {year_bought}\n")

        try:
            if archive.info['next']:
                self.exhibit_index(self.next_page(archive.info["page"]), exhibit)
        except:
            pass

        return exhibit

    def next_page(self, page):
        page += 1
        print(f"NEXT PAGE: {page}\n")
        data = self.retrieve(self.key, page, self.year)

        return Archive.parse(data)
