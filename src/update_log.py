import pandas as pd
from openpyxl import load_workbook

from io import BytesIO
from tempfile import NamedTemporaryFile

from config import AutoLogConfig


def update_log(xlsx_file: BytesIO, csv_file: BytesIO, config: AutoLogConfig) -> BytesIO:
    wb = load_workbook(xlsx_file)
    #df = pd.DataFrame(csv_file)

    
    out_bytes = BytesIO()
    wb.save(out_bytes)
    return out_bytes