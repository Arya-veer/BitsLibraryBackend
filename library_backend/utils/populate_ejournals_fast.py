import sys
sys.path.append('../')

import django,os, time
import threading

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()

import pandas as pd
from databases.models import Publisher, Subject, EJournal


class EjournalPopulator:
    def __init__(self, file_name):
        print("Populator")
        self.data = pd.read_excel(file_name)
        self.data.fillna("", inplace=True)
        self.publishers = {}
        self.subjects = {}
        self.clean_ejournals()
        self.populate_Publishers ()
        self.populate_subjects ()
        self.populate_ejournals ()

    def clean_ejournals (self):
        print("cleaning ejournals...")
        Publisher.objects.filter(name__in=set(self.data['Publishers'])).delete()
        Subject.objects.filter(name__in=set(self.data['Subject'])).delete()
        EJournal.objects.filter(name__in=set(self.data['Title of Journal'])).delete()

    def populate_publishers (self):
        print("populating publishers...")
        for publisher in Publisher.objects.bulk_create(
            Publisher(name=x) for x in set(self.data['Publishers'])
        ):
            self.publishers[publisher.name] = publisher
    
    def populate_subjects (self):
        print("populating subjects...")
        for subject in Subject.objects.bulk_create(
            Subject(name=x) for x in set(self.data['Subject'])
        ):
            self.subjects[subject.name] = subject

    def populate_ejournals (self):
        print("populating ejournals...")
        Ejournal.objects.bulk_create(
            Ejournal(
                name=row['Title of Journal'],
                publisher=self.publishers[row['Publishers']],
                subject=self.subjects[row['Subject']],
                url=row['URL'],
                extra_data = {
                    'isbn': row['ISSN'],
                    'name of database': row['Name of the Database'],
                    'accessible': row['Access Available at']
                }
            ) for index, row in self.data.iterrows())

if __name__ == "__main__":
    EjournalPopulator('ejournals.xlsx')