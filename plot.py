import os
from preprocess import Dataset
import matplotlib.pyplot as plt

class Worktable:
    def __init__(self):
        self.dataset = Dataset()
        self.dataset.get_data()

    def plot_price(self):
        time_axis = [2014.0+1.0/24+i*1.0/12 for i in range(72)] 
        for inc_id in list(self.dataset.val_inc_set):
            price_list = self.dataset.price_dict[inc_id]
            plt.plot(time_axis, price_list)
            plt.xlabel('years')
            plt.ylabel('price per share')
            plt.xlim((2014,2020))
            plt.title(f'{inc_id}')
            plt.savefig(f'figure/price/{inc_id}.png')
            plt.clf()








if __name__ =='__main__':
    w = Worktable()
    #print(w.dataset.price_dict)
    w.plot_price()
