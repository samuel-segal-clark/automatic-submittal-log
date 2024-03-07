from logger import log

def set_sheet_to_long_spec(rows,logger_name):
    for row in rows:
        set_long_spec(row,logger_name)



def set_long_spec(row,logger_name):
    spec_num = str(row[2].value)
    csi_code = str(row[0].value)
    if csi_code:
        space_split = csi_code.split(' ')
        if len(space_split) > 2:
            spec = ' '.join(space_split[:3])+(('.'+spec_num) if row[2].value else '')
            log(logger_name,'Changed spec on row #'+str(row.row)+':',row[2].value,'->',spec)
            row[2].value = spec


def set_sheet_to_short_spec(rows,logger_name):
    for row in rows:
        set_short_spec(row,logger_name)


def set_short_spec(row,logger_name):
    spec_num = str(row[2].value)
    if spec_num:
        period_split = spec_num.split('.',1)
        space_split = spec_num.split(' ')
        #Ensures that it does not condense already condensed codes
        if len(space_split) > 1:
            #TODO Add an & detection clause, as well as a - detection clause
            if len(space_split) > 3:
                specific_spec = '.'.join(space_split[3:]).replace(' ','.')
                log(logger_name,'Changed spec on row #'+str(row.row)+':',row[2].value,'->',specific_spec)
                row[2].value = "'"+specific_spec
            elif len(period_split) > 1:
                specific_spec = period_split[1].replace(' ','.')
                log(logger_name,'Changed spec on row #'+str(row.row)+':',row[2].value,'->',specific_spec)
                row[2].value = "'"+specific_spec
            elif len(space_split) == 3:
                log(logger_name,'Changed spec on row #'+str(row.row)+':',row[2].value,'->',None)
                row[2].value = None
            else:
                log(logger_name,'Cannot reduce spec:',spec_num)
