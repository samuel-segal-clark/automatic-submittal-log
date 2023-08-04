from functools import lru_cache
from config import get_property
from xlwings import Range



principal_row : Range | None = None
@lru_cache
def get_index_from_config(config_name: str) -> int | None:
    if not principal_row:
        return None
    
    col_name = get_property('EXCEL_COLUMNS', config_name)
    if not col_name:
        return None
    if type(col_name) is not str:
        return None
    
    col_name = col_name.strip()    

    for i in range(len(principal_row.columns)):
        cell = principal_row.columns[i]
        column = cell.address.split('$')[1]
        
        if column == col_name:
            return i
    
    return None



def get_cell_from_config(row: Range, config: str) -> Range | None:
    global principal_row
    if not principal_row:
        principal_row = row
    
    ind = get_index_from_config(config)
    if ind is not None:
        return row[ind]
    return None


def get_value_from_config(row: Range, attr:str):
    cell = get_cell_from_config(row, attr)
    if cell:
        return cell.value
    return None

def set_value_from_config(row: Range, attr: str, value: any):
    cell = get_cell_from_config(row, attr)
    if cell:
        #TODO Put automatic string integer protections in here
        cell.value = value

class ExcelSubmittal:
    def __init__(self, row: Range):
        self.row = row
        
        self.spec = get_value_from_config(row, 'SpecSection')
        self.name = get_value_from_config(row, 'Title')
        self.sub_spec = get_value_from_config(row, 'SubSpec')
        self.num = get_value_from_config(row, 'Number')
        self.type = get_value_from_config(row, 'ItemType')
        self.sub_by_date = get_value_from_config(row, 'SubmitByDate')
        self.need_approval_date = get_value_from_config(row, 'NeedApprovalDate')
        self.location = get_value_from_config(row, 'Location')
        self.create_date = get_value_from_config(row, 'SubmissionDate')
        self.return_date = get_value_from_config(row, 'ReturnedDate')
        self.status = get_value_from_config(row, 'Status')
        self.status_summary = get_value_from_config(row, 'StatusSummary')

        first_rev = get_cell_from_config(row, 'RevisedDateStart')
        ind = first_rev.column - row.column
        num_revisions = int(get_property('RevisionHandling','MaxRevisedSubmittalDates'))
        self.revisions = row.value[ind:ind+num_revisions]

    def update(self):
        set_value_from_config(self.row, 'SpecSection', self.spec)
        set_value_from_config(self.row, 'Title', self.name)
        set_value_from_config(self.row, 'SubSpec', self.sub_spec)
        set_value_from_config(self.row, 'Number',"'" +  self.num)
        set_value_from_config(self.row, 'ItemType', self.type)
        set_value_from_config(self.row, 'SubmitByDate', self.sub_by_date)
        set_value_from_config(self.row, 'NeedApprovalDate', self.need_approval_date)
        set_value_from_config(self.row, 'Location', self.location)
        set_value_from_config(self.row, 'SubmissionDate', self.create_date)
        set_value_from_config(self.row, 'ReturnedDate', self.return_date)
        set_value_from_config(self.row, 'Status', self.status)
        set_value_from_config(self.row, 'NeedApprovalDate', self.need_approval_date)
        set_value_from_config(self.row,'Location', self.location)
        set_value_from_config(self.row,'StatusSummary', self.status_summary)
        first_rev = get_cell_from_config(self.row, 'RevisedDateStart')
        ind = first_rev.column - self.row.column
        num_revisions = int(get_property('RevisionHandling','MaxRevisedSubmittalDates'))
        self.row[ind:ind+num_revisions].value = self.revisions