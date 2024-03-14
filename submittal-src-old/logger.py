import datetime
import os

#Possible refactor?
def get_logger_name():
    return 'changelog_'+datetime.datetime.now().strftime('%m-%d-%y-%H-%M')+'.txt'


log_name = None
def set_log_name(name):
    global log_name
    log_name = name


color_dict = {
    'input': ' \033[96m',
    'error': '\033[91m'
}
def log(*text,do_print=True, context=None):
    global log_name
    complete_text = ' '.join(map(str,text))
    if do_print:
        print_text = complete_text
        if context:
            print_text = color_dict[context] + print_text + '\033[0m'
        print(print_text)
    with open(os.path.abspath('..\logs\\'+log_name),'a') as file:
        try:
            file.write(complete_text+'\n')
        except:
            pass
