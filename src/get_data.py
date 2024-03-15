from io import BytesIO

import pandas as pd
import openpyxl
from config import AutoLogConfig
from excel_submittal import ExcelSubmittal, process_line


def get_data(xlsx_file: BytesIO, csv_file: BytesIO, config: AutoLogConfig) -> tuple[list[ExcelSubmittal],pd.DataFrame]:
    #Reads the Excel file and converts it to higher
    #level row objects
    out_submittals: list[ExcelSubmittal] = list()
    
    wb = openpyxl.open(xlsx_file)
    active_sheet = 'active' #TODO Config this
    sheet = wb.active
    first_row = 7
    row_start = 5 #TODO Config this
    row_end = 29 #TODO Config this
    iterable = sheet.iter_rows()
    
    #Skips the first n lines
    for _ in range(first_row):
        next(iterable)
    
    for row in iterable:
        line = row[row_start : row_end]
        submittal = process_line(line)
        out_submittals.append(submittal)

    #Reads the csv file
    out_csv: pd.DataFrame = pd.read_csv(csv_file)

    return (out_submittals,out_csv)