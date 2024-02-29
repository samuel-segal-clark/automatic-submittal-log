import streamlit as st

st.write('# Automatic Submittal Log')

file_container = st.columns(2)
procore_csv = file_container[0].file_uploader('Upload Procore CSV here',type=['csv'])
submittal_log_xlsx = file_container[1].file_uploader('Upload Submittal Log XLSX here', type=['xlsx'])


#TODO Read this from a file (i.e. default settings)
sub_log_settings = {

}

#TODO Read this from a file (i.e. settings types json)
settings_input = {
    'title-format': {
        'name': 'Title Format',
        'type': 'choice',
        'choices': [
            'Default',
            'WMATA'
        ]
    },
    'spec-section': {
        'name': 'Spec Section Column',
        'type': 'str'
    }
}

settings_container = st.container()
file_upload = settings_container.file_uploader('Import settings', type=['ini'])
settings_expander = st.expander('Settings')

form_elements = dict()
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
        form_elements[obj_key] = new_element
    submit_button = st.form_submit_button('Submit')
    if submit_button:
        st.write('Settings submited! The settings have been downloaded to your computer to use in the future!')