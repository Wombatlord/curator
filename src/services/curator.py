from src.adaptors.harvard_art_museum import Source
import json


class AbstractCurator:
    def full_exhibit(self) -> list:
        raise NotImplementedError()

    def curate_exhibit(self, sources: list[type[Source]]):
        raise NotImplementedError()

    def dump_full_exhibit(self, source_class: type[Source]):
        raise NotImplementedError()

    def dump_filtered_exhibit(self, source_class: type[Source]):
        raise NotImplementedError()


class Curator(AbstractCurator):
    @staticmethod
    def _ham_date_image_filter(artifact) -> bool:
        return artifact.strict_date & artifact.has_image_links

    def full_exhibit(self, archive: list):
        for records in archive:
            for record in records:
                print(record)

    def curate_source(self, source_class: type[Source], gallery: list) -> list:
        for item in source_class().filter(Curator._ham_date_image_filter):
            gallery.append(item)

        return gallery

    def curate_exhibit(self, sources: list[type[Source]]):
        for source in sources:
            # return self.curate_source(source, [])
            self.dump_full_exhibit(source)

    def dump_filtered_exhibit(self, source_class: type[Source], l):
        artifacts = {"exhibit": []}
        
        with open(f"./fixturesTest/page.json", "w+") as file:
            for i, item in enumerate(self.curate_source(source_class, l)):
                artifacts["exhibit"].append({f"Artifact {i}:": str(item)})

            file.write(
                # load the json from the bytes, and then dump to string with formatting
                json.dumps(
                    artifacts,
                    indent=4,
                    sort_keys=True,
                ),
            )

    def dump_full_exhibit(self, source_class: type[Source]):
        artifacts = {"exhibit": []}
        with open(f"./fixturesTest/page.json", "w+") as file:

            for i, item in enumerate(source_class().all()):
                artifacts["exhibit"].append({f"Artifact {i}:": str(item)})

            file.write(
                # load the json from the bytes, and then dump to string with formatting
                json.dumps(
                    artifacts,
                    indent=4,
                    sort_keys=True,
                ),
            )
