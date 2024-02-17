import sys
sys.path.append('../')

import xlrd
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True

import django,os, time
import threading

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()

from users.models import *
from concurrent.futures import ThreadPoolExecutor
from django.contrib.auth.models import User


def my_get_or_create(MyObj, **kwargs):
    try:
        obj = MyObj.objects.create(**kwargs)
    except InterruptedError:
        transaction.commit()
        obj = MyObj.objects.get(**kwargs)
    return obj

class FacultyPopulate:
    def __init__(self):
        self.path = 'Pilani_faculty.xlsx'
        self.workbook = xlrd.open_workbook(self.path)
        print("Workbook opened")
        self.sheet = self.workbook.sheet_by_index(0)
        self.rows = self.sheet.nrows
        self.columns = self.sheet.ncols

    def populate(self, start):
        for i in range(start, self.rows, 5):
            # auth_user
            user = my_get_or_create(User, username=str(self.sheet.cell_value(i,0)).strip())
            uid = str(self.sheet.cell_value(i,0)).strip()
            name = str(self.sheet.cell_value(i,1)).strip().title()
            if name == '':
                name = 'NA'
            else:
                name = name
            faculty = my_get_or_create(UserProfile, name=name, uid=uid,user_type='Faculty', auth_user=user)
            faculty.save()
            print(f"Added {name} - {uid} - {user.username} - {faculty.user_type}")

def worker(start, faculty):
    print(f"Starting thread starting from {start}")
    faculty.populate(start)
    print(f"Thread finished starting from {start}")

if __name__ == "__main__":
    faculty = FacultyPopulate()
    threads = []
    for i in range(1, 6):
        thread = threading.Thread(target=worker, args=(i, faculty))
        threads.append(thread)
        thread.start()
        #sleep for 5 seconds
        # time.sleep(5)
    for thread in threads:
        thread.join()
    print("Done")
