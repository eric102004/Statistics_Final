import os

with open('mean.csv',encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        print(line.encode('utf-8'))
        #char_list = line.split(',')
        #print(char_list)
