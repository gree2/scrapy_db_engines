# coding: utf-8

import pandas as pd

file_csv = 'data/dbengines.csv'
file_plantuml = 'data/dbengines.plantuml'

df = pd.read_csv(file_csv)

codes = []

codes.append('@startmindmap')
codes.append('* dbengines')
for index, (name, group) in enumerate(df.groupby('rank_text')):
    # if 'complete ranking' == name.lower():
    #     continue
    codes.append('** ' + str(index + 1).zfill(3) + ' => ' + name.lower())
codes.append('@endmindmap')
codes.append('\n')

for name, group in df.groupby('rank_text'):
    codes.append('@startmindmap')
    codes.append('* ' + name.lower())
    count = len(group)
    split = 10
    for index, row in group.iterrows():
        if 30 < count:
            if 1 == row['rank']:
                codes.append('** 001')
            elif 0 == (row['rank'] - 1) % split:
                codes.append('** ' + str(row['rank'] / split + 1).zfill(3))
            stars = '*** '
        else:
            stars = '** '
        codes.append(stars + str(row['rank']).zfill(3) + ' => ' + row['name_text']) # noqa
        if 60 <= row['rank']:
            break
    codes.append('@endmindmap')
    codes.append('\n')

with open(file_plantuml, 'wt') as f:
    f.write('\n'.join(codes))
