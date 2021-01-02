import os

with open('data/EMmes010.201901-C.csv', encoding='big5-hkscs') as f:
    lines = f.readlines()
    err=0
    for i in range(4,len(lines)):
        try:
            char_list = lines[i].split('\"')
            inc_id = int(char_list[1])
            price = float(char_list[5])
            print('inc_id:',inc_id)
            print('price:',price)
        except:
            err+=1
            print('error_id:',i)
            print('error_context:',lines[i].encode('big5-hkscs'))
    print('error_count:',err)
