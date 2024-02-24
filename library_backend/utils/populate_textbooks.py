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
        self.clean_textbooks()
        # self.populate_campuses ()
        self.populate_courses ()
        self.populate_textbooks ()

    def clean_textbooks (self):
        print("cleaning textbooks...")
        Campus.objects.filter(name__in=set(Course.objects.filter(course_id__in=set(self.data['Course No.'])).values_list('campus', flat=True))).delete()
        Course.objects.filter(course_id__in=set(self.data['Course No.'])).delete()
        TextBook.objects.filter(title__in=set(self.data['Title'])).delete()

    def populate_courses (self):
        print("populating courses...")
        for course in Course.objects.bulk_create(
            Course(
                name=row['Course Title'],
                course_id=row['Course No.'],
            ) for index, row in self.data.iterrows()
        ):
            self.courses[course.course] = course

    # def populate_campuses (self):

    def populate_textbooks (self):
        print("populating textbooks...")
        TextBook.objects.bulk_create(
            TextBook(
                title=row['Title'],
                course=self.courses[row['Course No.']],
                url=row['Book Link'],
                extra_data = {
                    'author': row['Author'],
                    'publisher': row['Publisher'],
                    'edition': row['Edition'],
                    'year': row['Year'],
                    'type': row['Remarks']
                }
            ) for index, row in self.data.iterrows())

if __name__ == "__main__":
    TextBookPopulator('textbooks.xlsx')