import os
import parameters
import math

class Dataset:
    def __init__(self):
        self.price_dict = {}
        self.val_inc_set = parameters.new_val_inc_set
        self.num_val_inc = len(self.val_inc_set)
        self.initial_price = {}
        self.inc_count = {}


    def get_data(self):
        
        for y in range(2014,2020):
            for m in range(1,13):
                #print(y, m)
                if m<10:
                    month = f'0{m}'
                else:
                    month = m
                err=0
                if y!=2019:
                    with open(f'data/EMmes010.{y}{month}-C.txt',encoding='big5-hkscs') as f:
                        lines = f.readlines()
                    for i in range(5,len(lines)):
                        line = lines[i]
                        char_list = line.split()
                        try:
                            inc_id = int(char_list[0])
                            price = float(char_list[2])
                            self.inc_count[inc_id] = self.inc_count.get(inc_id, 0) + 1
                            if inc_id in self.val_inc_set:
                                self.price_dict[inc_id] = self.price_dict.get(inc_id, [])
                                self.price_dict[inc_id].append(price)
                        except:
                            err += 1
                else:
                    with open(f'data/EMmes010.{y}{month}-C.csv', encoding='big5-hkscs') as f:
                        lines = f.readlines()
                    for i in range(4,len(lines)):
                        try:
                            char_list = lines[i].split('\"')
                            inc_id = int(char_list[1])
                            price = float(char_list[5])
                            self.inc_count[inc_id] = self.inc_count.get(inc_id, 0) + 1
                            if inc_id in self.val_inc_set:
                                self.price_dict[inc_id] = self.price_dict.get(inc_id, [])
                                self.price_dict[inc_id].append(price)
                        except:
                            err+=1
        self.num_inc = len(self.inc_count.keys())

        #get initial price
        with open('data/EMmes010.201401-C.txt',encoding='big5-hkscs') as f:
            lines = f.readlines()
            for i in range(5,len(lines)):
                line = lines[i]
                char_list = line.split()
                try:
                    inc_id = int(char_list[0])
                    price = float(char_list[2])
                    # write to initial price
                    if inc_id in self.val_inc_set:
                        self.initial_price[inc_id] = price
                except:
                    err += 1

    def cal_volatility(self):
        # we use e as the base when calculating the log return
        self.volatility = {}
        for inc_id in list(self.val_inc_set):                                                
            log_return_list = []
            price_list = self.price_dict[inc_id]
            assert len(price_list)==72
            for t in range(len(price_list)-1):
                log_return = math.log(price_list[t+1]) - math.log(price_list[t])
                log_return_list.append(log_return)
            assert len(log_return_list)==71
            return_mean = sum(log_return_list) / len(log_return_list)
            vol = 0
            for r in log_return_list:
                vol += ( r - return_mean )**2
            vol = (vol/(len(log_return_list)-1))**0.5
            self.volatility[inc_id] = vol
            



if __name__ =='__main__':
    dataset = Dataset()
    dataset.get_data()
    dataset.cal_volatility()
    print('price_dict:\n', dataset.price_dict)
    print('val_inc_list:\n', dataset.val_inc_set)
    print('num_inc:', dataset.num_inc)
    print('num_valid_inc:',dataset.num_val_inc)
    print('initial_price:',dataset.initial_price)
    print('inc_count\n:',dataset.inc_count)
    print('volatility\n:', dataset.volatility)
