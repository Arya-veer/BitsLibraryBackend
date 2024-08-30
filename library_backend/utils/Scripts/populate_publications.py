import sys,os,django
sys.path.append('../../')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()
import pandas as pd

from databases.models import Publication

class PublicationPopulator:
    def __init__(self, file_name):
        print("Populator")
        self.file_name = file_name
        self.data = None
        self.publications = {}
        self.run()
        
    def run(self):
        self.data = pd.read_excel(self.file_name, skiprows=1)
        self.data.fillna("", inplace=True)
        self.__remove_publications()
        self.__populate_publications ()
        
    def __remove_publications(self):
        print("removing publications...")
        Publication.objects.all().delete()

    def __populate_publications (self):
        print("populating publications...")
        Publication.objects.bulk_create(
            (Publication(
                #Authors	Title	Year	Source title	Volume	Issue	DOI	Publisher	ISSN	Type
                authors=row['Authors'],
                title=row['Title'],
                year=row['Year'],
                source_title=row['Source title'],
                volume=row['Volume'],
                issue=row['Issue'],
                doi=row['DOI'],
                publisher=row['Publisher'],
                issn=row['ISSN'],
                publication_type=row['Type']
            ) for index, row in self.data.iterrows()), ignore_conflicts=True)

if __name__ == "__main__":
    PublicationPopulator('Publications of the Month.xlsx')