# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/12/16 上午11:08

import re
import json
import datetime
from dateutil.relativedelta import relativedelta

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


tmp3 = {
    "name": "abc",
    "age": "11"
}
print(type(tmp3))
print("tmp3: {}".format(tmp3))

tmp4 = json.dumps(tmp3, indent=4)
print(type(tmp4))
print("tmp4: {}".format(tmp4))

tmp5 = json.loads(tmp4)
print(type(tmp5))
print("tmp5: {}".format(tmp5))


now = datetime.datetime.now()
print(now.strftime('%Y'))
print(now.strftime('%Y%m'))
print(now.strftime('%Y%m%d'))

patt3 = r'0{0,}(\d+)'
text = '01'
tmp6 = re.match(patt3, text).groups()
print("tmp6: {}".format(int(tmp6[0])-1))

patt4 = r'(\d{4})年 - (\d{4})年'
text = '2092年 - 2106年'
tmp7 = re.match(patt4, text).groups()
print("tmp7 begin: {}".format(tmp7[0]))
print("tmp7 end: {}".format(tmp7[1]))


month = datetime.datetime.now().replace(day=1).month
interval = datetime.timedelta(days=1)
last_month = (datetime.datetime.now().replace(day=1) - datetime.timedelta(days=1)).month
if last_month < 10:
    last_month = '0{0}'.format(last_month)
print(last_month)
print(datetime.datetime.now())
time_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
tmp8 = time_str[0:5] + last_month + time_str[7:]
print("tmp8: {}".format(tmp8))

year = datetime.datetime.now().replace(day=1).year
time_str = datetime.datetime.strftime(datetime.datetime.now().replace(day=1), '%Y-%m-%d %H:%M:%S')
time_tmp = time_str
time_str = time_str[0:5] + "01" + time_str[7:]
last_year = (datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(days=1)).year
tmp9 = str(last_year) + time_tmp[4:]
print("tmp9: {}".format(tmp9))


interval = -1
print(abs(interval))
now = datetime.datetime.now()
tmp10 = now + relativedelta(years=1)
print("tmp10: {}".format(tmp10))

patt5 = r'(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})'
time_str = '2018-10-23 14:15:00.000'
tmp11 = re.match(patt5, time_str).groups()
print("tmp11: {}".format(tmp11))
