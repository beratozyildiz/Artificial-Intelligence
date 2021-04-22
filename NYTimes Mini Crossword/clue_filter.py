'''
def fix_gaps(clue):
    if '___' in clue:
        clue1 = clue.replace('___','*') + ' -crossword'
        clue2 = '"' + clue1 + '"'+ ' -crossword'
        #clue3 = 'allintext:' + clue1
        return clue1,clue2
    else:
        return None
'''

def demand_synonyms(clue):
    clue1 = ''
    for char in clue:
        if char.isalnum():
            clue1 += char
    if clue1 == clue:
        return 'allintext:synonyms of {} -crossword'.format(clue)
    elif 'synonym for' in clue.lower():
        clue = 'allintext:' + clue + ' -crossword'
        return  clue

    elif 'synonym of' in clue.lower():
        clue = 'allintext:' + clue + ' -crossword'
        return clue
    else:
        return None

def get_abbreviation(clue):
    if 'abbr.' in clue.lower():
        clue1 = clue.lower().replace('abbr.', '') + ' -crossword'
        clue2 = 'allintext: synonyms of ' + clue1
        clue3 = 'allintext: abbreviations of ' + clue1
        return clue1,clue2,clue3
    else:
        return None


def clue_in_clue(clue):
    if '___' in clue and '(' in clue and ')' in clue:
        until_brackets = ''
        inside_brackets = ''
        for char in clue:
            until_brackets += char
            if char == '(':
                for i in range(clue.index(char)+1,len(clue)-1):
                    if clue[i] == ')':
                        break
                    inside_brackets += clue[i]
        clue1 = until_brackets.replace('(','').replace(')','') + ' -crossword'
        clue += ' -crossword'
        return clue, clue1
    elif '(' in clue and ')' in clue:
        until_brackets = ''
        inside_brackets = ''
        for char in clue:
            until_brackets += char
            if char == '(':
                for i in range(clue.index(char) + 1, len(clue) - 1):
                    if clue[i] == ')':
                        break
                    inside_brackets += clue[i]
        clue1 = until_brackets.replace('(', '').replace(')', '') + ' -crossword'
        clue += ' -crossword'
        return clue,clue1
    else:
        return None


def typeof_kindoff(clue):
    if 'type of' in clue.lower():
        clue += ' -crossword'
        return clue,clue.lower().replace('type of', '*'), clue.lower().replace('type of', '* *')
    if 'kind of' in clue.lower():
        clue1 = clue.lower().replace('kind of', '*') + ' -crossword'
        clue2 =  clue.lower().replace('kind of', '* *') + ' -crossword'
        clue += ' -crossword'
        return clue,clue1, clue2
    else:
        return None

def ownership(clue):
   if "'s" in clue:
       clue1 = clue.split("'s")[1] + ' of ' + clue.split("'s")[0] + ' -crossword'
       return clue, clue1
   elif "'" in clue:
       clue1 = clue.split("'")[1] + ' of ' + clue.split("'")[0] + ' -crossword'
       return clue, clue1
   else:
       return None


def opposite(clue):
    if 'not' in clue.lower():
        clue += ' -crossword'
        clue1 = clue.lower().replace('not','opposite of')
        clue2 = clue.lower().replace('not','antonyms of')
        clue3 = 'allintext:' + clue2
        return clue,clue1,clue2,clue3
    else:
        return None


def and_or(clue):
    if ' and ' in clue.lower():
        clue1 = clue.lower().split('and')[0] + ' -crossword'
        clue2 = clue.lower().split('and')[1] + ' -crossword'
        clue += ' -crossword'
        return clue1,clue2,clue
    elif ' or ' in clue.lower():
        clue1 = clue.lower().split(' or ')[0] + ' -crossword'
        clue2 = clue.lower().split(' or ')[1] + ' -crossword'
        clue += ' -crossword'
        return clue1,clue2,clue
    else:
        return None

def pop_backslash(clue):
    if "\'"  in clue:
        clue = clue.replace('"',"") + ' -crossword'
        return clue
    else:
        return clue








def filter_clue(clue):
    queries = []

    if pop_backslash(clue) != None:
        queries.append(pop_backslash(clue))
    if demand_synonyms(clue) != None:
        queries.append(demand_synonyms(clue))
    if get_abbreviation(clue) != None:
        for query in get_abbreviation(clue):
            queries.append(query)
    if clue_in_clue(clue) != None:
        for query in clue_in_clue(clue):
            queries.append(query)
    if typeof_kindoff(clue) != None:
        for query in typeof_kindoff(clue):
            queries.append(query)
    if ownership(clue) != None:
        for query in ownership(clue):
            queries.append(query)
    if opposite(clue) != None:
        for query in opposite(clue):
            queries.append(query)
    if and_or(clue) != None:
        for query in and_or(clue):
            queries.append(query)

    if len(queries) == 0:
        clue += ' -crossword'
        return [clue]

    return queries



'''In good spirits --> GLAD
Blue ribbon or gold trophy --> PRIZE
Gobble, gobble, gobble --> EATUP
Prevent from happening --> AVERT
Ancient stringed instrument --> LYRE
Thanksgiving sauce --> GRAVY
Liquid volume that would fill a 10cm x 10cm x 10cm cube --> LITER
Color of a blue sky --> AZURE
The "D" of D.M.V.: Abbr. --> DEPT
Sound of church bells --> PEAL'''


