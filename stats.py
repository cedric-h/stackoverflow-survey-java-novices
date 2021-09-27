import csv
import re
from collections import Counter

def open_schema(y): return open(f'developer_survey_{y}/survey_results_schema.csv')
def open_data(y): return open(f'developer_survey_{y}/survey_results_public.csv')

def row_langs(row):
    langs = row.get('tech_do')            or \
            row.get('HaveWorkedLanguage') or \
            row.get('LanguageWorkedWith') or \
            row.get('LanguageHaveWorkedWith')
    return [x.strip() for x in langs.split(';')] if langs else []

def row_years(row):
    years = row.get('experience_range')  or \
            row.get('YearsCoding')       or \
            row.get('YearsProgram')      or \
            row.get('YearsCode')

    if years is None:
        return years
    elif (m := re.match('(\d+)(?: to |-| - )(\d+) years', years)):
        return (int(m.group(1)) + int(m.group(2))) / 2
    elif (m := re.match('(\d+)(?: or more |\+ )years', years)):
        return int(m.group(1))
    elif (m := re.match('(?:Less|More) than (a|\d+) year', years)):
        return 1 if not m.group(1).isdigit() else int(m.group(1))
    elif years == 'NA':
        return None
    else:
        return int(years)

for y in range(2016, 2021+1):
    with open_schema(y) as s, open_data(y) as d:
        print(f'year: {y}')
        data = [(row_years(row), row_langs(row)) for row in csv.DictReader(d)]
        data = [x for x in data if x[0] is not None]

        under_2 = len([years for years,_ in data if years <= 2])
        print(f'  2 or less year coders: {int(1000 * under_2/len(data))/10}%')

        c = Counter(lang for years, langs in data if years <= 2 for lang in langs)
        common = [l for l,p in c.most_common() if l not in ['NA', 'HTML', 'CSS', 'HTML/CSS']]
        print('  Top 5: ' + ', '.join(common[:5]))
        print('  Java place: ' + str(1 + common.index('Java')))
