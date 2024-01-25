import sys
sys.path.append('../')

import xlrd
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True
import django,os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()

from papers.models import Course,TextBook


class TextbookPopulate:
    def __init__(self):
        self.path = 'textbooks.xlsx'
        self.workbook = xlrd.open_workbook(self.path)
        print("Workbook opened")
        self.sheet = self.workbook.sheet_by_index(0)
        self.rows = self.sheet.nrows
        self.columns = self.sheet.ncols
    
    def get_course(self,code,name):
        courses = Course.objects.filter(course_id=code)
        if courses.exists():
            courses.update(name=name)
            return courses.first()
        else:
            return Course.objects.create(course_id=code,name=name)

    def populate(self):
        extra_data = {}
        for i in range(1,self.rows):
            try:
                course = self.get_course(str(self.sheet.cell_value(i,1)).strip(),str(self.sheet.cell_value(i,2)).strip())
                title = str(self.sheet.cell_value(i,3)).strip()
                extra_data['author'] = str(self.sheet.cell_value(i,4)).strip()
                extra_data['publisher'] = str(self.sheet.cell_value(i,5)).strip()
                extra_data['edition'] = str(self.sheet.cell_value(i,6)).strip()
                extra_data['year'] = str(self.sheet.cell_value(i,7)).strip()
                extra_data['type'] = str(self.sheet.cell_value(i,8)).strip()
                to_remove_keys = []
                for key in extra_data.keys():
                    if extra_data[key] == '':
                        to_remove_keys.append(key)
                    elif extra_data[key].isnumeric():
                        extra_data[key] = int(float(extra_data[key]))
                for key in to_remove_keys:
                    extra_data.pop(key)
                print(extra_data)
                url = str(self.sheet.cell_value(i,13)).strip()
                if url.startswith('http'):
                    url = url
                else:
                    continue
                tb = TextBook.objects.create(course=course,title=title,extra_data=extra_data,url=url)
                print(tb)
            except Exception as e:
                print(e)
                print("Error at row",i)
                continue
            


if __name__ == '__main__':
    tbpopulator = TextbookPopulate()
    tbpopulator.populate()
