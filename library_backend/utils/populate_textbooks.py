import sys
sys.path.append('../')

import django,os, time
import threading

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()

import pandas as pd
from papers.models import TextBook, Course
from databases.models import Campus


class TextBookPopulator:
    def __init__(self, file_name):
        print("Populator")
        self.data = pd.read_excel(file_name)
        self.data.fillna("", inplace=True)
        self.courses = {}
        self.campuses = {}
        self.populate_campuses()
        self.populate_courses ()
        self.populate_textbooks ()

    def populate_courses (self):
        print("populating courses...")
        Course.objects.bulk_create(
            Course(
                name=row['Course Title'],
                course_id=row['Course No.'],
            ) for index, row in self.data.iterrows())
        for course in Course.objects.filter(course_id__in=set(self.data['Course No.'])):
            self.courses[course.course_id] = course

    def populate_campuses (self):
        print("populating campuses...")
        Campus.objects.bulk_create(
            (Campus(name='Pilani'), Campus(name='Goa'), Campus(name='Hyderabad')),
            ignore_conflicts=True
        )
        for campus in Campus.objects.all():
            self.campuses[campus.name] = campus

    def populate_textbooks (self):
        print("populating textbooks...")
        TextBook.objects.bulk_create(
            (TextBook(
                title=row['Title'],
                course=self.courses[row['Course No.']],
                url=row['Book Link'],
                extra_data = {
                    'author': row['Author'],
                    'publisher': row['Publisher'],
                    'edition': row['Edition'],
                    'year': row['Year'],
                    'type': row['Remark']
                }
            ) for index, row in self.data.iterrows()), ignore_conflicts=True)

if __name__ == "__main__":
    TextBookPopulator('textbooks.xlsx')