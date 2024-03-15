from openpyxl.cell import Cell

from config import AutoLogConfig

class ExcelSubmittal:
    def __init__(self, name_cell: Cell) -> None:
        self.name_cell = name_cell
        self.name = name_cell.value

def process_line(line: list[Cell], config: AutoLogConfig) -> ExcelSubmittal:
    #TODO Make all of this dependent on the config
    #for i, cell in enumerate(line):
    #    print(i, cell.value)

    return ExcelSubmittal(
        name_cell=line[1]
    )