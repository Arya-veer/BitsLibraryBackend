import sys
sys.path.append('../')

import xlrd

import django,os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()

from databases.models import *

class EJournalPopulator:
    def __init__(self):
        self.path = 'ejournals.xlsx'
        self.workbook = xlrd.open_workbook(self.path)
        print("Workbook opened")
        self.sheet = self.workbook.sheet_by_index(0)
        self.rows = self.sheet.nrows
        self.columns = self.sheet.ncols
    
    def populate(self):
        for i in range(1,self.rows):
            title = str(self.sheet.cell_value(i,1)).strip().title()
            if title == '':
                title = Subject.objects.get_or_create(name='NA')[0]
            else:
                title = Subject.objects.get_or_create(name=title)[0]
            subject = str(self.sheet.cell_value(i,5)).strip().title()
            if subject == '':
                subject = Subject.objects.get_or_create(name='NA')[0]
            else:
                subject = Subject.objects.get_or_create(name=subject)[0]
            publisher = str(self.sheet.cell_value(i,2)).strip().title()
            if publisher == '':
                publisher = Publisher.objects.get_or_create(name='NA')[0]
            else:
                publisher = Publisher.objects.get_or_create(name=publisher)[0]
            url = str(self.sheet.cell_value(i,4)).strip()
            if url == '':
                url = 'NA'
            else:
                url = url
            extra_data = {}
            extra_data['isbn'] = str(self.sheet.cell_value(i,3)).strip()
            extra_data['name of database'] = str(self.sheet.cell_value(i,6)).strip()
            extra_data['accessible'] = str(self.sheet.cell_value(i,7)).strip()
            EBook.objects.filter(name=title,publisher=publisher,subject=subject,url=url).delete()
            ejournal = EJournal.objects.get_or_create(name=title,publisher=publisher,subject=subject,url=url,extra_data = extra_data)[0]
            print(f"Added {title} - {publisher} - {subject} - {url} ")


if __name__ == "__main__":
    populator = EJournalPopulator()
    populator.populate()

