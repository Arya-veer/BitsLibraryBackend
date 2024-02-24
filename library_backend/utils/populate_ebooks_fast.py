import sys
sys.path.append('../')

import django,os, time
import threading

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()

import pandas as pd
from databases.models import Publisher, Subject, EBook


class EBookPopulator:
    def __init__(self, file_name):
        print("Populator")
        self.data = pd.read_excel(file_name)
        self.data.fillna("", inplace=True)
        self.publishers = {}
        self.subjects = {}
        self.clean_ebooks()
        self.populate_publishers ()
        self.populate_subjects ()
        self.populate_ebooks ()

    def clean_ebooks (self):
        Publisher.objects.filter(name__in=set(self.data['Publisher'])).delete()
        Subject.objects.filter(name__in=set(self.data['Subject'])).delete()
        EBook.objects.filter(name__in=set(self.data['Title'])).delete()

    def populate_publishers (self):
        print("populating publishers...")
        for publisher in Publisher.objects.bulk_create(
            Publisher(name=x) for x in set(self.data['Publisher'])
        ):
            self.publishers[publisher.name] = publisher
    
    def populate_subjects (self):
        print("populating subjects...")
        for subject in Subject.objects.bulk_create(
            Subject(name=x) for x in set(self.data['Subject'])
        ):
            self.subjects[subject.name] = subject

    def populate_ebooks (self):
        print("populating ebooks...")
        EBook.objects.bulk_create(
            EBook(
                name=row['Title'],
                author=row['Author'],
                publisher=self.publishers[row['Publisher']],
                subject=self.subjects[row['Subject']],
                url=row['Url'],
                extra_data = {
                    'isbn': row['ISBN'],
                    'edition': row['Edition'],
                    'year': row['Year']
                }
            ) for index, row in self.data.iterrows())

if __name__ == "__main__":
    EBookPopulator('ebooks.xlsx')