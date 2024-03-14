import pandas as pd
import xlwings as xw

from translate_status import translate_status
from logger import get_logger_name, log

def update_row(row,data):
   
    
    if not(row.num):
        return
    
    num_split = row.num.split('.')
    #TODO Make the program more robust for non-conforming numbers
    if len(num_split) < 2:
        return

    index_num = num_split[0]
    revision_num = num_split[1]

    sub_rows = data.loc[data['#'] == index_num]
    if sub_rows.empty:
        #This shouldn't occur, but sometimes Procore is weird :(
        return

    sub_recent = sub_rows.iloc[0]
    sub_first = sub_rows.iloc[-1]

    #Updates the revision number
    if str(revision_num) != str(sub_recent['Rev.']):
        new_num = str(index_num) + '.' + str(sub_recent['Rev.'])
        row.num = new_num
        log('\tUpdated submittal # #'+str(index_num)+':\t',row.num,'->',new_num)

    #Updates the returned date
    if ( ( type(row.return_date) is str and '\n' in row.return_date) or not row.return_date) and sub_first['Returned Date'] and 'nan' not in str(sub_first['Returned Date']):
        returned_date_str = str(sub_first['Returned Date']).split(' ')[0].split('\n')[0]
        row.return_date = returned_date_str
        log('\tUpdated return date #'+str(index_num)+':\t',returned_date_str)

    translated_status = translate_status(sub_recent['Status'])
    #Updates the statuses
    if row.status != translated_status and row.status != 'AAN':
        log('\tUpdated status '+str(index_num)+':\t',row.status,'->',translated_status)
        row.status = translated_status
        


    #Updates the revised submittal date
    for i in range(len(row.revisions)):

        revision_data = sub_rows.loc[sub_rows['Rev.'] == i+1]
        if len(revision_data) == 1:

            this_date = row.revisions[i]
            revision_row = revision_data.iloc[0]
            if revision_row['Created At']:
                created_date_str = revision_row['Created At'].split(' ')[0]
                if (not(this_date) or this_date.strftime('%m/%d/%Y') != created_date_str):
                    log('\tUpdated revised submittal date #'+str(index_num)+':','Revised submittal',row.revisions[i],'->',created_date_str)
                    row.revisions[i] = created_date_str

    for i in range(sub_recent['Rev.'],len(row.revisions)):
        if row.revisions[i]:
            log('\tRemoved superfluous date: #',row.num,':',row.revisions[i])
        row.revisions[i] = None

    row.update()

#Updates existing rows on the submittal log
def update_all_rows(rows,data):
    for row in rows:
        update_row(row,data)
        
            

#TODO Fix this
if __name__ == '__main__':
    data = pd.read_csv('../files/data.csv')
    wb = xw.Book('../files/submittal_log.xlsm')
    active = wb.sheets['Active']
    max_row = 2000
    active_data = active.range('F8:AD'+str(max_row))
    logger_name = get_logger_name()
    update_all_rows(active_data.rows,data,get_logger_name)
    
