from src.adaptors.harvard_art_museum import HAM_Artifact, Source
from src.adaptors.museum import Museum
from src.adaptors.source import Result


class AbstractCurator:
    def prepare_sources(self) -> list:
        raise NotImplementedError

    def full_exhibit(self) -> list:
        raise NotImplementedError

    def curate_exhibit(self) -> list:
        raise NotImplementedError


class Curator(AbstractCurator):
    @staticmethod
    def _ham_date_image_filter(artifact) -> bool:
        return artifact.strict_date & artifact.has_image_links

    def prepare_sources(self, labels: list[str], query) -> list:
        archive = []
        for label in labels:
            if label == "HAM":
                source_class = Museum.HAM.get_source()
                result = source_class(query.get("year"))
                archive.append(result.all())

        return archive
    
    def full_exhibit(self, archive: list):
        for records in archive:
            for record in records:
                artifact = HAM_Artifact.parse(record)
                print(artifact)
    
    def curate_exhibit(self, sources: list):
        for source in sources:
            for item in source:
                artifact = HAM_Artifact.parse(item)
                if Curator._ham_date_image_filter(artifact):
                    print(artifact)

