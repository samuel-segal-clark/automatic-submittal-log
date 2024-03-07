import json
import streamlit as st

from textutil import get_text

st.write('# Automatic Submittal Log')

file_container = st.columns(2)
procore_csv = file_container[0].file_uploader('Upload Procore CSV here',type=['csv'])
submittal_log_xlsx = file_container[1].file_uploader('Upload Submittal Log XLSX here', type=['xlsx'])


json_text = get_text('settings-input.json')
settings_input = json.loads(json_text)

#Loads the default settings onto it
sub_log_settings = {
    key: (value['default'] if 'default' in value else None)
    for key, value in settings_input.items()
    }

settings_container = st.container()
file_upload = settings_container.file_uploader('Import settings', type=['ini'])
settings_expander = st.expander('Settings')

with settings_expander.form('Input Settings'):
    for obj_key in settings_input.keys():
        set_obj = settings_input[obj_key]
        new_element = None
        match set_obj['type']:
            case 'choice':
                new_element = st.selectbox(
                    label=set_obj['name'],
                    options=set_obj['choices']
                )
            case 'str':
                new_element = st.text_input(set_obj['name'])
            case 'num':
                new_element = st.number_input(set_obj['name'])
        sub_log_settings[obj_key] = new_element
    submit_button = st.form_submit_button('Submit')
    if submit_button:
        print(sub_log_settings)
        st.write('Settings submited! The settings have been downloaded to your computer to use in the future!')