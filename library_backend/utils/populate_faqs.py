import sys
sys.path.append('../')

import xlrd,json

import django,os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()

from misc.models import *

class FAQPopulate:
    def __init__(self) -> None:
        # stores faq.json in self.data
        with open('faqs.json','r') as f:
            self.data = json.load(f)
        print("FAQ JSON loaded")
    
    def populate(self):
        for i in self.data:
            question = i['question'].strip()
            answer = i['content'].strip()
            FreqAskedQuestion.objects.get_or_create(question=question,answer=answer)
            print(f"Added {question}")


if __name__ == "__main__":
    faq = FAQPopulate()
    faq.populate()