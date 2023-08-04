import pandas as pd

status_dictionary = {
                'For Record Only': 'FRO',
                'Void': 'VOID',
                'Resubmittal Reqd.': 'Revise & Resubmit',
                'Additional Info. Reqd.': "Add'l Info Req'd",
                'Rejected': 'Rejected',
                'Approved': 'Approved',
                'Open': 'Open - in Review',
                'Closed':'FRO'
                }

def translate_status(status):
    if not(status):
        return None
    if pd.isna(status):
        return None
    if status in status_dictionary:
        return status_dictionary[status]
    return status
    
