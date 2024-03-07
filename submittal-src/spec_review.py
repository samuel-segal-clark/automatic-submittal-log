import os
import re
from functools import lru_cache

from PyPDF2 import PdfReader
from thefuzz import fuzz, process
from fuzzysearch import find_near_matches

#TODO Make this into a cached function
#TODO Do this keeping in mind the end of section
files = list(map(
    lambda x: os.path.abspath('../spec/'+x),
    os.listdir(os.path.abspath('../spec/'))
    ))

#Sorts pages into sections
sections = dict()
for file in files:
    reader = PdfReader(file)
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        all_boxes = list()
        def extract(text, cm, tm, fontDict, fontSize):
            obj = {'text': text,
                    'cm': cm,
                    'tm': tm,
                    'fontDict': fontDict,
                    'fontSize': fontSize}
            if text and text.strip():
                all_boxes.append( obj )
        page.extract_text(visitor_text = extract)
        if all_boxes:
            y = min(all_boxes, key = lambda x: x['tm'][-1])['tm'][-1]
            last_line = list(filter(lambda x: abs(x['tm'][-1] - y) < 10, all_boxes))
            last_line.sort( key = lambda x: x['tm'][-2] )
            line = ' '.join(map(lambda x: x['text'],last_line))

            matches = list(re.finditer(r'\d\d \d\d \d\d?\.?(\w{1,2})?',line))
            if matches:
                section_name = max(matches, key = lambda x: x.start() ).group()
                if len(section_name.split(' ')[-1]) < 2:
                    section_name += '0'

                if section_name not in sections:
                    sections[section_name] = list()
                sections[section_name].append(page)


    print('\n'.join(sections.keys()))
print(len(sections['34 21 80']))
input()
    

@lru_cache
def get_lines(section_name):
    global sections
    if section_name not in sections:
        print('Cant find',section_name)
        return None
    
    pages = sections[section_name]
    current_x = -1
    lines = list()
    #Gets the text within the  
    for page_num in range(len(pages)):
        page = pages[page_num]
        
        text_boxes = list()
        def extract(text, cm, tm, fontDict, fontSize):
            if text and text.strip():
                text_boxes.append( {'text': text,
                                    'cm': cm,
                                    'tm': tm,
                                    'fontDict': fontDict,
                                    'fontSize': fontSize} )
        page.extract_text(visitor_text = extract)

        line_spacing = 5
        tab_spacing = 20
        if text_boxes:
            text_boxes.sort( key = lambda x: x['tm'][-1], reverse = True )
            
            #Consolidates lines
            curr_line = list()
            y = text_boxes[0]['tm'][-1]
            for box in text_boxes:
                if box['text'] == '`':
                    continue

                curr_x, curr_y = box['tm'][-2:]
                
                if curr_line and y - curr_y > line_spacing:

                    curr_line.sort( key = lambda x: x['tm'][-2] )
                    x = min( map( lambda q: q['tm'][-2], curr_line ) )
                    line_text = ' '.join( map( lambda x: x['text'], curr_line ) )
                    pross_line = ( x, y, line_text )
                    
                    lines.append( pross_line )

                    y = curr_y
                    curr_line = list()
                curr_line.append(box)
    return lines
        
def get_possible_specs(csi, name, sub_type):
             
    lines = get_lines(csi)
    if not lines:
        print('No lines :(')
        return None
    
    #TODO This probably could be made into a recursive function,
    #     but it works too weird
    submittal_line_nums = list()
    for i in range(len(lines)):
        x, y, text = lines[i]
        if 'submit' in text.lower():    
            submittal_line_nums.append(i)

    codes = list()
    for i in submittal_line_nums:
        has_submittal = False
        has_name = False

        
        or_x, or_y, or_text = lines[i]
        x = or_x

        has_submittal = ('SUBMITTALS' in or_text)
        
        type_line_num = i
        for q in range(i, len(lines)):
            curr_x, curr_y, text = lines[q]
            if curr_x < x:
                break
            if sub_type.lower() in text.lower():
                type_line_num = q
                has_name = True
                break

        x, _, __ = lines[type_line_num]
        consider_lines = [lines[type_line_num]]
        for q in range(type_line_num, 0, -1):
            curr_x, curr_y, curr_text = lines[q]
            if curr_x < x:
                x = curr_x
                consider_lines.append(lines[q])
        consider_lines.reverse()
        coded_list = list(map(lambda x: x[2].split(' ')[0], consider_lines))

        #Cleans up the spec #
        if len(coded_list) > 1 and re.match(r'\d\.\d', coded_list[0]) and re.match(r'\d\.\d', coded_list[1]):
            del coded_list[0]
        coded_list = list(map(lambda x: x[:-1] if x[-1] in ').' else x, coded_list))
        coded_list = list(filter(lambda x: not re.match(r'[a-zA-Z]{3,}',x), coded_list))
        coded = '.'.join(coded_list)
        
        obj = ( coded, has_submittal, has_name )
        codes.append(obj)
    return codes
        

def set_spec(row):
    full_csi, name, spec_num, _, __, item_type = row.value[0:6]
    
    if not full_csi:
        return

    #DELETE THESE LINES
    if spec_num:
        return
    ##END DELETE
    csi_split = full_csi.split(' ')
    
    if len(csi_split)<3:
        return
    csi = ' '.join(csi_split[:3])
    specs = get_possible_specs(csi,name,item_type)
    print(csi, name, item_type, ':',spec_num)
    print(specs)
    
    if not(specs):
        print('----')
        return

    specs = list(set(specs))
    out_spec = None
    if spec_num:
        for (code, sub, name) in specs:
            if spec_num in code and code not in spec_num:
                out_spec = code
    if not out_spec:
        filtered = list(filter(lambda x: x[2], specs))
        if len(filtered) == 1:
            out_spec = filtered[0][0]
        elif len(filtered) > 1:
            print(filtered)
            out_spec = filtered[int(input('Index'))][0]

    if not out_spec:
        filtered = list(filter(lambda x: x[1], specs))
        if len(filtered) == 1:
            out_spec = filtered[0][0]
        elif len(filtered) > 1:
            print(filtered)
            out_spec = filtered[int(input('Index'))][0]
    

    if out_spec and (not spec_num or out_spec not in spec_num):
        print(spec_num,'->',out_spec)
        if not input():
            row[2].value = out_spec
            row[2].color = (230,255,230)
            

    print('----')

        
    
if __name__ == '__main__':
    import xlwings as xw
    wb = xw.Book('../files/submittal_log.xlsm')
    active = wb.sheets['Active']
    max_row = 2000
    active_data = active.range('F8:AD'+str(max_row))
    for i in range(0,len(active_data.rows)):
        row = active_data.rows[i]
        print()
        print('----|'+('%04d'%i)+'/'+str(len(active_data.rows))+'|----')
        set_spec(row)
