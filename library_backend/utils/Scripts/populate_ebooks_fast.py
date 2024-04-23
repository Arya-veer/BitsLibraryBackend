import pandas as pd

from databases.models import Publisher, Subject, EBook

class EBookPopulator:
    def __init__(self, file_name):
        print("Populator")
        self.file_name = file_name
        self.data = None
        
        self.publishers = {}
        self.subjects = {}
        
    def run(self):
        self.data = pd.read_excel(self.file_name)
        self.data.fillna("", inplace=True)
        self.__populate_publishers ()
        self.__populate_subjects ()
        self.__populate_ebooks ()

    def __populate_publishers (self):
        print("populating publishers...")
        Publisher.objects.bulk_create(
            (Publisher(name=x) for x in set(self.data['Publisher'])),
            ignore_conflicts=True
        )
        for publisher in Publisher.objects.filter(name__in=set(self.data['Publisher'])):
            self.publishers[publisher.name] = publisher
    
    def __populate_subjects (self):
        print("populating subjects...")
        Subject.objects.bulk_create(
            (Subject(name=x) for x in set(self.data['Subject'])),
            ignore_conflicts=True
        )
        for subject in Subject.objects.filter(name__in=set(self.data['Subject'])):
            self.subjects[subject.name] = subject

    def __populate_ebooks (self):
        print("populating ebooks...")
        EBook.objects.bulk_create(
            (EBook(
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
            ) for index, row in self.data.iterrows()), ignore_conflicts=True)

if __name__ == "__main__":
    EBookPopulator('ebooks.xlsx')