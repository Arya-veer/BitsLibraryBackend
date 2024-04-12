import sys
sys.path.append('../')
import django,os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()

from misc.models import DataExcel
from populate_ebooks_fast import EBookPopulator
from populate_ejournals_fast import EjournalPopulator
from populate_faculty_fast import FacultyPopulator

import threading

SCRIPT_TO_CLASS_MAPPING = {
    "Ebooks": EBookPopulator,
    "EJournals": EjournalPopulator,
    "Faculty": FacultyPopulator,
}


class ScriptsHandler:
    
    def __init__(self,data_excel) -> None:
        Script = SCRIPT_TO_CLASS_MAPPING[data_excel.purpose]
        self.data_excel = data_excel
        self.script = Script(data_excel.excel)
        
    def __run_script(self):
        self.data_excel.errors = self.script.run()
        self.data_excel.save()
    
    def populate(self):
        # Create a new thread
        thread = threading.Thread(target=self.__run_script)
        return