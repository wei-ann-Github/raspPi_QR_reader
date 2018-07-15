import random

import names
import pandas as pd

houseList = ['Gate', 'Ballmer', 'Satya', 'Allen']
names_list = []; house = []
for i in range(100):
	name = names.get_full_name()
	names_list.append(name)
	house = houseList[random.randint(0, 3)]

myDict = {'names':names_list, 'houses':house}
df = pd.DataFrame(myDict)
df.to_csv('names.csv', index=False)
