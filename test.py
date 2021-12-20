# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/12/16 上午11:08

import re

patt1 = r'\s*'
patt2 = r'\s+'

text = ['abc ddd few3r', 'gerwgre bvfrdegr 2']

# print(text)
tmp1 = []
for i in text:
    tmp1.append(re.split(patt1, i))
print(tmp1)


tmp2 = []
for i in text:
    tmp2.append(re.split(patt2, i))
print(tmp2)