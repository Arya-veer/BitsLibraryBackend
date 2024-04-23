
import pandas as pd
from users.models import UserProfile
from django.contrib.auth.models import User

class FacultyPopulator:
    def __init__(self, file_name):
        print("Populator")
        self.file_name = file_name
        self.data = None
        self.auth_user = {}
    
    def run(self):
        self.data = pd.read_excel(self.file_name)
        self.data.fillna("", inplace=True)
        self.__populate_auth_user()
        self.__populate_faculty ()

    def __populate_faculty (self):
        print("populating faculty...")
        UserProfile.objects.bulk_create(
            (UserProfile(
                name=row['Name'],
                uid=row['PSRN'],
                user_type='Faculty',
                auth_user=self.auth_user[row['Email']]
            ) for index, row in self.data.iterrows()), ignore_conflicts=True)
    
    def __populate_auth_user(self):
        print("populating auth_user...")
        User.objects.bulk_create(
            (User(
                username=row['PSRN'],
                email=row['Email'],
            ) for index, row in self.data.iterrows()),
            ignore_conflicts=True
        )
        for user in User.objects.filter(email__in=set(self.data['Email'])):
            self.auth_user[user.email] = user
            

if __name__ == "__main__":
    FacultyPopulator('Pilani_faculty.xlsx')