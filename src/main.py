#Setting up project
import sys
import os
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.append(cwd)

import pandas as pd
import xlwings as xw
import datetime
from thefuzz import fuzz, process

from review import update_all_rows
from translate_status import translate_status
from logger import get_logger_name, log, set_log_name
from config import get_property
from change_spec import set_sheet_to_long_spec, set_sheet_to_short_spec
from fuzzy_match import set_spec_sections, get_spec, name_match_dialogue
from sub_row import ExcelSubmittal
from populate_row import insert_row, update_placeholder

#Gets logger name
logger_name = get_logger_name()
set_log_name(logger_name)
print('-----Logger Available At-----')
print(logger_name.center(29))
print('-----------------------------')
print()

log('Start Logging')
log('-------------')
log('')

#Loading config
log('Loading config...')
title_format = get_property('PROCORE_READER','TitleFormat')
log('\tTitle Format:',title_format)
change_spec = get_property('SPEC_NUMBER','ChangeSpec')
log('\tChange Spec:',change_spec)
spec_format = get_property('SPEC_NUMBER','SpecFormat')
log('\tSpec Format:',spec_format)


#Loads csv data file
data_filename = 'data.csv'
log('Loading Procore csv submittal data file:\t',data_filename)
data = pd.read_csv(os.path.abspath('..\\files\\'+data_filename))


#Loads submittal log Excel sheet
excel_filename = 'submittal_log.xlsm'
log('Loading submittal log excel file:\t\t',excel_filename)
wb = xw.Book(os.path.abspath('..\\files\\'+excel_filename))
active = wb.sheets['Active']
compare = wb.sheets['Compare']

#Removes filter
log( 'Removing the filter present...')
active.api.AutoFilterMode = False

max_row = active.range('A'+str(active.cells.last_cell.row)).end('up').row

log('Packaging and formatting the Excel data')
#Gets the active data'
active_data = active.range('A7:AD'+str(max_row))
excel_submittals = list()
division = int(len(active_data.rows)/20)
for i in range(len(active_data.rows)):
    if i%division == 0:
        print('\t',int(100*i/len(active_data.rows)),r'% completed')
    excel_submittals.append(
        ExcelSubmittal( active_data.rows[i] )
    )

log('Loading data from Excel sheet')
#Gets all the numbers present in the excel sheet
active_number_lookup_list = list(
    map(
        lambda x: x.num.split('.')[0],
        filter(
            lambda x: x.num, excel_submittals)
        )
    )

#Gets all the spec present in the Excel sheet
spec_numbers = set(map(lambda x: x.spec, excel_submittals))
set_spec_sections(spec_numbers)

#Gets a list of all placeholders
placeholders = list(filter(
    lambda x: x.spec and x.name and not x.num and x.status != 'VOID',
    excel_submittals
    ))

#Divides program into editting old submittals
new_submittals = list(
    filter(
        lambda x: x['#'] not in active_number_lookup_list,
        map(
            lambda x: x[1],
            data.iterrows()
            )
        )
    )

log(len(new_submittals), 'new submittals loaded.')

#Removes numerical duplicates from new_submittals
log('Removing numerical duplicates from new submittals')
temp = []
for i in new_submittals:
    num = i['#']
    is_duplicate = False
    for j in temp:
        if j['#'] == num:
            is_duplicate = True
            break
    if not(is_duplicate):
        temp.append(i)
new_submittals = temp

#Updates new submittals
q=0
for sub in new_submittals:
    q=q+1
    if not sub['Spec Section'] or str(sub['Spec Section']) == 'nan':
        continue
    
    log('('+str(q)+'/'+str(len(new_submittals))+') Looking for placeholders for submittal #'+str(sub['#']),':',sub['Spec Section'],context='input')
    
    #TODO Use a string.starts with method on this
    csi, validity = get_spec( sub['Spec Section'] )
    
    log('\t',csi,context='input')
    log('\t',sub['Title'],context='input')

    #TODO Put this in config
    item_threshold = 30
    if validity >= item_threshold:
        status, code = name_match_dialogue(sub['Title'], csi, placeholders)
        if status:
           update_placeholder(code, sub)
        else:
            match code:
                case 'insert':
                    insert_row(sub, excel_submittals, active, title_format = title_format)
                case 'manual':
                    input('Press enter when put in manually')
                case 'nomatch':
                    log('No matches found')
                    log('Insert Row? (Enter any letter not to insert row)',context='input')
                    should_insert = input()
                    if should_insert:
                        log('Did not insert row. Please adjust manually.')
                    else:
                        insert_row(sub, excel_submittals, active, title_format = title_format)
                case 'update':
                    user_barrier = input('Enter in "@" to skip to updating: ')
                    if user_barrier == '@':
                        log('Skipping to updates')
                        break
                    else:
                        log('"@" was not entered, continuing to next new submittal')
                case _:
                    log('An error has occurred: '+code,context='error')
                
    log()

log('Updating the existing submittal items')
update_all_rows(excel_submittals,data)

if change_spec == 'True':
    log('Changing the spec number to format:',spec_format)
    match spec_format:
        case 'long': set_sheet_to_long_spec(active_data.rows,logger_name)
        case 'short': set_sheet_to_short_spec(active_data.rows,logger_name)
        case _: log('Invalid spec format:',spec_format,
                    '. Valid spec formats: long, short')

log('Done!')
