import sys
sys.path.append('../')

import django,os, time
import threading

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()

import pandas as pd
from users.models import UserProfile
from django.contrib.auth.models import User



class FacultyPopulator:
    def __init__(self, file_name):
        print("Populator")
        self.data = pd.read_excel(file_name)
        self.auth_user = {}
        self.data.fillna("", inplace=True)
        self.populate_auth_user()
        self.populate_faculty ()

    def populate_faculty (self):
        print("populating faculty...")
        UserProfile.objects.bulk_create(
            (UserProfile(
                name=row['Full Name'],
                uid=row['Employee ID'],
                user_type='Faculty',
                auth_user=self.auth_user[row['Employee ID']]
            ) for index, row in self.data.iterrows()), ignore_conflicts=True)
    
    def populate_auth_user(self):
        print("populating auth_user...")
        User.objects.bulk_create(
            (User(username=x) for x in set(self.data['Employee ID'])),
            ignore_conflicts=True
        )
        for user in User.objects.filter(username__in=set(self.data['Employee ID'])):
            self.auth_user[user.username] = user
            

if __name__ == "__main__":
    FacultyPopulator('Pilani_faculty.xlsx')