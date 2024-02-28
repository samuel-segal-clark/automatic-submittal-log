import streamlit as st
import pandas as pd

st.write('# Automatic Submittal Log')

file_container = st.columns(2)
procore_csv = file_container[0].file_uploader('Upload Procore CSV here',type=['csv'])
submittal_log_xlsx = file_container[1].file_uploader('Upload Submittal Log XLSX here', type=['xlsx'])

with st.expander('Settings'):
    with st.form('settings_form'):

        import_settings = st.file_uploader('Import settings', type=['ini'])
        submitted = st.form_submit_button('Save Settings')

        if submitted:
            print('Submit!')
