import streamlit as st
from update_log import update_log

excel = st.file_uploader('Excel File')
if excel:
    e_bytes = excel.getvalue()
    res_bytes = update_log(excel, None, None)
    st.download_button('Download result', res_bytes, file_name='output.xlsx')