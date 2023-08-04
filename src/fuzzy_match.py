import re
from functools import lru_cache

from thefuzz import fuzz
from logger import log


spec_sections = list()
def set_spec_sections(sections):
    global spec_sections
    spec_sections = sections




def get_largest_string(s1, s2):
    s1 = ''.join(re.split(r'-\s',s1))
    s2 = ''.join(re.split(r'-\s',s2))
    i = 0
    for i in range( min( len(s1), len(s2) ) ):
        if s1[i] != s2[i]:
            break
    return i
#TODO Get largest last? Similar to get largest string, but works from the end
#Could help with more varied spec formats


#Maybe change this to set up, then match for improved performance
#Matches the Procore spec section to the section in the log
spec_dict = dict()
@lru_cache
def get_spec(spec):
    global spec_dict
    global spec_sections

    adjusted_spec = ' '.join(spec.split('.'))
    #TODO Put weighting into config
    csi =  max(spec_sections, key = lambda x: (fuzz.ratio(spec, x)+ 8*get_largest_string(str(spec), str(x))) )
    return csi, fuzz.ratio(spec, csi)
    

#TODO Maybe separate the dialogue?
def name_match_dialogue(name, spec, placeholders, number_matches = 4):
    same_csi = list(filter(lambda x: x.spec == spec, placeholders))
    same_csi.sort(key = lambda x: fuzz.token_sort_ratio(name,x.name),reverse=True)

    if not len(same_csi):
        return (False, 'nomatch')

    num_match = min( number_matches, len(same_csi) )

    #Selection dialogue
    for i in range(num_match):
            log('\t'+str(i+1)+')  (',str(fuzz.token_sort_ratio(same_csi[i].name,name))    ,')',same_csi[i].name,context='input',)
    log('\t'+str(num_match+1)+') None of the Above',context='input',)
    n = input('\t ')
    log(n, do_print=False)
    if n.isdigit() and int(n)>0 and int(n)<num_match:
        return (True, same_csi[int(n)-1])

    if n == '$':
        return (False, 'manual')
    if n == '@':
        return (False, 'update')
    return (False, 'insert')
