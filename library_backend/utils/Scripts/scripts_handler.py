from utils.Scripts.populate_ebooks_fast import EBookPopulator
from utils.Scripts.populate_ejournals_fast import EjournalPopulator
from utils.Scripts.populate_faculty_fast import FacultyPopulator
from utils.Scripts.populate_students import StudentPopulator

import threading

SCRIPT_TO_CLASS_MAPPING = {
    "EBooks": EBookPopulator,
    "EJournals": EjournalPopulator,
    "Faculty": FacultyPopulator,
    "Student": StudentPopulator
}


class ScriptsHandler:
    
    def __init__(self,data_excel) -> None:
        Script = SCRIPT_TO_CLASS_MAPPING[data_excel.purpose]
        self.data_excel = data_excel
        self.script = Script(data_excel.excel)
        
    def __run_script(self):
        self.data_excel.errors = []
        try:
            self.script.run()
            self.data_excel.status = "Completed"
        except Exception as e:
            self.data_excel.errors.append(str(e))
            self.data_excel.status = "Failed"
        self.data_excel.save()
    
    def populate(self):
        # Create a new thread
        thread = threading.Thread(target=self.__run_script)
        thread.start()
        print("Thread working!!!")
        return
    

if __name__ == "__main__":
    pass