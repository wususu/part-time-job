# coding:UTF-8



with open('city.txt', 'r') as fp:
    text = fp.read()

r = []

strs = text.splitlines()

for obj in strs:
    objs = obj.split("：")
    if len(objs) != 2:
        continue
    citys = objs[1].split(" ")
    citys = list(map(lambda c: c.strip(), citys))
    for city in citys:
        if city:
            r.append(city)

