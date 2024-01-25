import sys
sys.path.append('../')

import xlrd

import django,os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()

from databases.models import *


class EBookPopulate:
    def __init__(self):
        self.path = 'ebooks.xlsx'
        self.workbook = xlrd.open_workbook(self.path)
        print("Workbook opened")
        self.sheet = self.workbook.sheet_by_index(0)
        self.rows = self.sheet.nrows
        self.columns = self.sheet.ncols

    def populate(self):
        for i in range(1,self.rows):
            subject = str(self.sheet.cell_value(i,1)).strip().title()
            if subject == '':
                subject = Subject.objects.get_or_create(name='NA')[0]
            else:
                subject = Subject.objects.get_or_create(name=subject)[0]
            author = str(self.sheet.cell_value(i,2)).strip().title()
            if author == '':
                author = 'NA'
            else:
                author = author
            name = str(self.sheet.cell_value(i,3)).strip().title()
            if name == '':
                name = 'NA'
            else:
                name = name
            publisher = str(self.sheet.cell_value(i,5)).strip().title()
            if publisher == '':
                publisher = Publisher.objects.get_or_create(name='NA')[0]
            else:
                publisher = Publisher.objects.get_or_create(name=publisher)[0]
            url = str(self.sheet.cell_value(i,8)).strip()
            if url == '':
                url = 'NA'
            else:
                url = url
            extra_data = {}
            extra_data['isbn'] = str(self.sheet.cell_value(i,7)).strip()
            extra_data['edition'] = str(self.sheet.cell_value(i,5)).strip()
            extra_data['year'] = str(self.sheet.cell_value(i,6)).strip()
            ebook = EBook.objects.get_or_create(name=name,author=author,publisher=publisher,subject=subject,url=url)[0]
            ebook.extra_data = extra_data
            ebook.save()

            print(f"Added {name} - {author} - {publisher} - {subject} - {url} ")

if __name__ == "__main__":
    ebook = EBookPopulate()
    ebook.populate()