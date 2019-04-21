# coding: utf-8

import pandas as pd

file_csv = 'data/dbengines.csv'
file_readme = 'readme.md'

df = pd.read_csv(file_csv)

codes = []

codes.append('### dbengines\n')
codes.append('![dbengines](data/dbengines.png?raw=true "dbengines")\n')

for index, (name, group) in enumerate(df.groupby('rank_text')):
    no = str(index + 1).zfill(3)
    codes.append('### {} => {}\n'.format(no, name.lower()))
    codes.append('![{}](data/dbengines_{}.png?raw=true "{}")\n'.format(name.lower(), no, name.lower()))


with open(file_readme, 'wt') as f:
    f.write('\n'.join(codes))
