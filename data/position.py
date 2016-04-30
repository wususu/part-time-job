# coding:UTF-8

import re

with open('position.txt', 'r') as fp:
    text = fp.read()

r = []
text = text.strip()
text = re.sub(r'（.*）', '', text)
text = re.sub(r'\(.*\)', '', text)
text = re.sub(r'\d+', ' ', text)
strs = re.split(r'[\r]*[\n]*[\s]*[，]*[、]*', text)

for obj in strs:
    obj = obj.strip()
    if len(obj) == 1:
        continue
    if obj[-2:] == '学院':
        continue
    if obj not in r:
        r.append(obj)

print(r)

