import os
import parameters
from preprocess import Dataset
import matplotlib.pyplot as plt
import numpy as np

class RDataset:
    def __init__(self):
        self.val_inc_set = parameters.new_val_inc_set
        self.net_income_dict = None
        self.count_dict = None
        self.val_inc_count = None
        self.dataset = Dataset()
        self.initial_price = None
        self.return_ratio_dict = None
        self.full_inc_set = dict()
        self.full_count_dict = dict()

    def get_data(self):
        self.dataset.get_data()
        self.initial_price = self.dataset.initial_price
        self.net_income_dict = {}
        self.count_dict = {}
        for y in range(2014,2020):
            for q in [2,4]:
                #with open(f"financial_report/U_{y}Q{q}.csv", encoding='big5-hkscs') as f:
                with open(f"financial_report/U_{y}Q{q}.csv") as f:
                    lines = f.readlines()
                    err = 0
                    #for i in range(38,len(lines)):
                    for i in range(len(lines)):
                        line = lines[i].strip()
                        char_list = line.split(',')
                        if char_list[1] and char_list[1][0]=='(':
                            char_list[1] = char_list[1][1:-1]
                        try:
                            inc_id = int(char_list[0])
                            net_income = float(char_list[1])
                            #using full dict to check if company has full data
                            self.full_inc_set[inc_id] = self.full_inc_set.get(inc_id, [])
                            self.full_inc_set[inc_id].append(net_income)
                            self.full_count_dict[inc_id] = self.full_count_dict.get(inc_id, 0) +1
                            if inc_id in self.val_inc_set:
                                self.net_income_dict[inc_id] = self.net_income_dict.get(inc_id, [])
                                self.net_income_dict[inc_id].append(net_income)
                                self.count_dict[inc_id] = self.count_dict.get(inc_id, 0) + 1
                        except:
                            err +=1
        '''
        #print the number
        print('full_count_dict:', self.full_count_dict)
        count_list = [0 for i in range(13)]
        for v in self.full_count_dict.values():
            count_list[v] +=1
        print('count_list:',count_list)
        new_parameters = set()
        for inc,v in self.full_count_dict.items():
            if v >= 10 and inc>=1000:
                new_parameters.add(inc)
        print('new_parameters:', new_parameters)
        print(done)
        '''

        self.val_inc_count = 0
        for inc ,c in self.count_dict.items():
            if c==12:
                self.val_inc_count+=1

        #compute income_sum_dict
        self.income_sum_dict = {}
        for inc_id in list(self.val_inc_set):
            assert len(self.net_income_dict[inc_id])==12
            self.income_sum_dict[inc_id] = sum(self.net_income_dict[inc_id])

        print('net_income_dict:',self.net_income_dict)
        print('num of inc:', len(self.net_income_dict.keys()))
        print('count_dict:', self.count_dict)
        print('val_inc_count:',self.val_inc_count)
        print('val_inc_set:', self.val_inc_set)
        print('initial_price:',self.initial_price)
        print('income_sum_dict:', self.income_sum_dict)

    def cal_return_ratio(self):
        self.return_ratio_dict = {}
        for inc_id in list(self.val_inc_set):
            assert len(self.net_income_dict[inc_id])==12
            income_sum = sum(self.net_income_dict[inc_id])
            initial_price = self.initial_price[inc_id]
            return_ratio = income_sum / initial_price
            self.return_ratio_dict[inc_id] = return_ratio

        print('return_ratio_dict:', self.return_ratio_dict)
        print('max_return', max(self.return_ratio_dict.values()))

    def cal_volatility(self):
        self.dataset.cal_volatility()
        print('volatility:',self.dataset.volatility)

    def plot_scatter(self):
        x = []
        y = []
        for inc in list(self.val_inc_set):
            volatility = self.dataset.volatility[inc]
            return_ratio = self.return_ratio_dict[inc]
            x.append(volatility)
            y.append(return_ratio)
        plt.scatter(x, y)
        plt.xlabel('volatility')
        plt.ylabel('return ratio')                 #中文？？
        plt.title('return_ratio vs volatility')
        plt.savefig('figure/scatter/scatter.png')
        plt.clf()

    def get_corrcoef(self):
        x = []
        y = []
        for inc in list(self.val_inc_set):
            volatility = self.dataset.volatility[inc]
            return_ratio = self.return_ratio_dict[inc]
            if 0.05<=volatility<=0.15 and 0<=return_ratio<=2:                   #remove outliers
                x.append(volatility)
                y.append(return_ratio)
        x = np.array(x)
        y = np.array(y)
        self.corrcoef = np.corrcoef(x, y)[0][1]

        print('correlation coefficient:', self.corrcoef)



if __name__ =='__main__':
    r = RDataset()
    r.get_data()
    r.cal_return_ratio()
    r.cal_volatility()
    r.plot_scatter()
    r.get_corrcoef()
