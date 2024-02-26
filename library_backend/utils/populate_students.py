import sys
sys.path.append('../')

import django,os, time
import threading

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()

import pandas as pd
from users.models import UserProfile
from django.contrib.auth.models import User



class StudentPopulator:
    def __init__(self, file_name):
        print("Populator")
        self.data = pd.read_excel(file_name)
        self.auth_user = {}
        self.data.fillna("", inplace=True)
        self.populate_auth_user()
        self.populate_students ()

    def populate_students (self):
        print("populating students...")
        UserProfile.objects.bulk_create(
            (UserProfile(
                name=row['firstname'] + " " + row['surname'],
                uid=row['sort1'],
                user_type='Student',
                auth_user=self.auth_user[row['email']]
            ) for index, row in self.data.iterrows()), ignore_conflicts=True)
    
    def populate_auth_user(self):
        print("populating auth_user...")
        User.objects.bulk_create(
            (User(
                username=row['sort1'],
                email=row['email'],
            ) for index, row in self.data.iterrows()),
            ignore_conflicts=True
        )
        for user in User.objects.filter(email__in=set(self.data['email'])):
            self.auth_user[user.email] = user
            

if __name__ == "__main__":
    StudentPopulator('students.xlsx')