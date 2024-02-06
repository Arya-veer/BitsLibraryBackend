import sys
sys.path.append('../')

import xlrd
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True

import django,os, time
import threading

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()

from databases.models import *
from concurrent.futures import ThreadPoolExecutor

def my_get_or_create(MyObj, **kwargs):
    try:
        obj = MyObj.objects.create(**kwargs)
    except InterruptedError:
        transaction.commit()
        obj = MyObj.objects.get(**kwargs)
    return obj

class EBookPopulate:
    def __init__(self):
        self.path = 'ebooks.xlsx'
        self.workbook = xlrd.open_workbook(self.path)
        print("Workbook opened")
        self.sheet = self.workbook.sheet_by_index(0)
        self.rows = self.sheet.nrows
        self.columns = self.sheet.ncols

    def populate(self, start):
        for i in range(start, self.rows, 5):
            subject = str(self.sheet.cell_value(i,1)).strip().title()
            print(subject)
            if subject == '':
                # subject = Subject.objects.get_or_create(name='NA')[0]
                subject = my_get_or_create(Subject, name='NA')
            else:
                # subject = Subject.objects.get_or_create(name=subject)[0]
                subject = my_get_or_create(Subject, name=subject)
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
                publisher = my_get_or_create(Publisher, name='NA')
            else:
                publisher = my_get_or_create(Publisher, name=publisher)
            url = str(self.sheet.cell_value(i,8)).strip()
            if url == '':
                url = 'NA'
            else:
                url = url
            extra_data = {}
            extra_data['isbn'] = str(self.sheet.cell_value(i,7)).strip()
            extra_data['edition'] = str(self.sheet.cell_value(i,5)).strip()
            extra_data['year'] = str(self.sheet.cell_value(i,6)).strip()
            ebook = my_get_or_create(EBook, name=name, author=author, publisher=publisher, subject=subject, url=url)
            ebook.extra_data = extra_data
            ebook.save()

            print(f"Added {name} - {author} - {publisher} - {subject} - {url} ")

def worker(start, ebook):
    print(f"Starting thread starting from {start}")
    ebook.populate(start)
    print(f"Thread finished starting from {start}")

if __name__ == "__main__":
    ebook = EBookPopulate()
    threads = []
    for i in range(1, 6):
        thread = threading.Thread(target=worker, args=(i,ebook))
        threads.append(thread)
        thread.start()
        #sleep for 5 seconds
        # time.sleep(5)
    for thread in threads:
        thread.join()
    print("Done")
