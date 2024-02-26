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
        self.data = pd.read_excel(file_name, skiprows=1)
        self.data.fillna("", inplace=True)
        self.publishers = {}
        self.subjects = {}
        self.populate_publishers ()
        self.populate_subjects ()
        self.populate_ejournals ()

    def populate_publishers (self):
        print("populating publishers...")
        Publisher.objects.bulk_create(
            (Publisher(name=x) for x in set(self.data['Publishers'])),
            ignore_conflicts=True
        )
        for publisher in Publisher.objects.filter(name__in=set(self.data['Publishers'])):
            self.publishers[publisher.name] = publisher
    
    def populate_subjects (self):
        print("populating subjects...")
        Subject.objects.bulk_create(
            (Subject(name=x) for x in set(self.data['Subject'])),
            ignore_conflicts=True
        )
        for subject in Subject.objects.filter(name__in=set(self.data['Subject'])):
            self.subjects[subject.name] = subject

    def populate_ejournals (self):
        print("populating ejournals...")
        EJournal.objects.bulk_create(
            (EJournal(
                name=row['Title of Journal'],
                publisher=self.publishers[row['Publishers']],
                subject=self.subjects[row['Subject']],
                url=row['URL'],
                extra_data = {
                    'isbn': row['ISSN'],
                    'name of database': row['Name of the Database'],
                    'accessible': row['Access Available at']
                }
            ) for index, row in self.data.iterrows()), ignore_conflicts=True)

if __name__ == "__main__":
    EjournalPopulator('ejournals.xlsx')