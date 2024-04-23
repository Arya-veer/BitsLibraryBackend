import sys,os,django
sys.path.append('../../')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()

import pandas as pd
from users.models import UserProfile
from django.contrib.auth.models import User



class StudentPopulator:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = None
        self.data.fillna("", inplace=True)
        self.auth_user = {}
        
    def run(self):
        self.data = pd.read_excel(self.file_name)
        User.objects.filter(id__in = UserProfile.objects.filter(user_type='Student').values_list("auth_user")).update(is_active=False)
        self.__populate_auth_user()
        self.__populate_students ()
        
    def __populate_students (self):
        print("populating students...")
        UserProfile.objects.bulk_create(
            (UserProfile(
                name=row['firstname'] + " " + row['surname'],
                uid=row['sort1'],
                user_type='Student',
                auth_user=self.auth_user[row['email']]
            ) for index, row in self.data.iterrows()), ignore_conflicts=True)
    
    def __populate_auth_user(self):
        print("populating auth_user...")
        User.objects.bulk_create(
            (User(
                username=row['sort1'],
                email=row['email'],
                is_active = True
            ) for index, row in self.data.iterrows()),
            ignore_conflicts=True
        )
        for user in User.objects.filter(email__in=set(self.data['email'])):
            self.auth_user[user.email] = user
            

if __name__ == "__main__":
    StudentPopulator('students.xlsx')