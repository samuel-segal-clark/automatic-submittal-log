from sub_row import ExcelSubmittal
from logger import log
from fuzzy_match import get_spec
from translate_status import translate_status

def update_placeholder(row_sub,sub):
    row_sub.num = str(sub['#'])+'.'+str(sub['Rev.'])
    row_sub.create_date = sub['Created At'].split(' ')[0]

    status = translate_status(sub['Status'])
    row_sub.status = status
    
    if type(sub['Returned Date']) is str and status != 'Open - in Review':
        row_sub.return_date = sub['Returned Date'].split(' ')[-1]
    
    row_sub.update()

def insert_row(sub, excel_data, sheet, title_format = 'Default'):
    csi, _ = get_spec( sub['Spec Section'] )
    same_csi = filter(lambda x: x.spec == csi, excel_data)

    lowest_cell = max(same_csi,key = lambda x: x.row.row)
    q = str( lowest_cell.row.offset(row_offset = 1).row )
    sheet.range(q+':'+q).insert(shift='down')

    #Interalized chauvinism :(
    e_sub = ExcelSubmittal( sheet.range('A'+str(q)+':AD'+str(q)) )
    e_sub.row.color = 255,255,255

    e_sub.spec = csi
    e_sub.num = f"{sub['#']}.{sub['Rev.']}"
    e_sub.location = sub['Location'] if sub['Location'] else 'All Locations'
    e_sub.type = sub['Type']
    e_sub.create_date = sub['Created At'].split(' ')[0]
    e_sub.status_summary = '=IF(OR(X{row}="Approved",X{row}="FRO",X{row}="AAN"),"Closed","Not Closed")'.format(row = e_sub.row.row)

    #TODO This is buggy
    if sub['Returned Date'] and 'nan' not in str(sub['Returned Date']):
        e_sub.return_date = sub['Returned Date'].split('\n')[-1]

    if title_format == 'WMATA':
        #TODO Clean this up
        e_sub.name = sub['Title'].split(' ',maxsplit=1)[1] if len(sub['Title'].split(' '))>0 else sub['Title']
    else:
        e_sub.name = sub['Title']

    e_sub.status = translate_status(sub['Status'])
    
    e_sub.update()
    log(f"Submittal #{sub['#']} inserted at row {q}")
    
